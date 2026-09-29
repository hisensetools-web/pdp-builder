"""ClickUp as the queue: tasks in 'ready to build' become rows, links from the field + description,
done tasks skipped, write-back ticks the box and comments, rate limits retried."""
import json
import unittest
from unittest import mock

from pdpkit import batch, clickup, config

URL_FIELD = {"id": "f-url", "name": "Main Competitor", "type": "url"}
DONE_FIELD = {"id": "f-done", "name": "z-imagesPulled", "type": "checkbox"}


def task(id_, name, url=None, done=None, text=""):
    return {"id": id_, "name": name, "url": f"https://app.clickup.com/t/{id_}", "status": {"status": "ready to build"},
            "text_content": text,
            "custom_fields": [dict(URL_FIELD, value=url), dict(DONE_FIELD, value=done)]}


class FakeResponse:
    def __init__(self, status, body=None, headers=None):
        self.status_code, self._body, self.headers = status, body, headers or {}
        self.content = json.dumps(body).encode() if body is not None else b""

    def json(self):
        return self._body


class FakeSession:
    """Answers GET /list/x/task with pages, records every POST."""
    def __init__(self, tasks, fields=(URL_FIELD, DONE_FIELD), fail_first=0):
        self.tasks, self.fields, self.fail_first = tasks, list(fields), fail_first
        self.headers = {}
        self.calls = []

    def request(self, method, url, params=None, json=None, timeout=None):
        self.calls.append((method, url.replace(clickup.API, ""), params, json))
        if self.fail_first:
            self.fail_first -= 1
            return FakeResponse(429, {"err": "rate"}, {"Retry-After": "0"})
        if method == "GET" and url.endswith("/task"):
            assert params["statuses[]"] == [getattr(self, "expect_status", "ready for lp")]
            return FakeResponse(200, {"tasks": self.tasks, "last_page": True})
        if method == "GET" and url.endswith("/list/901222590753") or (method == "GET" and url.rstrip("/").endswith("/list/L")):
            return FakeResponse(200, {"id": "L", "name": "Product Research",
                                      "statuses": [{"status": st} for st in getattr(self, "statuses", ["researching", "ready for lp", "lp ready", "testing"])]})
        if method == "GET" and url.endswith("/field"):
            return FakeResponse(200, {"fields": self.fields})
        if method == "GET" and "/task/" in url:
            tid = url.rsplit("/", 1)[-1]
            return FakeResponse(200, {"id": tid, "text_content": "see https://store.com/products/from-full-task"})
        if method == "POST":
            return FakeResponse(200, {})
        return FakeResponse(404, {"err": "nope"})


