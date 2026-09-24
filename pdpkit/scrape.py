"""Fetch a competitor product page, find every image on it, download them, and
pull the structured facts (title, price, variants, copy, reviews) that feed
product_summary.

Shopify stores get the best data: /products/<handle>.json gives the gallery in
original resolution plus variants and the description. Everything else falls
back to HTML parsing (og:image, JSON-LD, <img>/<source>/lazy-load attributes),
and, when the page is JavaScript-rendered, a headless Chromium pass.
"""
from __future__ import annotations

import hashlib
import json
import logging
import mimetypes
import re
import time
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from . import config, images

log = logging.getLogger("pdpkit.scrape")

HTML_HEADERS = {
    "User-Agent": config.USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".avif")
SKIP_URL_WORDS = (
    "logo", "icon", "favicon", "payment", "badge", "flag", "sprite", "pixel", "star",
    "trustpilot", "klarna", "paypal", "visa", "mastercard", "amex", "applepay", "gpay",
    "loading", "spinner", "placeholder", "blank", "1x1", "tracking", "facebook.com/tr",
    "stamped", "judge.me", "loox", "yotpo", "emoji", "svg",
)
# Shopify CDN size / crop suffixes: name_600x600.jpg, name_1024x.jpg, name_600x600_crop_center.jpg, name@2x.jpg
_SHOPIFY_SIZE = re.compile(r"_(?:\d+x\d*|x\d+)(?:_crop_[a-z]+)?(?:@\dx)?(?=\.[a-z]{3,4}(?:\?|$))", re.I)
# containers whose images are the product's own gallery / scroller
GALLERY_HINT = re.compile(r"(product[-_ ]?(media|gallery|image|images|photo|photos|slider|carousel)|media[-_ ]?gallery"
                          r"|gallery|carousel|slider|swiper|splide|flickity|glide|keen-slider|thumbnail"
                          r"|t-slds|t-store__prod|tn-atom|js-product|main[-_ ]?image|photo[-_ ]?main|zoom)", re.I)
# ... unless they are one of these, which are other products or page furniture
GALLERY_EXCLUDE = re.compile(r"(related|recommend|upsell|cross[-_ ]?sell|also[-_ ]?(like|bought)|you[-_ ]?may"
                             r"|similar|recently[-_ ]?viewed|complete[-_ ]?the|bundle[-_ ]?with|testimonial|review"
                             r"|footer|site[-_ ]?header|navigation|announcement|logo|press|badge)", re.I)

# every attribute a store or page builder may hide the real image behind
LAZY_ATTRS = ("data-src", "data-original", "data-lazy", "data-zoom", "data-image", "data-large_image", "data-large",
              "data-full", "data-bg", "data-background", "data-background-image", "data-bgset", "data-thumb",
              "data-srcset", "data-lazy-srcset", "data-retina", "content")
IMG_ATTRS = ("src", "srcset") + LAZY_ATTRS

_SHOPIFY_CDN = re.compile(r"https?://[^\s\"'<>]+?/cdn/shop/(?:files|products)/[^\s\"'<>)]+?\.(?:jpe?g|png|webp|avif)", re.I)
_CDN_SHOPIFY = re.compile(r"https?://cdn\.shopify\.com/s/files/[^\s\"'<>)]+?\.(?:jpe?g|png|webp|avif)", re.I)
# any absolute image URL, including the escaped \/ form used inside embedded JSON
# backslashes stay inside the class: an embedded JSON string writes the path as a\/b\/c.jpg
_ANY_IMAGE_URL = re.compile(r"https?:\\?/\\?/[^\s\"'<>)]+?\.(?:jpe?g|png|webp|avif)", re.I)


@dataclass
class ImageRef:
    url: str
    alt: str = ""
    kind: str = "page"      # "gallery" (product photos) or "page" (everything else on the PDP)
    order: int = 0


