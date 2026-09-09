"""Paths, .env loading and settings for the PDP cloning pipeline (pdp.py).

Reuses the tracker's minimal .env loader so one .env file serves both tools.
Every setting is optional except where a command says otherwise; a missing key
only disables the command that needs it.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Minimal .env loader: KEY=VALUE lines, '#' comments, no interpolation.
    Existing environment variables win over the file."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.split(" #", 1)[0].strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


load_dotenv()

# Where every product gets its own folder: pdp_output/<product-slug>/
OUTPUT_ROOT = Path(os.environ.get("PDP_OUTPUT_DIR", ROOT / "pdp_output"))

REQUEST_TIMEOUT = (10, 45)
REQUEST_RETRIES = 3
USER_AGENT = os.environ.get(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36",
)
MIN_IMAGE_BYTES = int(os.environ.get("PDP_MIN_IMAGE_BYTES", "8000"))   # skip icons / badges / pixels
MAX_IMAGES = int(os.environ.get("PDP_MAX_IMAGES", "80"))
CHROMIUM_PATH = os.environ.get("META_CHROMIUM_PATH", "").strip()   # shared with the tracker; empty = Playwright's own Chromium

# --- Claude (product_summary polish + guide text) ---------------------------
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
ANTHROPIC_ENABLED = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))

# --- Higgsfield Cloud API ---------------------------------------------------
# Credentials: HF_KEY="key:secret" (or HF_API_KEY + HF_API_SECRET), from https://cloud.higgsfield.ai
HIGGSFIELD_MODEL = os.environ.get("HIGGSFIELD_MODEL", "openai/gpt-image-2/edit")   # confirmed to exist on platform.higgsfield.ai (hf-models)
HIGGSFIELD_IMAGE_ARG = os.environ.get("HIGGSFIELD_IMAGE_ARG", "image_urls")   # arg that carries reference URLs
HIGGSFIELD_MAX_REFS = int(os.environ.get("HIGGSFIELD_MAX_REFS", "6"))
HIGGSFIELD_ASPECT = os.environ.get("HIGGSFIELD_ASPECT", "1:1")
HIGGSFIELD_RESOLUTION = os.environ.get("HIGGSFIELD_RESOLUTION", "2K")
HIGGSFIELD_NUM_IMAGES = int(os.environ.get("HIGGSFIELD_NUM_IMAGES", "4"))
HIGGSFIELD_EXTRA_ARGS = os.environ.get("HIGGSFIELD_EXTRA_ARGS", "")   # JSON object merged into every request
# Backend: "api" = platform.higgsfield.ai with HF_KEY (higgsfield-client); "cli" = the `higgsfield` CLI on your
# normal account (`higgsfield auth login`). Default: api when HF_KEY is set, otherwise cli.
_HF_KEY_SET = bool(os.environ.get("HF_KEY") or (os.environ.get("HF_API_KEY") and os.environ.get("HF_API_SECRET")))
HIGGSFIELD_BACKEND = os.environ.get("HIGGSFIELD_BACKEND", "api" if _HF_KEY_SET else "cli").strip().lower()
HIGGSFIELD_CLI = os.environ.get("HIGGSFIELD_CLI", "higgsfield")                  # executable name / path
HIGGSFIELD_CLI_MODEL = os.environ.get("HIGGSFIELD_CLI_MODEL", "nano_banana_2")   # `higgsfield model list --json` for ids
HIGGSFIELD_CLI_EXTRA = os.environ.get("HIGGSFIELD_CLI_EXTRA", "")                # extra flags appended verbatim

# --- Shopify Admin API ------------------------------------------------------
SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE", "").strip()             # e.g. my-brand.myshopify.com
# Dev Dashboard app (the only kind you can create since Jan 2026): Client ID + Client secret; pdp.py mints
# the 24-hour Admin API token itself (client credentials grant) and caches it in SHOPIFY_TOKEN_CACHE.
SHOPIFY_CLIENT_ID = os.environ.get("SHOPIFY_CLIENT_ID", "").strip()
SHOPIFY_CLIENT_SECRET = os.environ.get("SHOPIFY_CLIENT_SECRET", "").strip()
SHOPIFY_ADMIN_TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN", "").strip()  # shpat_... from a legacy admin-created app (still works)
SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2025-07")
SHOPIFY_TOKEN_CACHE = Path(os.environ.get("SHOPIFY_TOKEN_CACHE", ROOT / "data" / "shopify_token.json"))
SHOPIFY_REQUIRED_SCOPES = ("write_products", "write_files")

# Prompts for `generate` when no --prompt / --prompt-file is given: one prompt per paragraph
# (blank-line separated), '#' lines are comments, {title} {handle} {vendor} {price} {product_type}
# are filled from the grabbed product. prompts.txt is yours (gitignored); prompts.example.txt is the starter.
PROMPTS_FILE = Path(os.environ.get("PDP_PROMPTS_FILE", ROOT / "prompts.txt"))
PROMPTS_EXAMPLE = ROOT / "prompts.example.txt"

# --- Brand ------------------------------------------------------------------
BRAND_NAME = os.environ.get("BRAND_NAME", "SoleneLife").strip()          # replaces the competitor's brand in titles
BRAND_SUFFIX = os.environ.get("BRAND_SUFFIX", "").strip()               # optional, e.g. "by SoleneLife" instead of a prefix
GRAB_ALL_IMAGES = os.environ.get("PDP_GRAB_ALL_IMAGES", "").strip() in ("1", "true", "yes")   # default: gallery (top-of-fold) only

# --- Guide ------------------------------------------------------------------
PDP_TEMPLATE = os.environ.get("PDP_TEMPLATE", str(ROOT / "templates" / "universal_pdp_template.md")).strip()


def slugify(text: str, max_len: int = 60) -> str:
    """Filesystem-safe folder name from a product title or handle."""
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "product")[:max_len].rstrip("-")


def product_dir(slug: str) -> Path:
    return OUTPUT_ROOT / slug


def generated_dir_name(product_name: str) -> str:
    """The user-specified folder name for Higgsfield output: '[product name]_shopify_PDP_imgs'."""
    return f"{slugify(product_name)}_shopify_PDP_imgs"


_TRADEMARKS = re.compile(r"[\u2122\u00ae\u00a9]")   # ™ ® ©


def generic_name(title: str, vendor: str = "", store_domain: str = "") -> str:
    """Competitor title without their brand: 'Ruffs™ Calming Diffuser Kit' -> 'Calming Diffuser Kit'."""
    name = _TRADEMARKS.sub("", title or "")
    host = (store_domain or "").lower().replace("www.", "").split(".")[0]
    stems = {host}
    for pre in ("get", "try", "shop", "the", "my", "buy", "hello", "meet", "go", "use"):
        if host.startswith(pre) and len(host) > len(pre) + 2:
            stems.add(host[len(pre):])
    for suf in ("store", "shop", "official", "co", "us", "uk", "au"):
        stems |= {st[: -len(suf)] for st in list(stems) if st.endswith(suf) and len(st) > len(suf) + 2}
    brands = {b for b in ({vendor or ""} | stems) if len(b) >= 3}
    for b in sorted(brands, key=len, reverse=True):
        name = re.sub(r"(?i)\b" + re.escape(b) + r"['\u2019]?s?\b", "", name)
    name = re.sub(r"\s*[|\-\u2013\u2014:]\s*$", "", name)
    name = re.sub(r"^\s*[|\-\u2013\u2014:]\s*", "", name)
    return re.sub(r"\s{2,}", " ", name).strip(" -\u2013\u2014|:") or title


def our_title(title: str, vendor: str = "", store_domain: str = "", brand: str | None = None) -> str:
    """'Ruffs™ Calming Diffuser Kit' -> 'SoleneLife Calming Diffuser Kit'."""
    brand = BRAND_NAME if brand is None else brand
    base = generic_name(title, vendor, store_domain)
    if not brand:
        return base
    if base.lower().startswith(brand.lower()):
        return base
    return f"{base} {BRAND_SUFFIX}".strip() if BRAND_SUFFIX else f"{brand} {base}"
