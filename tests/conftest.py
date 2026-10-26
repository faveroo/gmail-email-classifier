from pathlib import Path

import pytest

from gmail_classifier.baseline import train
from gmail_classifier.dataset import load_dataset


@pytest.fixture
def records():
    return load_dataset(Path(__file__).resolve().parents[1] / "data/examples/synthetic-v1.json")


@pytest.fixture
def model(records):
    return train(records)