class RowsTests(unittest.TestCase):
    def client(self, tasks, **kw):
        s = FakeSession(tasks, **kw)
        return clickup.ClickUp(token="pk_test", session=s), s

    def test_ready_to_build_tasks_become_rows_with_every_product_link(self):
        c, _ = self.client([
            task("t1", "Skull Candle Warmer", url="https://www.amazon.com/Candle-Warmer/dp/B0GFPBVVLQ/ref=sr_1_2?th=1",
                 text="Competition: https://www.amazon.com/Candle-Warmer/dp/B0GFPBVVLQ/ Adspy https://vm.tiktok.com/ZN8MHQG7m/"),
            task("t2", "Sol Study Light", url="https://bibikstore.ru/rassvet-zakat1",
                 text="second colour https://bibikstore.ru/polnoch1"),
            task("t3", "Avengers Popcorn", url="https://www.tiktok.com/@cineworld/video/768", text="watch list"),
            task("t4", "Done Thing", url="https://done.com/products/x", done="true"),
        ])
        rows, note = clickup.product_rows(c)
        self.assertEqual([r.name for r in rows], ["Skull Candle Warmer", "Sol Study Light"])
        self.assertEqual(rows[0].urls, ["https://www.amazon.com/dp/B0GFPBVVLQ"])           # field + description = one link
        self.assertEqual(rows[1].urls, ["https://bibikstore.ru/rassvet-zakat1", "https://bibikstore.ru/polnoch1"])
        self.assertEqual(rows[0].task_id, "t1")
        self.assertIn("1 already pulled", note)
        self.assertIn("no product link on: Avengers Popcorn", note)

    def test_redo_includes_done_tasks(self):
        c, _ = self.client([task("t4", "Done Thing", url="https://done.com/products/x", done=True)])
        rows, _ = clickup.product_rows(c, include_done=True)
        self.assertEqual([r.name for r in rows], ["Done Thing"])

    def test_description_fetched_when_the_list_call_omits_it(self):
        t = task("t5", "Lamp", url=None)
        del t["text_content"]
        c, s = self.client([t])
        rows, _ = clickup.product_rows(c)
        self.assertEqual(rows[0].url, "https://store.com/products/from-full-task")
        self.assertTrue(any(call[1] == "/task/t5" for call in s.calls))

    def test_rate_limit_is_retried(self):
        c, s = self.client([task("t1", "X", url="https://x.com/products/x")], fail_first=2)
        with mock.patch("pdpkit.clickup.time.sleep"):
            rows, _ = clickup.product_rows(c)
        self.assertEqual(len(rows), 1)

    def test_bad_token_is_explained(self):
        s = FakeSession([])
        s.request = lambda *a, **k: FakeResponse(401, {"err": "Token invalid"})
        c = clickup.ClickUp(token="pk_bad", session=s)
        with self.assertRaises(clickup.ClickUpError) as cm:
            clickup.product_rows(c)
        self.assertIn("token", str(cm.exception).lower())

    def test_missing_token_is_explained(self):
        with mock.patch.object(config, "CLICKUP_TOKEN", ""), self.assertRaises(clickup.ClickUpError):
            clickup.ClickUp(token="")


class WriteBackTests(unittest.TestCase):
    def test_done_ticks_the_box_and_comments(self):
        s = FakeSession([])
        c = clickup.ClickUp(token="pk_test", session=s)
        row = batch.Row("Skull Candle Warmer", "https://www.amazon.com/dp/B0GFPBVVLQ", 0, task_id="t1")
        note = clickup.mark_done(c, row, r"C:\tt\pdp_output\skull-candle-warmer", 14, comment=True)
        posts = [(u, j) for m, u, p, j in s.calls if m == "POST"]
        self.assertEqual(posts[0], ("/task/t1/field/f-done", {"value": True}))
        self.assertEqual(posts[1][0], "/task/t1/comment")
        self.assertIn("14 file(s)", posts[1][1]["comment_text"])
        self.assertIn("skull-candle-warmer", posts[1][1]["comment_text"])
        self.assertIn("ticked", note)
        self.assertIn("comment posted", note)

    def test_missing_checkbox_field_is_a_hint_not_a_failure(self):
        s = FakeSession([], fields=(URL_FIELD,))
        c = clickup.ClickUp(token="pk_test", session=s)
        note = clickup.mark_done(c, batch.Row("X", "https://x.com/products/x", 0, task_id="t1"), "/tmp/x", 3, comment=False)
        self.assertIn("add one", note)
        self.assertFalse(any(m == "POST" for m, *_ in s.calls))

    def test_rows_without_a_task_are_left_alone(self):
        s = FakeSession([])
        c = clickup.ClickUp(token="pk_test", session=s)
        self.assertEqual(clickup.mark_done(c, batch.Row("X", "https://x.com/products/x", 0), "/tmp/x", 3), "")
        self.assertEqual(s.calls, [])