@dataclass
class PageData:
    url: str
    platform: str = "unknown"
    title: str = ""
    handle: str = ""
    vendor: str = ""
    product_type: str = ""
    price: str = ""
    compare_at_price: str = ""
    currency: str = ""
    description_html: str = ""
    description_text: str = ""
    options: list = field(default_factory=list)      # [{name, values}]
    variants: list = field(default_factory=list)     # [{title, price, compare_at_price, available, sku}]
    tags: list = field(default_factory=list)
    meta_description: str = ""
    headings: list = field(default_factory=list)
    bullets: list = field(default_factory=list)
    faqs: list = field(default_factory=list)         # [{q, a}]
    rating: str = ""
    review_count: str = ""
    review_snippets: list = field(default_factory=list)
    trust_lines: list = field(default_factory=list)  # shipping / guarantee / returns mentions
    cta_texts: list = field(default_factory=list)
    body_text: str = ""
    images: list = field(default_factory=list)       # [ImageRef]

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["images"] = [i.__dict__ for i in self.images]
        return d


# --------------------------------------------------------------------------- fetch
def short_error(e: Exception) -> str:
    """The part of a network traceback worth reading: 'connection refused', 'HTTP 403', a timeout."""
    text = " ".join(str(e).split())
    for pattern, msg in (("Connection refused", "connection refused (store unreachable)"),
                         ("Name or service not known", "domain does not resolve"),
                         ("getaddrinfo failed", "domain does not resolve"),
                         ("NameResolutionError", "domain does not resolve"),
                         ("timed out", "timed out"), ("SSLError", "TLS/certificate error"),
                         ("CertificateError", "TLS/certificate error")):
        if pattern.lower() in text.lower():
            return msg
    import re as _re
    m = _re.search(r"\b([45]\d\d)\b", text)
    if m:
        return f"HTTP {m.group(1)} from the store"
    return text[:160]


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HTML_HEADERS)
    return s


def _get(session: requests.Session, url: str, **kw) -> requests.Response:
    last = None
    for attempt in range(config.REQUEST_RETRIES):
        try:
            r = session.get(url, timeout=config.REQUEST_TIMEOUT, allow_redirects=True, **kw)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"{r.status_code} for {url}", response=r)
            return r
        except (requests.RequestException, requests.HTTPError) as e:
            last = e
            wait = 2 ** attempt
            log.warning("GET %s: %s; retry in %ss", url, short_error(e), wait)
            time.sleep(wait)
    raise RuntimeError(f"GET {url} failed after {config.REQUEST_RETRIES} attempts: {last}")


def fetch_html(session: requests.Session, url: str) -> str:
    r = _get(session, url)
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code} from the store for {url}")
    return r.text


def render_html(url: str, wait_ms: int = 4000) -> str:
    """Headless Chromium render for JS-heavy pages; scrolls to trigger lazy-loading."""
    try:
        from playwright.sync_api import sync_playwright  # imported lazily: optional dependency at runtime
    except ImportError as e:
        raise RuntimeError("this store needs a browser, and Playwright is not installed: "
                           "python -m pip install playwright && python -m playwright install chromium") from e

    with sync_playwright() as p:
        kw = {"headless": True}
        if config.CHROMIUM_PATH:
            kw["executable_path"] = config.CHROMIUM_PATH
        try:
            browser = p.chromium.launch(**kw)
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"cannot start Chromium ({str(e).splitlines()[0][:120]}); "
                               "run: python -m playwright install chromium") from e
        page = browser.new_page(user_agent=config.USER_AGENT, viewport={"width": 1366, "height": 900})
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(wait_ms)
        height = page.evaluate("document.body.scrollHeight")
        y = 0
        while y < height and y < 30000:
            y += 700
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(350)
            height = page.evaluate("document.body.scrollHeight")
        # carousels only render the visible slide: force every lazy image to load and scroll
        # each horizontally scrollable strip to its end
        page.evaluate("""() => {
            document.querySelectorAll('img').forEach(i => {
                i.loading = 'eager';
                for (const a of ['data-src','data-original','data-lazy','data-large_image','data-full']) {
                    const v = i.getAttribute(a);
                    if (v && !i.src.includes(v)) i.setAttribute('src', v);
                }
            });
            document.querySelectorAll('*').forEach(el => {
                if (el.scrollWidth > el.clientWidth + 40) el.scrollLeft = el.scrollWidth;
            });
        }""")
        page.wait_for_timeout(2500)
        page.evaluate("() => document.querySelectorAll('*').forEach(el => { if (el.scrollWidth > el.clientWidth + 40) el.scrollLeft = 0; })")
        page.wait_for_timeout(1200)
        html = page.content()
        browser.close()
    return html


