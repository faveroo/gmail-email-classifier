"""Convert probabilities into local label suggestions only."""

from dataclasses import dataclass
from math import isfinite

from .dataset import CATEGORIES


@dataclass(frozen=True)
class Policy:
    spam_threshold: float = 0.90
    legitimate_threshold: float = 0.20
    category_threshold: float = 0.60

    def __post_init__(self):
        if not 0 <= self.legitimate_threshold < self.spam_threshold <= 1:
            raise ValueError("Require 0 <= legitimate < spam <= 1")
        if not 0 <= self.category_threshold <= 1:
            raise ValueError("Category threshold must be in [0, 1]")

    def decide(self, spam_probability, category=None, confidence=None, *, known_text=True):
        if not isfinite(spam_probability) or not 0 <= spam_probability <= 1:
            raise ValueError("Invalid spam probability")
        result = {"spam_probability": float(spam_probability), "category": None,
                  "category_confidence": None, "action": "review", "label": "IA/Revisar"}
        if not known_text:
            return result
        if spam_probability >= self.spam_threshold:
            return {**result, "action": "suggest_label", "label": "IA/SPAM"}
        if spam_probability > self.legitimate_threshold:
            return result
        if category not in CATEGORIES or confidence is None:
            return result
        if not isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError("Invalid category probability")
        result.update(category=category, category_confidence=float(confidence))
        if confidence >= self.category_threshold:
            result.update(action="suggest_label", label=f"IA/{category}")
        return result
