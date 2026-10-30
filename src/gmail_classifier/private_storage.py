"""Local private files must stay outside the source checkout."""

import json
import os
from pathlib import Path


CHECKOUT = Path(__file__).resolve().parents[2]


def private_home() -> Path:
    base = Path(os.environ["LOCALAPPDATA"]) if os.environ.get("LOCALAPPDATA") else Path.home() / ".local/share"
    return base / "GmailEmailClassifier"


def private_path(path: str | Path) -> Path:
    path = Path(path).expanduser().resolve()
    if path == CHECKOUT or CHECKOUT in path.parents:
        raise ValueError("Private files must be outside the source checkout")
    # Also reject another Git checkout chosen as an output location.
    if any((parent / ".git").exists() for parent in path.parents):
        raise ValueError("Private files must be outside Git worktrees")
    return path


def write_private_json(path: str | Path, data, *, overwrite=False) -> Path:
    path = private_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects previous collections from accidental replacement.
    flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if overwrite else os.O_EXCL)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
    return path