# --------------------------------------------------------------------------- shopify json
def shopify_product_url(url: str) -> str | None:
    """https://x.com/products/foo?variant=1 -> https://x.com/products/foo.json (None if not a product URL)."""
    u = urlparse(url)
    m = re.search(r"(/products/[^/?#]+)", u.path)
    if not m:
        return None
    path = m.group(1)
    if path.endswith(".json") or path.endswith(".js"):
        path = re.sub(r"\.(json|js)$", "", path)
    # keep a /collections/x prefix out: /products/<handle>.json works at the root
    return urlunparse((u.scheme, u.netloc, path + ".json", "", "", ""))


def fetch_shopify_product(session: requests.Session, url: str) -> dict | None:
    pj = shopify_product_url(url)
    if not pj:
        return None
    try:
        r = _get(session, pj, headers={"Accept": "application/json"})
    except RuntimeError:
        return None
    if r.status_code != 200 or "json" not in r.headers.get("content-type", ""):
        return None
    try:
        data = r.json()
    except ValueError:
        return None
    return data.get("product") if isinstance(data, dict) else None


_HANDLE_RE = re.compile(r"/products/([a-z0-9][a-z0-9\-_%]{1,120})(?=[\"'?#/\s\\]|$)", re.I)
_NOT_A_HANDLE = {"all", "index", "json", "search"}


def find_product_handle(html: str) -> str | None:
    """The Shopify product a landing page is built around.

    Landing pages like /the-sol-light have no product JSON of their own, but they link to the
    real product. The canonical URL or og:url is the strongest signal; otherwise the handle
    referenced most often across the page wins."""
    soup = BeautifulSoup(html, "html.parser")
    strong = []
    canonical = soup.find("link", rel=lambda v: v and "canonical" in (v if isinstance(v, list) else [v]))
    if canonical and canonical.get("href"):
        strong.append(canonical["href"])
    og = soup.find("meta", attrs={"property": "og:url"})
    if og and og.get("content"):
        strong.append(og["content"])
    for value in strong:
        m = _HANDLE_RE.search(value)
        if m and m.group(1).lower() not in _NOT_A_HANDLE:
            return m.group(1)

    counts: dict[str, int] = {}
    for m in _HANDLE_RE.finditer(html):
        handle = m.group(1)
        if handle.lower() in _NOT_A_HANDLE or handle.endswith((".js", ".json", ".css")):
            continue
        counts[handle] = counts.get(handle, 0) + 1
    if not counts:
        return None
    return max(counts, key=lambda h: (counts[h], -len(h)))


_PRODUCT_ID_RE = re.compile(r'"product"\s*:\s*\{[^{}]*?"id"\s*:\s*"?(\d{6,})', re.I)
_VARIANT_ID_RE = re.compile(r'name=["\']id["\'][^>]*value=["\'](\d{6,})|"variants?"\s*:\s*\[?\s*\{[^{}]*?"id"\s*:\s*"?(\d{6,})', re.I)


