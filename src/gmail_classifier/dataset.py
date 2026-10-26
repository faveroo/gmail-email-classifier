"""Strict validation of the synthetic dataset contract."""

import json
from pathlib import Path

CATEGORIES = (
    "Financeiro", "Suporte", "RH", "Sistemas", "Comercial",
    "Administrativo", "Notificações", "Pessoal", "Outros",
)
SPLITS = ("train", "validation", "test")
FIELDS = {"id", "group_id", "subject", "body", "is_spam", "category", "source", "split"}


def normalize_text(subject: str, body: str) -> str:
    return " ".join(f"{subject} {body}".casefold().split())


def validate_records(records: list[dict]) -> list[dict]:
    if not isinstance(records, list) or not records:
        raise ValueError("Dataset must be a non-empty JSON array")
    ids, texts, groups = set(), set(), {}
    for index, row in enumerate(records):
        # Error messages deliberately omit email content.
        prefix = f"Record {index}"
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError(f"{prefix}: unexpected or missing fields")
        for field in ("id", "group_id", "subject", "body", "source", "split"):
            if not isinstance(row[field], str):
                raise ValueError(f"{prefix}: {field} must be a string")
        if not row["id"].strip() or not row["group_id"].strip():
            raise ValueError(f"{prefix}: empty identifier")
        text = normalize_text(row["subject"], row["body"])
        if not text:
            raise ValueError(f"{prefix}: empty message")
        if type(row["is_spam"]) is not bool:
            raise ValueError(f"{prefix}: is_spam must be a boolean")
        if row["source"] != "synthetic" or row["split"] not in SPLITS:
            raise ValueError(f"{prefix}: only synthetic source and known splits are allowed")
        if row["is_spam"]:
            if row["category"] is not None:
                raise ValueError(f"{prefix}: spam category must be null")
        elif row["category"] not in CATEGORIES:
            raise ValueError(f"{prefix}: invalid legitimate category")
        if row["id"] in ids or text in texts:
            raise ValueError(f"{prefix}: duplicate id or normalized message")
        if row["group_id"] in groups and groups[row["group_id"]] != row["split"]:
            raise ValueError(f"{prefix}: group crosses split boundary")
        ids.add(row["id"])
        texts.add(text)
        groups[row["group_id"]] = row["split"]
    for split in SPLITS:
        rows = [r for r in records if r["split"] == split]
        if {r["is_spam"] for r in rows} != {True, False}:
            raise ValueError(f"{split}: requires spam and legitimate messages")
        if {r["category"] for r in rows if not r["is_spam"]} != set(CATEGORIES):
            raise ValueError(f"{split}: requires every legitimate category")
    return records


def load_dataset(path: str | Path) -> list[dict]:
    return validate_records(json.loads(Path(path).read_text(encoding="utf-8")))
