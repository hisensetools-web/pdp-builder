"""batch: column detection in a messy sheet export, URL cleaning, skip/failure handling."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pdpkit import batch, config

# shaped like the real export: research links (pipiads/tiktok/instagram) in one column, the
# competitor product URL in another, tracking parameters attached, continuation rows with a
# blank name, and checklist rows that hold no URL at all
MESSY = [
    ["Product Name", "Adspy", "Competition", "First Appearance Date", "Checklist", "Result"],
    ["Wicked Tumbler", "https://www.pipiads.com/product-search/68e977 https://vm.tiktok.com/ZN8My63PS/",
     "https://babies-amity.com/products/wicked-for-good-tumbler?ttclid=ABC&utm_campaign=x&utm_source=tiktok",
     "Oct 10", "Keyword search", "TRUE"],
    ["", "https://www.pipiads.com/product-search/68e9aa", "", "", "Image search", "TRUE"],
    ["", "", "https://shopeloria.com/products/wicked-for-good-free-sip-bottle", "", "Google image", "TRUE"],
    ["Vanity Pouch", "https://www.instagram.com/reel/Ddb7uPzx9gA/",
     "https://urbanglaam.com/products/vanity-chain-pouch?utm_source=tiktok&_pos=3&_sid=691f17e69", "", "", ""],
    ["Conclusion", "", "", "", "", ""],
    ["Dup", "", "https://urbanglaam.com/products/vanity-chain-pouch", "", "", ""],
]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    return path


class UrlTests(unittest.TestCase):
    def test_tracking_parameters_dropped_real_ones_kept(self):
        self.assertEqual(batch.clean_url("https://s.com/products/x?utm_source=tiktok&ttclid=Z&variant=42"),
                         "https://s.com/products/x?variant=42")
        self.assertEqual(batch.clean_url("https://s.com/products/x?_pos=3&_sid=ab&_ss=r"), "https://s.com/products/x")
        self.assertEqual(batch.clean_url("https://s.com/products/x#reviews)."), "https://s.com/products/x")

    def test_research_hosts_are_not_store_urls(self):
        for u in ("https://www.pipiads.com/product-search/68e9", "https://vm.tiktok.com/ZN8My63PS/",
                  "https://www.instagram.com/reel/Ddb7/", "https://shop.example.com"):
            self.assertFalse(batch.is_store_url(u), u)
        self.assertTrue(batch.is_store_url("https://babies-amity.com/products/wicked-for-good-tumbler"))
        self.assertTrue(batch.is_store_url("https://tykapryde.com/the-sol-light"))   # not a /products/ path

    def test_marketplaces_count_as_product_pages(self):
        # the sheet cites Amazon and Etsy as the product's source; those pages hold the images
        for u in ("https://www.amazon.com/Candle-Warmer-Dimmer/dp/B0GFPBVVLQ/ref=sr_1_2?keywords=skull",
                  "https://www.etsy.com/ie/listing/4360095387/ghostface-halloween-bling-mask?ref=sr_gallery-1-2",
                  "https://www.aliexpress.com/item/100500.html"):
            self.assertTrue(batch.is_store_url(u), u)

    def test_first_store_url_ignores_research_links_in_the_same_cell(self):
        cell = "https://www.pipiads.com/x https://babies-amity.com/products/t?utm_source=a  notes"
        self.assertEqual(batch.first_store_url(cell), "https://babies-amity.com/products/t")
        self.assertEqual(batch.first_store_url("no links here"), "")


class ReadRowsTests(unittest.TestCase):
    def test_picks_the_competition_column_and_carries_the_name_down(self):
        with tempfile.TemporaryDirectory() as d:
            rows, note = batch.read_rows(write_csv(Path(d) / "s.csv", MESSY))
        self.assertIn("URL column 3", note)
        self.assertIn("name column 1", note)
        urls = [r.url for r in rows]
        self.assertEqual(urls, ["https://babies-amity.com/products/wicked-for-good-tumbler",
                                "https://shopeloria.com/products/wicked-for-good-free-sip-bottle",
                                "https://urbanglaam.com/products/vanity-chain-pouch"])
        self.assertEqual(rows[1].name, "Wicked Tumbler")     # continuation row inherits the product name
        self.assertEqual(rows[2].name, "Vanity Pouch")
        self.assertEqual(len(urls), len(set(urls)))          # the duplicate row is dropped

    def test_shipped_example_csv_parses(self):
        rows, _ = batch.read_rows(config.PRODUCTS_EXAMPLE)
        self.assertGreaterEqual(len(rows), 5)
        self.assertTrue(all(r.url.startswith("https://") and r.name for r in rows))
        # the row with no competitor link yet is carried in the file but produces no work
        self.assertNotIn("B&BW x Nightmare Before Christmas Candle Holder", [r.name for r in rows])

    def test_a_sheet_without_product_urls_says_so(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_csv(Path(d) / "s.csv", [["Product", "Source"], ["Eyebrow tattoos", "FB"]])
            with self.assertRaises(SystemExit) as cm:
                batch.read_rows(path)
        self.assertIn("no product URLs", str(cm.exception))


class ProcessTests(unittest.TestCase):
    def setUp(self):
        self.rows = [batch.Row("A", "https://a.com/products/a", 1),
                     batch.Row("B", "https://b.com/products/b", 2),
                     batch.Row("C", "https://c.com/products/c", 3)]

    def test_one_failure_does_not_stop_the_batch(self):
        calls = []

        def fake_grab(url, session=None, all_images=False, use_browser=None, **kw):
            calls.append((url, use_browser))
            if "b.com" in url:
                raise RuntimeError("HTTP 403 from the store")
            data = mock.Mock(title="X Thing", vendor="X", url=url)
            return data, Path("/tmp/x"), [{"kind": "gallery"}, {"kind": "gallery"}]

        with mock.patch("pdpkit.scrape.grab", side_effect=fake_grab), \
             mock.patch("pdpkit.scrape.grab_via_browser", side_effect=RuntimeError("HTTP 503 from the store")) as via, \
             mock.patch("pdpkit.scrape.make_session"), mock.patch("pdpkit.summary.write_summary"), \
             mock.patch.object(batch, "find_existing", return_value=None):
            results = batch.process(self.rows)
        self.assertEqual([r.status for r in results], ["grabbed", "failed", "grabbed"])
        self.assertIn("403", results[1].error)                 # the original refusal is what gets reported
        self.assertIn("browser retry", results[1].error)
        self.assertEqual(results[0].images, 2)
        self.assertEqual(calls, [("https://a.com/products/a", None), ("https://b.com/products/b", None),
                                 ("https://c.com/products/c", None)])
        via.assert_called_once()                                # the failing row was retried browser-only

    def test_a_store_that_blocks_plain_requests_succeeds_on_the_browser_retry(self):
        calls = []

        def fake_grab(url, session=None, all_images=None, use_browser=None, **kw):
            calls.append("static")
            raise RuntimeError("HTTP 503 from the store")

        def fake_via_browser(url, out_dir=None, session=None, all_images=None):
            calls.append("browser")
            return mock.Mock(title="Amazon Thing", vendor="", url=url), Path("/tmp/x"), [{"kind": "gallery"}]

        with mock.patch("pdpkit.scrape.grab", side_effect=fake_grab), \
             mock.patch("pdpkit.scrape.grab_via_browser", side_effect=fake_via_browser), \
             mock.patch("pdpkit.scrape.make_session"), mock.patch("pdpkit.summary.write_summary"), \
             mock.patch.object(batch, "find_existing", return_value=None):
            results = batch.process(self.rows[:1])
        self.assertEqual(calls, ["static", "browser"])
        self.assertEqual(results[0].status, "grabbed")
        self.assertIn("browser", results[0].steps)

    def test_already_grabbed_rows_are_skipped_unless_redo(self):
        with mock.patch("pdpkit.scrape.make_session"), \
             mock.patch.object(batch, "find_existing", return_value=Path("/tmp/done")) as fe, \
             mock.patch("pdpkit.scrape.grab") as grab:
            results = batch.process(self.rows[:1])
            self.assertEqual(results[0].status, "skipped")
            grab.assert_not_called()
            fe.return_value = None
            with mock.patch("pdpkit.summary.write_summary"):
                grab.return_value = (mock.Mock(title="T", vendor="", url="u"), Path("/tmp/x"), [])
                results = batch.process(self.rows[:1], skip_existing=False)
        self.assertEqual(results[0].status, "grabbed")

    def test_limit_and_dry_run(self):
        with mock.patch("pdpkit.scrape.make_session"), mock.patch("pdpkit.scrape.grab") as grab:
            results = batch.process(self.rows, limit=2, dry_run=True)
        grab.assert_not_called()
        self.assertEqual([r.status for r in results], ["dry-run", "dry-run"])

    def test_find_existing_matches_on_stored_url(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "thing").mkdir()
            (root / "thing" / "product_summary.json").write_text(json.dumps({"url": "https://a.com/products/a?utm_source=x"}))
            with mock.patch.object(config, "OUTPUT_ROOT", root):
                self.assertEqual(batch.find_existing("https://a.com/products/a"), root / "thing")
                self.assertIsNone(batch.find_existing("https://a.com/products/other"))

    def test_short_error_keeps_the_readable_part(self):
        self.assertIn("connection refused", batch.short_error(RuntimeError(
            "GET http://x/y failed after 3 attempts: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries "
            "exceeded (Caused by NewConnectionError('Failed to establish a new connection: [Errno 111] Connection refused'))")))
        self.assertEqual(batch.short_error(RuntimeError("blocked: 403 Forbidden")), "HTTP 403 from the store")
        self.assertEqual(batch.short_error(RuntimeError("read timed out")), "timed out")
        self.assertIn("does not resolve", batch.short_error(RuntimeError("NameResolutionError: nope")))

    def test_log_written(self):
        results = [batch.Result("A", "https://a.com/products/a", status="grabbed", images=3, steps=["grab"])]
        with tempfile.TemporaryDirectory() as d:
            path = batch.write_log(results, Path(d) / "batch_log.csv")
            body = path.read_text()
        self.assertIn("https://a.com/products/a", body)
        self.assertIn("grabbed", body)


if __name__ == "__main__":
    unittest.main()