def page_product_ids(html: str) -> tuple[set[str], set[str]]:
    """Shopify product ids and variant ids mentioned anywhere on the page.
    A landing page with a direct add-to-cart form carries the variant id even when it never
    links to /products/<handle>."""
    products = set(_PRODUCT_ID_RE.findall(html))
    variants = {g for m in _VARIANT_ID_RE.findall(html) for g in m if g}
    return products, variants


def _title_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 2}


def find_product_in_catalogue(session: requests.Session, base_url: str, html: str, page_title: str = "",
                              max_pages: int = 3) -> dict | None:
    """Last resort for a landing page: read the store's own catalogue and pick the product this
    page sells, matched on product id, then variant id, then title overlap."""
    origin = "{0.scheme}://{0.netloc}".format(urlparse(base_url))
    product_ids, variant_ids = page_product_ids(html)
    want = _title_words(page_title)
    best, best_score = None, 0.0
    for page in range(1, max_pages + 1):
        try:
            r = _get(session, f"{origin}/products.json", params={"limit": 250, "page": page},
                     headers={"Accept": "application/json"})
        except RuntimeError:
            return best
        if r.status_code != 200 or "json" not in r.headers.get("content-type", ""):
            return best
        try:
            items = (r.json() or {}).get("products") or []
        except ValueError:
            return best
        if not items:
            break
        for prod in items:
            if str(prod.get("id")) in product_ids:
                return prod
            if variant_ids and {str(v.get("id")) for v in prod.get("variants") or []} & variant_ids:
                return prod
            if want:
                have = _title_words(prod.get("title", ""))
                overlap = len(want & have) / len(want)
                if overlap > best_score and overlap >= 0.6:
                    best, best_score = prod, overlap
    return best


def fetch_product_by_handle(session: requests.Session, base_url: str, handle: str) -> dict | None:
    origin = "{0.scheme}://{0.netloc}".format(urlparse(base_url))
    try:
        r = _get(session, f"{origin}/products/{handle}.json", headers={"Accept": "application/json"})
    except RuntimeError:
        return None
    if r.status_code != 200 or "json" not in r.headers.get("content-type", ""):
        return None
    try:
        return (r.json() or {}).get("product")
    except ValueError:
        return None


# --------------------------------------------------------------------------- image urls
def normalise_image_url(url: str, base: str) -> str:
    url = unescape(url.strip())
    if url.startswith("//"):
        url = "https:" + url
    url = urljoin(base, url)
    u = urlparse(url)
    path = _SHOPIFY_SIZE.sub("", u.path)
    # drop query (v=, width=) except for CDNs that need it; Shopify's ?v= is a cache-buster
    return urlunparse((u.scheme, u.netloc, path, "", "", ""))


def _is_image_url(url: str) -> bool:
    low = url.lower().split("?", 1)[0]
    if not low.endswith(IMAGE_EXT):
        return False
    return not any(w in low for w in SKIP_URL_WORDS)


def _srcset_urls(value: str) -> list[str]:
    out = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        out.append(part.split()[0])
    return out


def in_gallery_container(tag, depth: int = 6) -> bool:
    """True when an <img> sits inside the product's own gallery / scroller, judged by the
    class and id of its ancestors. Related-product carousels and page furniture do not count."""
    node = tag
    hit = False
    for _ in range(depth):
        node = getattr(node, "parent", None)
        if node is None or not getattr(node, "get", None):
            break
        marker = " ".join(filter(None, [" ".join(node.get("class") or []), node.get("id") or "",
                                        node.get("data-section-type") or ""]))
        if not marker:
            continue
        if GALLERY_EXCLUDE.search(marker):
            return False              # the nearest meaningful ancestor wins
        if GALLERY_HINT.search(marker):
            hit = True
    return hit


