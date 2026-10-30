import copy
import json
import re
import threading
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest

from gmail_classifier.review_ui import load_collection, make_server, page, progress, save_review


@pytest.fixture
def collection(records):
    rows = copy.deepcopy(records)
    for row in rows:
        row.update(source="gmail_reviewed", human_reviewed=False, privacy_reviewed=False,
                   exclude=False, is_spam=None, category=None, split=None)
    return {"format_version": 1, "source": "gmail_reviewed", "records": rows}


def form_for(row, **changes):
    form = {"subject": row["subject"], "body": row["body"], "label": "Financeiro",
            "group_id": row["group_id"], "split": "train", "human_reviewed": "on",
            "privacy_reviewed": "on"}
    form.update(changes)
    return form


def test_save_preserves_original_backup_and_rejects_stale_form(tmp_path, collection):
    path = tmp_path / "review.json"
    path.write_text(json.dumps(collection), encoding="utf-8")
    _, revision = load_collection(path)
    saved = save_review(path, revision, 0, form_for(collection["records"][0]))
    assert saved["records"][0]["human_reviewed"] is True
    assert saved["records"][0]["category"] == "Financeiro"
    assert json.loads((tmp_path / "review.before-review.json").read_text(encoding="utf-8")) == collection
    with pytest.raises(ValueError, match="outra janela"):
        save_review(path, revision, 0, form_for(collection["records"][0]))
    assert json.loads(path.read_text(encoding="utf-8")) == saved


def test_group_moves_and_split_assignment_keep_threads_together(tmp_path, collection):
    rows = collection["records"]
    rows[1]["group_id"] = rows[0]["group_id"]
    merged = rows[2]["group_id"]
    path = tmp_path / "review.json"
    path.write_text(json.dumps(collection), encoding="utf-8")
    _, revision = load_collection(path)
    saved = save_review(path, revision, 0, form_for(rows[0], group_id=merged, split="test"))
    assert {r["group_id"] for r in saved["records"][:3]} == {merged}
    assert {r["split"] for r in saved["records"][:3]} == {"test"}
    assert saved["records"][1]["human_reviewed"] is False


def test_missing_labels_are_never_confirmed_automatically(tmp_path, collection):
    path = tmp_path / "review.json"
    path.write_text(json.dumps(collection), encoding="utf-8")
    _, revision = load_collection(path)
    with pytest.raises(ValueError, match="classificação"):
        save_review(path, revision, 0, form_for(collection["records"][0], label=""))
    assert progress(collection)["pending"] == 80
    assert progress(collection)["ready"] is False
    excluded = save_review(path, revision, 0, form_for(collection["records"][0],
                           exclude="on", label="", human_reviewed="", privacy_reviewed=""))
    assert progress(excluded)["excluded"] == 1
    assert progress(excluded)["reviewed"] == 0


def test_page_escapes_untrusted_email_markup(collection):
    collection["records"][0]["body"] = '</textarea><script>alert("private")</script>'
    rendered = page(collection, "revision", 0, "csrf")
    assert "<script>" not in rendered
    assert "&lt;/textarea&gt;" in rendered
    assert "https://" not in rendered  # No external assets or links.


def test_progress_validates_labels_splits_and_coverage(collection, records):
    for current, original in zip(collection["records"], records):
        current.update(original)
        current.update(source="gmail_reviewed", human_reviewed=True, privacy_reviewed=True)
    assert progress(collection)["ready"] is True
    collection["records"][-1]["group_id"] = collection["records"][0]["group_id"]
    assert progress(collection)["ready"] is False


def test_http_form_requires_origin_csrf_and_valid_host(tmp_path, collection):
    path = tmp_path / "review.json"
    path.write_text(json.dumps(collection), encoding="utf-8")
    with make_server(path) as server:
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        origin = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(origin, timeout=3) as response:
                rendered = response.read().decode()
                assert response.headers["Cache-Control"] == "no-store"
                assert "default-src 'none'" in response.headers["Content-Security-Policy"]
            csrf = re.search(r'name="csrf" value="([^"]+)"', rendered).group(1)
            _, revision = load_collection(path)
            form = {**form_for(collection["records"][0]), "index": "0", "revision": revision, "csrf": csrf}
            for supplied_origin, supplied_csrf in [("https://evil.invalid", csrf), (origin, "wrong")]:
                request = Request(origin + "/save", data=urlencode({**form, "csrf": supplied_csrf}).encode(),
                                  headers={"Origin": supplied_origin})
                with pytest.raises(HTTPError) as error:
                    urlopen(request, timeout=3)
                assert error.value.code == 403
            with pytest.raises(HTTPError) as error:
                urlopen(Request(origin, headers={"Host": "evil.invalid"}), timeout=3)
            assert error.value.code == 403
            assert load_collection(path)[0] == collection
            with urlopen(Request(origin + "/save", data=urlencode(form).encode(),
                                 headers={"Origin": origin}), timeout=3) as response:
                assert response.status == 200  # Follows POST/redirect/GET.
            assert load_collection(path)[0]["records"][0]["category"] == "Financeiro"
            with urlopen(origin + "/status", timeout=3) as response:
                stats = json.load(response)
                assert stats["reviewed"] == 1
                assert "records" not in stats
        finally:
            server.shutdown()
            worker.join(timeout=3)
