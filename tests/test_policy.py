import pytest

from gmail_classifier.policy import Policy


@pytest.mark.parametrize("spam,confidence,label", [
    (0.90, None, "IA/SPAM"), (1.0, None, "IA/SPAM"),
    (0.89, 1.0, "IA/Revisar"), (0.21, 1.0, "IA/Revisar"),
    (0.20, 0.60, "IA/Financeiro"), (0.0, 0.59, "IA/Revisar"),
])
def test_boundaries(spam, confidence, label):
    assert Policy().decide(spam, "Financeiro", confidence)["label"] == label


def test_unknown_text_always_review():
    assert Policy().decide(1.0, known_text=False)["label"] == "IA/Revisar"


@pytest.mark.parametrize("options", [
    {"spam_threshold": 0.1}, {"legitimate_threshold": -1},
    {"spam_threshold": float("nan")}, {"category_threshold": 2},
])
def test_invalid_thresholds(options):
    with pytest.raises(ValueError):
        Policy(**options)


@pytest.mark.parametrize("value", [-1, 2, float("nan"), float("inf")])
def test_invalid_probability(value):
    with pytest.raises(ValueError):
        Policy().decide(value)