def extract_image_refs(html: str, base: str, product_json: dict | None = None) -> list[ImageRef]:
    """Every distinct product-ish image on the page. Gallery first (from Shopify JSON
    when available, otherwise og:image + JSON-LD), then page images in document order."""
    seen: dict[str, ImageRef] = {}
    order = 0

    def add(url: str, alt: str = "", kind: str = "page"):
        nonlocal order
        if not url or url.startswith("data:"):
            return
        norm = normalise_image_url(url, base)
        if not _is_image_url(norm):
            return
        if norm in seen:
            if kind == "gallery" and seen[norm].kind != "gallery":
                seen[norm].kind = "gallery"
            if alt and not seen[norm].alt:
                seen[norm].alt = alt
            return
        order += 1
        seen[norm] = ImageRef(url=norm, alt=alt.strip()[:200], kind=kind, order=order)

    if product_json:
        for img in product_json.get("images") or []:
            src = img.get("src") if isinstance(img, dict) else img
            alt = (img.get("alt") if isinstance(img, dict) else "") or ""
            add(src, alt, "gallery")

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("meta", attrs={"property": re.compile(r"^og:image(:secure_url)?$")}):
        add(tag.get("content", ""), "", "gallery")
    for script in soup.find_all("script", attrs={"type": re.compile("ld\\+json")}):
        try:
            data = json.loads(script.string or "")
        except (ValueError, TypeError):
            continue
        for obj in _walk_json(data):
            if isinstance(obj, dict) and str(obj.get("@type", "")).lower() == "product":
                imgs = obj.get("image") or []
                if isinstance(imgs, (str, dict)):
                    imgs = [imgs]
                for im in imgs:
                    add(im.get("url", "") if isinstance(im, dict) else im, "", "gallery")

    for tag in soup.find_all(["img", "source"]):
        alt = tag.get("alt", "") or ""
        kind = "gallery" if in_gallery_container(tag) else "page"
        for attr in IMG_ATTRS:
            val = tag.get(attr)
            if not val:
                continue
            if "srcset" in attr:
                for u in _srcset_urls(val):
                    add(u, alt, kind)
            else:
                add(val, alt, kind)

    # page builders (Tilda, Elementor, Webflow, Shogun) hang the real image off a <div>
    for tag in soup.find_all(True):
        if tag.name in ("img", "source"):
            continue
        kind = None
        for attr in LAZY_ATTRS:
            val = tag.get(attr)
            if not val or not isinstance(val, str):
                continue
            if kind is None:
                kind = "gallery" if in_gallery_container(tag) else "page"
            if "srcset" in attr:
                for u in _srcset_urls(val):
                    add(u, tag.get("alt", "") or "", kind)
            else:
                add(val, tag.get("alt", "") or "", kind)
    for tag in soup.find_all(style=re.compile(r"background(?:-image)?\s*:", re.I)):
        for m in re.finditer(r"url\((['\"]?)([^'\")]+)\1\)", tag["style"]):
            add(m.group(2))

    # raw-source sweep: image URLs inside inline JSON / scripts that the DOM walk misses.
    # Shopify's CDN first (those are product photos), then any other absolute image URL.
    for rx in (_SHOPIFY_CDN, _CDN_SHOPIFY, _ANY_IMAGE_URL):
        for m in rx.finditer(html):
            add(m.group(0).replace("\\/", "/"))

    refs = sorted(seen.values(), key=lambda r: (0 if r.kind == "gallery" else 1, r.order))
    return refs[: config.MAX_IMAGES]


