"""Deterministic group splits for explicitly authorized, AI-labeled experiments."""

from collections import defaultdict
from copy import deepcopy
import random

from .dataset import validate_records


def split_groups(records: list[dict], seed=42) -> list[dict]:
    """Stratify group label signatures without inspecting text or fitting features.

    Singleton signatures stay in train; two groups use train/test. Larger strata
    reserve at least one independent group for validation and test. Rare classes
    may therefore be unassessable in held-out splits, which reports must disclose.
    """
    rows = deepcopy(records)
    groups = defaultdict(list)
    for row in rows:
        groups[row["group_id"]].append(row)
    strata = defaultdict(list)
    for group_id, members in groups.items():
        signature = tuple(sorted({"SPAM" if r["is_spam"] else r["category"] for r in members}))
        strata[signature].append(group_id)
    rng = random.Random(seed)
    for signature in sorted(strata):
        group_ids = sorted(strata[signature])
        rng.shuffle(group_ids)
        count = len(group_ids)
        test_count = max(1, round(count * 0.2)) if count >= 2 else 0
        validation_count = max(1, round(count * 0.2)) if count >= 3 else 0
        for index, group_id in enumerate(group_ids):
            split = ("test" if index < test_count else
                     "validation" if index < test_count + validation_count else "train")
            for row in groups[group_id]:
                row["split"] = split
    return validate_records(rows, allow_private=True, allow_ai=True)
