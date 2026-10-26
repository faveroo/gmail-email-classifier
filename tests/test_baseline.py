import copy
import json

import joblib
import numpy as np
import pytest

from gmail_classifier.baseline import evaluate, load_model, save_model, train
from gmail_classifier.cli import main


def test_training_does_not_learn_held_out_data(records):
    original = train(records)
    altered = copy.deepcopy(records)
    for row in altered:
        if row["split"] != "train":
            row["subject"] += " heldoutonlyword"
            if not row["is_spam"]:
                # Permute labels while retaining all categories in each split.
                categories = list(original.category.classes_)
                row["category"] = categories[(categories.index(row["category"]) + 1) % len(categories)]
    other = train(altered)
    assert "heldoutonlyword" not in other.spam.named_steps["tfidf"].vocabulary_
    np.testing.assert_array_equal(original.spam.named_steps["classifier"].coef_,
                                  other.spam.named_steps["classifier"].coef_)
    np.testing.assert_array_equal(original.category.named_steps["classifier"].coef_,
                                  other.category.named_steps["classifier"].coef_)


def test_spam_not_used_for_category_vocabulary(records, model):
    assert "milionário" not in model.category.named_steps["tfidf"].vocabulary_
    assert "milionario" not in model.category.named_steps["tfidf"].vocabulary_


def test_persistence_and_unknown_text(model, tmp_path):
    path = tmp_path / "model.joblib"
    save_model(model, path)
    loaded = load_model(path)
    assert loaded.predict("Fatura", "Pagamento de boleto") == model.predict("Fatura", "Pagamento de boleto")
    assert loaded.predict("zzqxxyz", "") ["label"] == "IA/Revisar"
    with pytest.raises(ValueError):
        loaded.predict(" ", "")
    joblib.dump({"format_version": -1}, path)
    with pytest.raises(ValueError):
        load_model(path)


def test_spam_and_uncertainty_skip_category(model, monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("Category model should not be called")
    monkeypatch.setattr(model.category, "predict_proba", fail)
    monkeypatch.setattr(model.spam, "predict_proba", lambda x: np.array([[0.05, 0.95]]))
    assert model.predict("pagamento", "")["label"] == "IA/SPAM"
    monkeypatch.setattr(model.spam, "predict_proba", lambda x: np.array([[0.5, 0.5]]))
    assert model.predict("pagamento", "")["label"] == "IA/Revisar"


def test_legitimate_route_uses_category_model(model, monkeypatch):
    monkeypatch.setattr(model.spam, "predict_proba", lambda x: np.array([[0.95, 0.05]]))
    probabilities = np.zeros((1, len(model.category.classes_)))
    probabilities[0, list(model.category.classes_).index("Financeiro")] = 1.0
    monkeypatch.setattr(model.category, "predict_proba", lambda x: probabilities)
    assert model.predict("pagamento", "boleto")["label"] == "IA/Financeiro"


def test_report_is_serializable_and_metrics_explicit(records, model):
    report = evaluate(model, records)
    json.dumps(report)
    assert report["splits"]["test"]["count"] == 20
    for split in report["splits"].values():
        assert 0 <= split["review_rate"] <= 1
        assert len(split["category_on_true_legitimate"]["confusion_matrix"]) == 9
        assert "spam_policy_false_positives" in split


def test_cli_round_trip(records, tmp_path, capsys):
    dataset = tmp_path / "data.json"
    dataset.write_text(json.dumps(records), encoding="utf-8")
    artifact, report = tmp_path / "m.joblib", tmp_path / "r.json"
    main(["train", "--dataset", str(dataset), "--model", str(artifact), "--report", str(report)])
    assert artifact.exists() and json.loads(report.read_text())["seed"] == 42
    capsys.readouterr()
    main(["predict", "--model", str(artifact), "--subject", "Fatura", "--body", "Pagamento"])
    assert "spam_probability" in json.loads(capsys.readouterr().out)
    with pytest.raises(SystemExit) as error:
        main(["train", "--dataset", str(dataset), "--model", str(dataset)])
    assert error.value.code == 2