def _walk_json(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _walk_json(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_json(v)


# --------------------------------------------------------------------------- download
def download_images(session: requests.Session, refs: list[ImageRef], dest: Path, delay_s: float = 0.4) -> list[dict]:
    """Save every image into dest, compressed; returns a manifest (filename, url, alt, kind, bytes...).
    Names: gallery_01.jpg ... then page_01.jpg ...; duplicates by content hash are dropped."""
    dest.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    hashes: set[str] = set()
    counters = {"gallery": 0, "page": 0}
    for ref in refs:
        try:
            r = _get(session, ref.url, headers={"Accept": "image/avif,image/webp,image/*,*/*;q=0.8", "Referer": ref.url})
        except RuntimeError as e:
            log.warning("skip %s: %s", ref.url, e)
            continue
        if r.status_code != 200 or not r.content:
            log.warning("skip %s: HTTP %s", ref.url, r.status_code)
            continue
        ctype = r.headers.get("content-type", "").split(";")[0].strip().lower()
        if not ctype.startswith("image/"):
            continue
        if len(r.content) < config.MIN_IMAGE_BYTES:
            continue
        digest = hashlib.sha1(r.content).hexdigest()
        if digest in hashes:
            continue
        hashes.add(digest)
        ext = mimetypes.guess_extension(ctype) or Path(urlparse(ref.url).path).suffix or ".jpg"
        ext = {".jpe": ".jpg", ".jpeg": ".jpg"}.get(ext, ext)
        shot = images.compress(r.content, ext)
        counters[ref.kind] += 1
        name = f"{ref.kind}_{counters[ref.kind]:02d}{shot.ext}"
        (dest / name).write_bytes(shot.data)
        if config.KEEP_ORIGINALS and shot.note != "original":
            originals = dest / "originals"
            originals.mkdir(exist_ok=True)
            (originals / f"{ref.kind}_{counters[ref.kind]:02d}{ext}").write_bytes(r.content)
        entry = {"file": name, "url": ref.url, "alt": ref.alt, "kind": ref.kind,
                 "bytes": len(shot.data), "source_bytes": shot.original_bytes, "sha1": digest}
        if shot.width:
            entry["size"] = f"{shot.width}x{shot.height}"
        if shot.note:
            entry["compression"] = shot.note
        manifest.append(entry)
        time.sleep(delay_s)
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


# --------------------------------------------------------------------------- page facts
_TRUST_WORDS = re.compile(r"(free shipping|money[- ]back|guarantee|returns?|refund|warranty|secure checkout|ships? (?:in|within|from)|delivery|30[- ]day|60[- ]day|90[- ]day|lifetime)", re.I)
_CTA_WORDS = re.compile(r"^(add to cart|buy now|buy it now|shop now|order now|get yours|claim|checkout|add to bag)", re.I)


def _text(el) -> str:
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el else ""


def _money(v) -> str:
    if v is None or v == "":
        return ""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return f"{f:.2f}"


def extract_page_data(html: str, url: str, product_json: dict | None = None) -> PageData:
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "svg", "iframe"]):
        if t.name == "script" and "ld+json" in (t.get("type") or ""):
            continue
        t.decompose()

    pd = PageData(url=url)
    meta = {}
    for m in soup.find_all("meta"):
        key = m.get("property") or m.get("name")
        if key and m.get("content"):
            meta[key.lower()] = m["content"].strip()
    pd.meta_description = meta.get("og:description") or meta.get("description") or ""

    # JSON-LD product / ratings
    ld_product = None
    for script in soup.find_all("script", attrs={"type": re.compile("ld\\+json")}):
        try:
            data = json.loads(script.string or "")
        except (ValueError, TypeError):
            continue
        for obj in _walk_json(data):
            if isinstance(obj, dict) and str(obj.get("@type", "")).lower() == "product" and ld_product is None:
                ld_product = obj
            if isinstance(obj, dict) and str(obj.get("@type", "")).lower() == "aggregaterating":
                pd.rating = pd.rating or str(obj.get("ratingValue", ""))
                pd.review_count = pd.review_count or str(obj.get("reviewCount") or obj.get("ratingCount") or "")
            if isinstance(obj, dict) and str(obj.get("@type", "")).lower() == "review":
                body = obj.get("reviewBody") or obj.get("description")
                if body and len(pd.review_snippets) < 12:
                    pd.review_snippets.append(re.sub(r"\s+", " ", str(body))[:400])

    if product_json:
        pd.platform = "shopify"
        pd.title = product_json.get("title", "")
        pd.handle = product_json.get("handle", "")
        pd.vendor = product_json.get("vendor", "")
        pd.product_type = product_json.get("product_type", "")
        pd.tags = product_json.get("tags") if isinstance(product_json.get("tags"), list) else [t.strip() for t in str(product_json.get("tags", "")).split(",") if t.strip()]
        pd.description_html = product_json.get("body_html") or ""
        pd.options = [{"name": o.get("name"), "values": o.get("values", [])} for o in product_json.get("options") or [] if isinstance(o, dict)]
        for v in product_json.get("variants") or []:
            pd.variants.append({
                "title": v.get("title"), "price": _money(v.get("price")), "compare_at_price": _money(v.get("compare_at_price")),
                "available": v.get("available"), "sku": v.get("sku"),
            })
        if pd.variants:
            prices = [float(v["price"]) for v in pd.variants if v["price"]]
            pd.price = _money(min(prices)) if prices else ""
            comps = [float(v["compare_at_price"]) for v in pd.variants if v["compare_at_price"]]
            pd.compare_at_price = _money(max(comps)) if comps else ""
    elif ld_product:
        pd.title = ld_product.get("name", "")
        pd.vendor = (ld_product.get("brand") or {}).get("name", "") if isinstance(ld_product.get("brand"), dict) else str(ld_product.get("brand") or "")
        pd.description_text = str(ld_product.get("description") or "")
        offers = ld_product.get("offers") or {}
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            pd.price = _money(offers.get("price") or offers.get("lowPrice"))
            pd.currency = offers.get("priceCurrency", "")
    if "shopify" in html.lower() and pd.platform == "unknown":
        pd.platform = "shopify"
    if not pd.currency and ld_product:
        offers = ld_product.get("offers") or {}
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            pd.currency = offers.get("priceCurrency", "") or ""
    if not pd.currency:
        pd.currency = meta.get("og:price:currency") or meta.get("product:price:currency") or ""
    if not pd.price:
        pd.price = meta.get("og:price:amount") or meta.get("product:price:amount") or ""
    if not pd.title:
        h1 = soup.find("h1")
        pd.title = _text(h1) or meta.get("og:title") or _text(soup.title)
    if not pd.handle:
        m = re.search(r"/products/([^/?#.]+)", url)
        pd.handle = m.group(1) if m else config.slugify(pd.title)

    if pd.description_html and not pd.description_text:
        pd.description_text = _text(BeautifulSoup(pd.description_html, "html.parser"))

    body = soup.body or soup
    pd.headings = [t for t in (_text(h) for h in body.find_all(["h1", "h2", "h3"])) if t and len(t) < 160]
    pd.headings = list(dict.fromkeys(pd.headings))[:60]

    bullets = []
    for li in body.find_all("li"):
        t = _text(li)
        if 8 <= len(t) <= 220 and not li.find("a", href=re.compile(r"^/(collections|pages|blogs)")):
            bullets.append(t)
    pd.bullets = list(dict.fromkeys(bullets))[:80]

    # FAQ: <details><summary>, or accordion pairs (h3/button followed by a paragraph)
    for det in body.find_all("details"):
        q = _text(det.find("summary"))
        a = _text(det).replace(q, "", 1).strip()
        if q and a and len(pd.faqs) < 20:
            pd.faqs.append({"q": q[:200], "a": a[:800]})
    if not pd.faqs:
        for q_el in body.find_all(["button", "h3", "h4", "dt"]):
            q = _text(q_el)
            if not q.endswith("?") or len(q) > 160:
                continue
            nxt = q_el.find_next(["p", "div", "dd"])
            a = _text(nxt)
            if a and a != q and len(pd.faqs) < 20:
                pd.faqs.append({"q": q, "a": a[:800]})

    for el in body.find_all(["p", "li", "span", "div"]):
        t = _text(el)
        if 8 <= len(t) <= 140 and _TRUST_WORDS.search(t) and len(pd.trust_lines) < 25:
            pd.trust_lines.append(t)
    pd.trust_lines = list(dict.fromkeys(pd.trust_lines))

    for el in body.find_all(["button", "a"]):
        t = _text(el)
        if t and _CTA_WORDS.search(t) and t not in pd.cta_texts and len(pd.cta_texts) < 10:
            pd.cta_texts.append(t)

    if not pd.review_snippets:
        for el in body.find_all(class_=re.compile(r"review|testimonial", re.I)):
            t = _text(el)
            if 40 <= len(t) <= 600 and len(pd.review_snippets) < 12:
                pd.review_snippets.append(t)
        pd.review_snippets = list(dict.fromkeys(pd.review_snippets))
    if not pd.review_count:
        m = re.search(r"(\d[\d,]{1,6})\s*(?:reviews|ratings|verified)", body.get_text(" "), re.I)
        pd.review_count = m.group(1) if m else ""
    if not pd.rating:
        m = re.search(r"(\d\.\d)\s*(?:/\s*5|out of 5|stars?)", body.get_text(" "), re.I)
        pd.rating = m.group(1) if m else ""

    text = re.sub(r"\s+", " ", body.get_text(" ", strip=True))
    pd.body_text = text[:20000]
    return pd


