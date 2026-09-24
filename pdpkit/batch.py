"""Run the pipeline over a spreadsheet of products.

Export your sheet as CSV (Google Sheets: File > Download > Comma-separated values) and run

    python pdp.py batch products.csv

The URL column is found by looking at the values, not the header, so any export works: the
column with the most product-page URLs in it wins. A name column ("product name", "product",
"name", "title") is used for the folder name when present. Rows without a URL are skipped.

One product per row, and one failure never stops the run: every row's outcome is printed and
written to batch_log.csv next to the input.
"""
from __future__ import annotations

import csv
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from . import config
from .scrape import short_error  # noqa: F401  (re-exported: batch reports the same short reasons)

log = logging.getLogger("pdpkit.batch")

URL_RE = re.compile(r"https?://[^\s,]+", re.I)
NAME_HEADERS = ("product name", "product", "name", "title", "item")
# tracking parameters that make one product URL look like ten
TRACKING_PREFIXES = ("utm_", "ttclid", "fbclid", "gclid", "gad_", "msclkid", "epik", "irclickid", "_pos", "_sid", "_ss")
# Research and social sources, never the product page we want. Marketplaces (Amazon, Etsy,
# AliExpress) are NOT here: a sheet often cites them as the product's source, and their pages
# carry the images we are after.
NON_STORE_HOSTS = ("pipiads.com", "instagram.com", "tiktok.com", "vm.tiktok.com", "facebook.com", "youtube.com",
                   "youtu.be", "google.com", "docs.google.com", "drive.google.com", "x.com", "twitter.com",
                   "pinterest.", "reddit.com", "linkedin.com", "myshopify.com/admin")


class RowError(RuntimeError):
    """An already-readable reason for a row's failure (not to be shortened again)."""


@dataclass
class Row:
    name: str
    url: str
    source_row: int


@dataclass
class Result:
    name: str
    url: str
    status: str = "pending"      # grabbed / uploaded / guided / failed / skipped
    folder: str = ""
    images: int = 0
    title: str = ""
    error: str = ""
    bytes: int = 0
    source_bytes: int = 0
    steps: list = field(default_factory=list)


def cli_size(manifest: list[dict]) -> str:
    from .cli import _size_line
    return _size_line(manifest)


def clean_url(url: str) -> str:
    """Drop tracking parameters and fragments; keep the rest of the query (?variant= matters)."""
    u = urlparse(url.strip().rstrip(").,;"))
    kept = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True)
            if not any(k.lower().startswith(p) for p in TRACKING_PREFIXES)]
    return urlunparse((u.scheme, u.netloc, u.path, u.params, urlencode(kept), ""))


