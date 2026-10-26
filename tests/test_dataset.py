import pytest

from gmail_classifier.dataset import CATEGORIES, validate_records


def test_distribution(records):
    assert len(records) == 80
    assert {r["category"] for r in records if not r["is_spam"]} == set(CATEGORIES)


@pytest.mark.parametrize("field,value", [
    ("is_spam", 1), ("is_spam", "false"), ("category", "unknown"),
    ("subject", None), ("source", "gmail"), ("split", "unknown"), ("id", " "),
])
def test_bad_fields(records, field, value):
    records[0][field] = value
    with pytest.raises(ValueError):
        validate_records(records)


@pytest.mark.parametrize("change", ["id", "text", "group", "empty", "spam_category", "extra", "missing", "coverage"])
def test_integrity(records, change):
    if change == "id":
        records[-1]["id"] = records[0]["id"]
    elif change == "text":
        records[-1].update(subject=records[0]["subject"].upper(), body="  " + records[0]["body"])
    elif change == "group":
        records[-1]["group_id"] = records[0]["group_id"]
    elif change == "empty":
        records[0].update(subject=" ", body="\n")
    elif change == "spam_category":
        records[-1]["category"] = "Financeiro"
    elif change == "extra":
        records[0]["sender"] = "private"
    elif change == "missing":
        del records[0]["group_id"]
    else:
        records[:] = [r for r in records if not (r["split"] == "test" and r["category"] == "RH")]
    with pytest.raises(ValueError):
        validate_records(records)


@pytest.mark.parametrize("value", [[], {}, None])
def test_invalid_container(value):
    with pytest.raises(ValueError):
        validate_records(value)
