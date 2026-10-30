"""Separate multilingual SMS spam experiment using the gated SpamShield corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

MODEL_FORMAT = 1
DATASET_ID = "M-Arjun/SpamShield-Datasets"
LABELS = [0, 1]
SPLITS = ("train", "validation", "test")


def _dependencies():
    try:
        import pandas as pd
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise RuntimeError(
            "Install the multilingual extra: python -m pip install -e '.[multilingual]'"
        ) from exc
    return pd, hf_hub_download


def download_dataset(cache_dir: str | Path | None = None) -> Path:
    """Download the gated parquet after the user accepts HF dataset access terms."""
    _, hf_hub_download = _dependencies()
    options = {"repo_id": DATASET_ID, "filename": "combined.parquet", "repo_type": "dataset"}
    if cache_dir is not None:
        options["cache_dir"] = str(cache_dir)
    try:
        return Path(hf_hub_download(**options))
    except Exception as exc:
        # Do not include request headers, tokens, or upstream response bodies in errors.
        raise RuntimeError(
            "Dataset download failed. Sign in with `hf auth login` and accept the access "
            "conditions on the Hugging Face dataset page first."
        ) from exc


def load_frame(path: str | Path):
    pd, _ = _dependencies()
    frame = pd.read_parquet(path, columns=["text", "label", "category", "language"])
    required = {"text", "label", "category", "language"}
    if not required.issubset(frame.columns) or frame.empty:
        raise ValueError("Dataset must contain text, label, category and language columns")
    frame = frame.dropna(subset=["text", "label", "language"]).copy()
    frame["text"] = frame["text"].astype(str).str.strip()
    frame["language"] = frame["language"].astype(str).str.strip()
    frame["label"] = frame["label"].astype(int)
    if (frame["text"].eq("").any() or not set(frame["label"].unique()).issubset({0, 1})
            or frame["language"].eq("").any()):
        raise ValueError("Dataset contains empty text/language or labels outside 0 and 1")

    # Collapse exact normalized duplicates before splitting to prevent direct leakage.
    frame["_normalized"] = frame["text"].str.casefold().str.split().str.join(" ")
    conflicting = frame.groupby("_normalized")["label"].nunique().gt(1)
    if conflicting.any():
        raise ValueError("Conflicting spam labels found for identical normalized messages")
    frame = frame.drop_duplicates("_normalized", keep="first").drop(columns="_normalized")
    return frame.reset_index(drop=True)


def _split_frame(frame, seed: int = 42):
    # Each language × binary-label stratum is represented in every split when possible.
    strata = frame["language"].astype(str) + "|" + frame["label"].astype(str)
    train, heldout = train_test_split(
        frame, test_size=0.30, random_state=seed, stratify=strata
    )
    heldout_strata = heldout["language"].astype(str) + "|" + heldout["label"].astype(str)
    validation, test = train_test_split(
        heldout, test_size=0.50, random_state=seed, stratify=heldout_strata
    )
    result = {"train": train, "validation": validation, "test": test}
    # Guard exact-string split isolation even if the splitter changes in the future.
    text_sets = [set(part["text"].str.casefold().str.split().str.join(" ")) for part in result.values()]
    if any(text_sets[i] & text_sets[j] for i in range(3) for j in range(i + 1, 3)):
        raise ValueError("Duplicate normalized message crossed a split boundary")
    return result


def _pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char", ngram_range=(2, 5), min_df=2, max_features=500_000,
            sublinear_tf=True, dtype=np.float32,
        )),
        ("classifier", LogisticRegression(
            max_iter=1000, random_state=42, class_weight="balanced", solver="liblinear"
        )),
    ])


def _evaluate(model, frame):
    expected = frame["label"].tolist()
    predicted = model.predict(frame["text"]).astype(int).tolist()
    probabilities = model.predict_proba(frame["text"])[:, 1]
    by_language = {}
    for language, rows in frame.groupby("language", sort=True):
        truth = rows["label"].astype(int).tolist()
        guess = model.predict(rows["text"]).astype(int).tolist()
        by_language[str(language)] = {
            "count": len(rows),
            "spam_count": int(sum(truth)),
            "accuracy": float(sum(a == b for a, b in zip(truth, guess)) / len(rows)),
            "spam_f1": float(f1_score(truth, guess, pos_label=1, zero_division=0)),
            "macro_f1": float(f1_score(truth, guess, average="macro", zero_division=0)),
            "confusion_matrix": confusion_matrix(truth, guess, labels=LABELS).tolist(),
        }
    return {
        "count": len(frame),
        "distribution": {"ham": int((frame["label"] == 0).sum()),
                         "spam": int((frame["label"] == 1).sum())},
        "language_count": int(frame["language"].nunique()),
        "accuracy": float(sum(a == b for a, b in zip(expected, predicted)) / len(frame)),
        "spam_f1": float(f1_score(expected, predicted, pos_label=1, zero_division=0)),
        "macro_f1": float(f1_score(expected, predicted, average="macro", zero_division=0)),
        "classification_report": classification_report(
            expected, predicted, labels=LABELS, target_names=["ham", "spam"],
            output_dict=True, zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(expected, predicted, labels=LABELS).tolist(),
        "spam_probability_mean": float(probabilities.mean()),
        "by_language": by_language,
    }


def train_and_evaluate(dataset_path: str | Path, model_path: str | Path,
                       report_path: str | Path, *, seed: int = 42) -> dict:
    frame = load_frame(dataset_path)
    if frame["language"].nunique() < 2 or set(frame["label"].unique()) != {0, 1}:
        raise ValueError("Expected multiple languages and both binary labels")
    splits = _split_frame(frame, seed)
    model = _pipeline()
    model.fit(splits["train"]["text"], splits["train"]["label"])

    file_hash = hashlib.sha256(Path(dataset_path).read_bytes()).hexdigest()
    report = {
        "source": DATASET_ID,
        "dataset_sha256": file_hash,
        "license": "CC-BY-4.0",
        "attribution": "M-Arjun, SpamShield-Datasets (Hugging Face), CC-BY-4.0",
        "seed": seed,
        "split_strategy": "Exact normalized duplicates collapsed, then stratified 70/15/15 by language × binary label.",
        "total_count": len(frame),
        "languages": sorted(frame["language"].unique().tolist()),
        "full_distribution": {"ham": int((frame["label"] == 0).sum()),
                              "spam": int((frame["label"] == 1).sum())},
        "category_distribution": {str(k): int(v) for k, v in
                                  frame["category"].fillna("unknown").value_counts().items()},
        "model": "Character TF-IDF (2–5 grams, max 500k) + Logistic Regression",
        "dataset_note": (
            "SMS corpus, not a Gmail email benchmark; Dutch and Italian records are spam-only. "
            "Some fine-grained categories are sparse."
        ),
        "splits": {name: _evaluate(model, splits[name]) for name in SPLITS},
    }
    artifact = {
        "format_version": MODEL_FORMAT,
        "sklearn_version": sklearn.__version__,
        "dataset_sha256": file_hash,
        "model": model,
    }
    model_path, report_path = Path(model_path), Path(report_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if model_path.resolve() == report_path.resolve():
        raise ValueError("Model and report paths must differ")
    joblib.dump(artifact, model_path)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def load_spamshield_model(path: str | Path):
    artifact = joblib.load(path)
    if (not isinstance(artifact, dict) or artifact.get("format_version") != MODEL_FORMAT
            or artifact.get("sklearn_version") != sklearn.__version__):
        raise ValueError("Incompatible SpamShield model; retrain with this environment")
    return artifact["model"]


def predict(model, text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Enter a message to classify")
    probabilities = model.predict_proba([text])[0]
    return {"label": "spam" if probabilities[1] >= 0.5 else "ham",
            "spam_probability": float(probabilities[1]),
            "ham_probability": float(probabilities[0])}