def is_store_url(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    if not host or any(h in host for h in NON_STORE_HOSTS):
        return False
    return bool(urlparse(url).path.strip("/"))     # a bare domain is not a product page


def first_store_url(cell: str) -> str:
    """The first product-page URL in a cell (cells often hold several, or a URL plus notes)."""
    for raw in URL_RE.findall(cell or ""):
        url = clean_url(raw)
        if is_store_url(url):
            return url
    return ""


def read_rows(path: Path) -> tuple[list[Row], str]:
    """Rows with a usable product URL, plus a note on which columns were used."""
    with path.open(newline="", encoding="utf-8-sig") as f:
        table = [r for r in csv.reader(f)]
    if not table:
        raise SystemExit(f"{path} is empty")
    width = max(len(r) for r in table)
    table = [r + [""] * (width - len(r)) for r in table]

    # the URL column is the one with the most product-page URLs in it
    counts = [sum(1 for r in table if first_store_url(r[c])) for c in range(width)]
    url_col = max(range(width), key=lambda c: counts[c])
    if not counts[url_col]:
        raise SystemExit(f"no product URLs found in {path}. Export the sheet as CSV and check the column holding the "
                         "competitor product links (research links like pipiads / tiktok / instagram are ignored).")

    # the name column: a header match, else the nearest text column left of the URLs
    header = [h.strip().lower() for h in table[0]]
    name_col = next((i for i, h in enumerate(header) if h in NAME_HEADERS), None)
    if name_col is None:
        name_col = next((c for c in range(url_col - 1, -1, -1)
                         if sum(1 for r in table[1:] if r[c].strip() and not URL_RE.search(r[c])) >= counts[url_col] // 2), None)

    rows: list[Row] = []
    seen: set[str] = set()
    last_name = ""
    for i, r in enumerate(table, start=1):
        url = first_store_url(r[url_col])
        if not url or url in seen:
            continue
        seen.add(url)
        name = (r[name_col].strip() if name_col is not None else "")
        last_name = name or last_name          # continuation rows repeat the product with a blank name cell
        rows.append(Row(name=name or last_name, url=url, source_row=i))
    note = f"URL column {url_col + 1}" + (f", name column {name_col + 1}" if name_col is not None else ", no name column")
    return rows, note


def find_existing(url: str) -> Path | None:
    """The product folder already grabbed from this URL, if any (folders are named after the
    competitor's handle, so match on the stored source URL rather than on the row's name)."""
    import json
    root = config.OUTPUT_ROOT
    if not root.exists():
        return None
    target = clean_url(url).rstrip("/")
    for facts in root.glob("*/product_summary.json"):
        try:
            stored = json.loads(facts.read_text(encoding="utf-8")).get("url", "")
        except (ValueError, OSError):
            continue
        if clean_url(stored).rstrip("/") == target:
            return facts.parent
    return None


def process(rows: list[Row], *, do_guide: bool = False, do_upload: bool = False, all_images: bool | None = None,
            limit: int | None = None, skip_existing: bool = True, dry_run: bool = False,
            browser: bool | None = None) -> list[Result]:
    from . import scrape, summary

    results: list[Result] = []
    session = scrape.make_session()
    todo = rows[:limit] if limit else rows
    for i, row in enumerate(todo, 1):
        res = Result(name=row.name, url=row.url)
        print(f"\n[{i}/{len(todo)}] {row.name or row.url}")
        if dry_run:
            res.status = "dry-run"
            results.append(res)
            print(f"    would grab {row.url}")
            continue
        existing = find_existing(row.url)
        if skip_existing and existing:
            res.status, res.folder = "skipped", str(existing)
            results.append(res)
            print(f"    already grabbed -> {existing} (use --redo to grab it again)")
            continue
        try:
            # the folder is named from the sheet, so it is the name you recognise
            out_dir = config.product_dir(config.slugify(row.name)) if row.name else None
            try:
                data, out_dir, manifest = scrape.grab(row.url, out_dir=out_dir, session=session,
                                                      all_images=all_images, use_browser=browser)
            except Exception as first:  # noqa: BLE001 - a store that blocks plain requests (Amazon, Etsy) may still render
                if browser is not None:
                    raise
                print(f"    {short_error(first)}; retrying with the browser only")
                try:
                    data, out_dir, manifest = scrape.grab_via_browser(row.url, out_dir=out_dir, session=session, all_images=all_images)
                except Exception as second:  # noqa: BLE001
                    raise RowError(f"{short_error(first)}; browser retry: {short_error(second) if 'HTTP' in str(second) else str(second)[:120]}") from second
                res.steps.append("browser")
            summary.write_summary(data, out_dir, manifest)
            res.folder, res.images = str(out_dir), len(manifest)
            res.title = config.our_title(data.title, data.vendor, urlparse(data.url).netloc)
            res.bytes = sum(m.get("bytes", 0) for m in manifest)
            res.source_bytes = sum(m.get("source_bytes") or m.get("bytes", 0) for m in manifest)
            res.status = "grabbed"
            res.steps.append("grab")
            print(f"    {data.title}")
            gallery = sum(1 for m in manifest if m.get("kind") == "gallery")
            print(f"    {len(manifest)} images ({gallery} gallery) -> {out_dir / 'competitor_imgs'}  ({cli_size(manifest)})")
            if manifest and not gallery:
                print("    note: no separate product gallery detected; every image on the page is saved as page_NN")
        except Exception as e:  # noqa: BLE001 - one bad store must not stop the batch
            res.status, res.error = "failed", (str(e) if isinstance(e, RowError) else short_error(e))
            results.append(res)
            log.debug("grab failed for %s: %s", row.url, e)
            print(f"    FAILED: {res.error}")
            continue
        if do_upload:
            try:
                from . import shopify_admin
                folder = Path(res.folder) / config.generated_dir_name(res.title)
                if not folder.exists() or not any(p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") for p in folder.iterdir()):
                    print(f"    upload skipped: no images in {folder.name} yet")
                else:
                    up = shopify_admin.upload_folder(folder, title=res.title, vendor=config.BRAND_NAME)
                    res.status = "uploaded"
                    res.steps.append("upload")
                    print(f"    uploaded {len(up['uploaded'])} images -> {up['product']['id']}")
            except Exception as e:  # noqa: BLE001
                res.error = f"upload: {str(e)[:150]}"
                print(f"    upload FAILED: {res.error}")
        if do_guide:
            try:
                from . import guide as guide_mod
                template = Path(config.PDP_TEMPLATE)
                if not template.is_file():
                    print("    guide skipped: PDP_TEMPLATE not found")
                else:
                    pdf = guide_mod.build_guide(Path(res.folder), res.title, template)
                    res.steps.append("guide")
                    if res.status == "grabbed":
                        res.status = "guided"
                    print(f"    guide -> {pdf.name}")
            except Exception as e:  # noqa: BLE001
                res.error = f"guide: {str(e)[:150]}"
                print(f"    guide FAILED: {res.error}")
        results.append(res)
    return results


def write_log(results: list[Result], path: Path) -> Path:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["at", "name", "our_title", "url", "status", "images", "kb", "source_kb", "folder", "steps", "error"])
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for r in results:
            w.writerow([now, r.name, r.title, r.url, r.status, r.images, round(r.bytes / 1024),
                        round(r.source_bytes / 1024), r.folder, " ".join(r.steps), r.error])
    return path


def print_summary(results: list[Result]) -> None:
    by_status: dict[str, int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
    print("\n" + "-" * 60)
    print("  ".join(f"{k}: {v}" for k, v in sorted(by_status.items())))
    total, src = sum(r.bytes for r in results), sum(r.source_bytes for r in results)
    if src:
        print(f"images: {sum(r.images for r in results)}, {src / 1024 / 1024:.1f} MB downloaded -> "
              f"{total / 1024 / 1024:.1f} MB on disk ({round(100 * (1 - total / src))}% smaller)")
    failed = [r for r in results if r.status == "failed"]
    if failed:
        print("\nfailed rows (re-run them one at a time with `python pdp.py grab <url>`):")
        for r in failed:
            print(f"  {r.name or '(no name)'}: {r.url}\n      {r.error}")