def select_for_download(refs: list[ImageRef], all_images: bool) -> list[ImageRef]:
    """Gallery only by default; everything when asked, or when the page exposes no gallery at all."""
    if all_images or not any(r.kind == "gallery" for r in refs):
        return refs
    return [r for r in refs if r.kind == "gallery"]


# --------------------------------------------------------------------------- orchestration
def grab(url: str, out_dir: Path | None = None, use_browser: bool | None = None, session: requests.Session | None = None,
         all_images: bool | None = None) -> tuple[PageData, Path, list[dict]]:
    """Competitor grab: page facts + images saved to <out_dir>/competitor_imgs/.
    By default only the gallery (top-of-fold product photos) is saved; all_images=True also saves
    the rest of the page's images (infographics, lifestyle blocks)."""
    all_images = config.GRAB_ALL_IMAGES if all_images is None else all_images
    session = session or make_session()
    html = fetch_html(session, url)
    product_json = fetch_shopify_product(session, url)
    discovered = None
    if product_json is None:
        # a landing page (/the-sol-light) rather than /products/<handle>: find the real product
        discovered = find_product_handle(html)
        if discovered:
            product_json = fetch_product_by_handle(session, url, discovered)
            if product_json:
                log.info("landing page: using the gallery of /products/%s", discovered)
        if product_json is None:
            title = (BeautifulSoup(html, "html.parser").title.get_text() if "<title" in html else "") or ""
            product_json = find_product_in_catalogue(session, url, html, title)
            if product_json:
                discovered = product_json.get("handle")
                log.info("landing page: matched the store catalogue to /products/%s", discovered)
    refs = extract_image_refs(html, url, product_json)
    js_heavy = use_browser is True or (use_browser is None and len(refs) < 3 and not product_json)
    if js_heavy:
        log.info("few images in static HTML; rendering with headless Chromium")
        try:
            html = render_html(url)
            refs = extract_image_refs(html, url, product_json)
        except Exception as e:  # noqa: BLE001 - a missing browser must not abort the grab
            log.warning("browser render failed (%s); keeping static HTML", e)
    data = extract_page_data(html, url, product_json)
    if discovered and product_json:
        data.handle = discovered
    data.images = refs
    slug = config.slugify(data.handle or data.title)
    out_dir = out_dir or config.product_dir(slug)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "page_source.html").write_text(html, encoding="utf-8")
    if product_json:
        (out_dir / "product.json").write_text(json.dumps(product_json, indent=2), encoding="utf-8")
    manifest = download_images(session, select_for_download(refs, all_images), out_dir / "competitor_imgs")
    (out_dir / "page_data.json").write_text(json.dumps(data.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return data, out_dir, manifest