class ProcessHookTests(unittest.TestCase):
    def test_after_is_called_for_grabbed_and_already_grabbed_rows_only(self):
        from pathlib import Path
        seen = []

        def fake_grab(url, out_dir=None, session=None, all_images=None, use_browser=None, append=False):
            if "bad" in url:
                raise RuntimeError("HTTP 404 from the store")
            return mock.Mock(title="T", vendor="", url=url), Path("/tmp/x"), [{"kind": "gallery"}]

        rows = [batch.Row("A", "https://a.com/products/a", 0, task_id="ta"),
                batch.Row("B", "https://b.com/products/bad", 0, task_id="tb"),
                batch.Row("C", "https://c.com/products/c", 0, task_id="tc")]
        with mock.patch("pdpkit.scrape.grab", side_effect=fake_grab), mock.patch("pdpkit.scrape.make_session"), \
             mock.patch("pdpkit.summary.write_summary"), mock.patch.object(batch, "record_source"), \
             mock.patch.object(batch, "find_existing", side_effect=lambda u: Path("/tmp/done") if "c.com" in u else None):
            results = batch.process(rows, browser=False, after=lambda row, res: seen.append((row.task_id, res.status)) or "ticked")
        self.assertEqual(seen, [("ta", "grabbed"), ("tc", "skipped")])
        self.assertEqual([r.status for r in results], ["grabbed", "failed", "skipped"])
        self.assertIn("clickup", results[0].steps)


if __name__ == "__main__":
    unittest.main()


class RenamedFieldTests(unittest.TestCase):
    def test_a_renamed_competitor_field_is_still_found(self):
        t = task("t1", "Lamp")
        t["custom_fields"] = [{"id": "f-url", "name": "Competition URL's (old name)", "type": "url", "value": "https://s.com/products/lamp"}]
        s = FakeSession([t])
        rows, _ = clickup.product_rows(clickup.ClickUp(token="pk_test", session=s))
        self.assertEqual(rows[0].url, "https://s.com/products/lamp")

    def test_empty_done_field_means_no_checkbox_at_all(self):
        s = FakeSession([])
        c = clickup.ClickUp(token="pk_test", session=s)
        note = clickup.mark_done(c, batch.Row("X", "https://x.com/products/x", 0, task_id="t1"), "/tmp/x", 3, done_field="", comment=True)
        posts = [u for m, u, p, j in s.calls if m == "POST"]
        self.assertEqual(posts, ["/task/t1/comment"])
        self.assertNotIn("checkbox", note)


class NoTokenTests(unittest.TestCase):
    def test_batch_without_a_key_stops_instead_of_reading_the_sheet(self):
        from pdpkit import cli
        with mock.patch.object(config, "CLICKUP_TOKEN", ""), mock.patch.object(config, "SOURCE", "clickup"), \
             mock.patch.object(cli, "_self_update", return_value=False), \
             mock.patch("pdpkit.batch.fetch_sheet") as sheet, self.assertRaises(SystemExit) as cm:
            cli.main(["batch", "--dry-run"])
        self.assertIn("ClickUp key is missing", str(cm.exception))
        sheet.assert_not_called()


class StatusRenameTests(unittest.TestCase):
    def test_renamed_column_is_found_through_the_aliases(self):
        s = FakeSession([task("t1", "Lamp", url="https://s.com/products/lamp")])
        s.statuses = ["researching", "ready for lp", "lp ready", "testing"]
        c = clickup.ClickUp(token="pk_test", session=s)
        real, note = clickup.resolve_status(c, "L", "ready to build")      # the old configured name
        self.assertEqual(real, "ready for lp")
        self.assertIn("does not exist", note)
        rows, _ = clickup.product_rows(c, list_id="L", status="ready to build")
        self.assertEqual([r.name for r in rows], ["Lamp"])

    def test_case_and_spacing_do_not_matter(self):
        s = FakeSession([]); s.statuses = ["Ready For LP", "testing"]
        c = clickup.ClickUp(token="pk_test", session=s)
        self.assertEqual(clickup.resolve_status(c, "L", "ready for lp"), ("Ready For LP", ""))

    def test_unknown_status_lists_the_real_ones(self):
        s = FakeSession([]); s.statuses = ["idea", "building", "live"]
        c = clickup.ClickUp(token="pk_test", session=s)
        with self.assertRaises(clickup.ClickUpError) as cm:
            clickup.resolve_status(c, "L", "ready for lp")
        self.assertIn("idea, building, live", str(cm.exception))
