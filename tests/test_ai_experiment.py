import copy

import numpy as np
import pytest

from gmail_classifier.ai_experiment import split_groups
from gmail_classifier.baseline import evaluate, load_model, save_model, train
from gmail_classifier.dataset import validate_records


@pytest.fixture
def ai_records(records):
    rows = [copy.deepcopy(r) for r in records if not r["is_spam"]]
    for row in rows:
        row["source"] = "gmail_ai_labeled"
    return rows


def test_ai_labels_require_both_explicit_opt_ins(ai_records):
    with pytest.raises(ValueError):
        validate_records(ai_records)
    with pytest.raises(ValueError):
        validate_records(ai_records, allow_private=True)
    with pytest.raises(ValueError):
        validate_records(ai_records, allow_ai=True)
    assert validate_records(ai_records, allow_private=True, allow_ai=True) == ai_records


def test_group_split_is_reproducible_and_rare_classes_stay_in_train(ai_records):
    rare = next(r for r in ai_records if r["category"] == "Financeiro")
    rows = [r for r in ai_records if r["category"] != "Financeiro" or r["id"] == rare["id"]]
    # Two distinct messages in a shared thread must remain together.
    similar = [r for r in rows if r["category"] == "Suporte"][:2]
    similar[1]["group_id"] = similar[0]["group_id"]
    original = copy.deepcopy(rows)
    assigned = split_groups(rows)
    assert rows == original
    assert assigned == split_groups(rows)
    assert next(r for r in assigned if r["id"] == rare["id"])["split"] == "train"
    for group in {r["group_id"] for r in assigned}:
        assert len({r["split"] for r in assigned if r["group_id"] == group}) == 1
    assert {r["split"] for r in assigned} == {"train", "validation", "test"}


def test_partial_coverage_does_not_weaken_human_or_synthetic_validation(records, ai_records):
    rows = [r for r in ai_records if r["category"] in {"Financeiro", "Comercial"}]
    validate_records(rows, allow_private=True, allow_ai=True)
    for row in rows:
        row["source"] = "gmail_reviewed"
    with pytest.raises(ValueError):
        validate_records(rows, allow_private=True, allow_ai=True)
    ai_records[0]["group_id"] = ai_records[-1]["group_id"]
    with pytest.raises(ValueError, match="boundary"):
        validate_records(ai_records, allow_private=True, allow_ai=True)


def test_single_spam_class_preserves_reference_and_trains_only_category(ai_records, model):
    with pytest.raises(ValueError, match="explicit trusted reference"):
        train(ai_records, allow_private=True, allow_ai=True)
    before = model.spam.named_steps["classifier"].coef_.copy()
    fitted = train(ai_records, allow_private=True, allow_ai=True, spam_reference=model)
    assert fitted.spam is not model.spam
    np.testing.assert_array_equal(fitted.spam.named_steps["classifier"].coef_, before)
    np.testing.assert_array_equal(model.spam.named_steps["classifier"].coef_, before)
    assert fitted.provenance == {"spam_source": "synthetic", "category_source": "gmail_ai_labeled", "human_gold_labels": False}


def test_ai_category_fit_never_learns_test_text_or_labels(ai_records, model):
    first = train(ai_records, allow_private=True, allow_ai=True, spam_reference=model)
    altered = copy.deepcopy(ai_records)
    for row in altered:
        if row["split"] != "train":
            row["body"] += " heldoutonlytoken"
            row["category"] = "Financeiro"
    second = train(altered, allow_private=True, allow_ai=True, spam_reference=model)
    assert "heldoutonlytoken" not in second.category.named_steps["tfidf"].vocabulary_
    np.testing.assert_array_equal(first.category.named_steps["classifier"].coef_,
                                  second.category.named_steps["classifier"].coef_)


def test_ai_evaluation_discloses_proxy_labels_and_missing_spam(ai_records, model, tmp_path):
    fitted = train(ai_records, allow_private=True, allow_ai=True, spam_reference=model)
    report = evaluate(fitted, ai_records, allow_private=True, allow_ai=True)
    assert "not human-verified" in report["warning"]
    assert report["model_provenance"]["human_gold_labels"] is False
    assert all(split["spam_recall_assessable"] is False for split in report["splits"].values())
    assert all(split["spam_positive_count"] == 0 for split in report["splits"].values())
    path = tmp_path / "ai.joblib"
    save_model(fitted, path)
    assert load_model(path).provenance == fitted.provenance
