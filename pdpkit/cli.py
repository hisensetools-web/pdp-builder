"""python pdp.py <command>. Run `python pdp.py --help`."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import config


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def _product_dir(slug_or_path: str) -> Path:
    p = Path(slug_or_path)
    if p.exists() and p.is_dir():
        return p
    d = config.product_dir(config.slugify(slug_or_path))
    if not d.exists():
        raise SystemExit(f"no product folder for '{slug_or_path}' (looked in {d}); run `grab <url>` first")
    return d


def _facts(product_dir: Path) -> dict:
    fp = product_dir / "product_summary.json"
    return json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else {}


def _product_name(product_dir: Path, override: str | None = None) -> str:
    """Our branded title (BRAND_NAME + competitor title without their brand), unless overridden."""
    if override:
        return override
    facts = _facts(product_dir)
    if facts.get("title"):
        from urllib.parse import urlparse
        return config.our_title(facts["title"], facts.get("vendor", ""), urlparse(facts.get("url", "")).netloc)
    return product_dir.name


def parse_prompts(text: str) -> list[str]:
    """Blank-line separated prompts; lines starting with '#' are comments; each prompt is joined to one line."""
    import re
    out = []
    for block in re.split(r"\n[ \t]*\n", text.replace("\r\n", "\n").replace("\ufeff", "")):
        lines = [l.strip() for l in block.split("\n") if l.strip() and not l.strip().startswith("#")]
        if lines:
            out.append(" ".join(lines))
    return out


def fill_placeholders(prompts: list[str], product_dir: Path | None) -> list[str]:
    facts = _facts(product_dir) if product_dir else {}
    from urllib.parse import urlparse
    domain = urlparse(facts.get("url", "")).netloc
    values = {k: str(facts.get(k) or "") for k in ("handle", "vendor", "price", "product_type", "currency")}
    values["competitor_title"] = str(facts.get("title") or "")
    values["product"] = config.generic_name(values["competitor_title"], values["vendor"], domain) if values["competitor_title"] else ""
    values["title"] = config.our_title(values["competitor_title"], values["vendor"], domain) if values["competitor_title"] else ""
    values["brand"] = config.BRAND_NAME
    out = []
    for p in prompts:
        for k, v in values.items():
            p = p.replace("{" + k + "}", v)
        out.append(p)
    return out


def _prompts(args, product_dir: Path | None = None) -> list[str]:
    prompts = list(args.prompt or [])
    source = None
    if args.prompt_file:
        source = Path(args.prompt_file)
    elif not prompts:
        if not config.PROMPTS_FILE.exists() and config.PROMPTS_EXAMPLE.exists():
            config.PROMPTS_FILE.write_text(config.PROMPTS_EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"created {config.PROMPTS_FILE.name} from {config.PROMPTS_EXAMPLE.name}; edit it to change the prompts")
        if config.PROMPTS_FILE.exists():
            source = config.PROMPTS_FILE
    if source:
        prompts += parse_prompts(source.read_text(encoding="utf-8"))
        print(f"prompts : {len(prompts)} from {source}")
    if not prompts:
        raise SystemExit(f"no prompts: write them in {config.PROMPTS_FILE} (one per paragraph) or pass --prompt / --prompt-file")
    return fill_placeholders(prompts, product_dir)


def _apply_image_opts(args) -> None:
    """Per-run overrides of the compression settings in .env."""
    if getattr(args, "no_compress", False) or getattr(args, "originals_only", False):
        config.COMPRESS_IMAGES = False
    if getattr(args, "keep_originals", False):
        config.KEEP_ORIGINALS = True
    if getattr(args, "max_px", None) is not None:
        config.IMAGE_MAX_PX = args.max_px
    if getattr(args, "quality", None) is not None:
        config.IMAGE_QUALITY = args.quality
    if getattr(args, "format", None):
        config.IMAGE_FORMAT = args.format


def _browser_choice(args):
    if getattr(args, "no_browser", False):
        return False
    if getattr(args, "browser", False):
        return True
    return None          # auto: render when Playwright is installed


def _images_choice(args):
    if getattr(args, "gallery_only", False):
        return False
    return None          # default from config: everything


def _size_line(manifest: list[dict]) -> str:
    """'4.1 MB -> 1.2 MB (71% smaller)' for one product's images."""
    out = sum(m.get("bytes", 0) for m in manifest)
    src = sum(m.get("source_bytes") or m.get("bytes", 0) for m in manifest)

    def mb(n: int) -> str:
        return f"{n / 1024 / 1024:.1f} MB" if n >= 1024 * 1024 else f"{n / 1024:.0f} KB"

    if not src:
        return "0 KB"
    pct = round(100 * (1 - out / src))
    return f"{mb(src)} -> {mb(out)}" + (f" ({pct}% smaller)" if pct > 0 else "")


# --------------------------------------------------------------------------- commands
def cmd_grab(args) -> int:
    from . import scrape, summary
    _apply_image_opts(args)
    if "<" in args.url or ">" in args.url:
        raise SystemExit(f"{args.url} still contains a placeholder. Open the product page in your browser and copy "
                         "the address bar, e.g. https://tykapryde.com/products/sol-study-light")
    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url
    try:
        data, out_dir, manifest = scrape.grab(args.url, use_browser=_browser_choice(args), all_images=_images_choice(args))
    except Exception as e:  # noqa: BLE001 - one clear line beats a traceback
        from . import scrape as _s
        hint = ("The page does not exist: open it in your browser and copy the address bar."
                if "404" in str(e) else
                "Check the URL opens in your browser; if the store blocks scripts, retry with --browser.")
        raise SystemExit(f"could not fetch {args.url}: {_s.short_error(e)}\n{hint}") from e
    md = summary.write_summary(data, out_dir, manifest, use_claude=not args.no_claude)
    from urllib.parse import urlparse
    print(f"product : {data.title}")
    print(f"ours    : {config.our_title(data.title, data.vendor, urlparse(data.url).netloc)}")
    print(f"folder  : {out_dir}")
    print(f"images  : {len(manifest)} saved to {out_dir / 'competitor_imgs'} ({sum(1 for m in manifest if m['kind'] == 'gallery')} gallery)")
    print(f"size    : {_size_line(manifest)}")
    via = sum(1 for m in manifest if m.get("via") == "browser")
    if via:
        print(f"note    : {via} image(s) came from the browser capture (the store refused a direct download)")
    if manifest and not any(m["kind"] == "gallery" for m in manifest):
        print("note    : no separate product gallery was detected; every image on the page is saved as page_NN")
    print(f"summary : {md}")
    if not config.ANTHROPIC_ENABLED and not args.no_claude:
        print("note    : ANTHROPIC_API_KEY not set, summary is the raw-facts version")
    return 0


def cmd_generate(args) -> int:
    pdir = _product_dir(args.product)
    name = _product_name(pdir, args.name)
    refs = [Path(r) for r in args.ref] if args.ref else None
    backend = args.backend or ("cli" if args.photoshoot else config.HIGGSFIELD_BACKEND)
    if backend == "cli":
        from . import higgsfield_cli
        out = higgsfield_cli.generate(pdir, name, _prompts(args, pdir), refs=refs, num_images=args.num, model=args.model,
                                      photoshoot_mode=args.photoshoot, dry_run=args.dry_run)
    else:
        from . import higgsfield
        out = higgsfield.generate(pdir, name, _prompts(args, pdir), refs=refs, num_images=args.num, model=args.model, dry_run=args.dry_run)
    print(f"generated images folder: {out}")
    return 0


def cmd_upload(args) -> int:
    from . import shopify_admin
    pdir = _product_dir(args.product)
    name = _product_name(pdir, args.name)
    folder = Path(args.folder) if args.folder else pdir / config.generated_dir_name(name)
    if not folder.exists():
        raise SystemExit(f"{folder} does not exist; run `generate` first or pass --folder")
    facts = {}
    fp = pdir / "product_summary.json"
    if fp.exists():
        facts = json.loads(fp.read_text(encoding="utf-8"))
    result = shopify_admin.upload_folder(
        folder, title=args.title or name, handle=args.handle, product_id=args.product_id,
        description_html=facts.get("description_html", "") if args.with_description else "",
        vendor=config.BRAND_NAME, product_type=facts.get("product_type", ""),
        dry_run=args.dry_run,
    )
    if not args.dry_run:
        p = result["product"]
        print(f"uploaded {len(result['uploaded'])} images to product {p.get('title')} ({p['id']})")
    return 0


def cmd_guide(args) -> int:
    from . import guide
    pdir = _product_dir(args.product)
    name = _product_name(pdir, args.name)
    template = Path(args.template or config.PDP_TEMPLATE or "")
    if not template.is_file():
        raise SystemExit("pass --template <file> (md/txt/docx/pdf/html) or set PDP_TEMPLATE in .env")
    pdf = guide.build_guide(pdir, name, template, use_claude=not args.no_claude)
    print(f"guide: {pdf}")
    return 0


def cmd_run(args) -> int:
    """grab -> generate -> upload -> guide, stopping at the first missing prerequisite."""
    from . import scrape, summary
    data, out_dir, manifest = scrape.grab(args.url, use_browser=_browser_choice(args), all_images=_images_choice(args))
    summary.write_summary(data, out_dir, manifest, use_claude=not args.no_claude)
    print(f"[1/4] grabbed {len(manifest)} images -> {out_dir}")
    name = args.name or data.title or data.handle
    args.product = str(out_dir)
    if args.prompt or args.prompt_file or config.PROMPTS_FILE.exists() or config.PROMPTS_EXAMPLE.exists():
        cmd_generate(args)
        print("[2/4] generated")
        if not args.skip_upload:
            args.folder = None
            args.title = None
            cmd_upload(args)
            print("[3/4] uploaded")
        else:
            print("[3/4] upload skipped")
    else:
        print("[2/4] no --prompt given, generation and upload skipped")
    if args.template or config.PDP_TEMPLATE:
        cmd_guide(args)
        print("[4/4] guide written")
    else:
        print("[4/4] no --template given, guide skipped")
    return 0


def cmd_batch(args) -> int:
    """Run the pipeline over every product URL in a spreadsheet export."""
    from . import batch
    path = Path(args.csv)
    if not path.is_file() and path.name == "products.csv" and config.PRODUCTS_EXAMPLE.exists():
        path.write_text(config.PRODUCTS_EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"created {path.name} from {config.PRODUCTS_EXAMPLE.name}; edit it or replace it with your own CSV export")
    if not path.is_file():
        raise SystemExit(f"{path} not found. In Google Sheets: File > Download > Comma-separated values (.csv), "
                         "save it in this folder, then pass its name.")
    _apply_image_opts(args)
    rows, note = batch.read_rows(path)
    print(f"{path.resolve()}")
    print(f"{len(rows)} products ({note}):")
    for r in rows:
        print(f"   {r.name or '(unnamed)':<45.45} {r.url[:70]}")
    print("If this is not the list you expect, re-export the right tab of your sheet over this file "
          "(a CSV export holds only the tab you are viewing).\n")
    results = batch.process(rows, do_guide=args.guide, do_upload=args.upload, all_images=_images_choice(args),
                            limit=args.limit, skip_existing=not args.redo, dry_run=args.dry_run,
                            browser=_browser_choice(args))
    batch.print_summary(results)
    if not args.dry_run:
        print(f"\nlog: {batch.write_log(results, path.with_name('batch_log.csv'))}")
    return 0


def cmd_hf_check(args) -> int:
    """Prove the Higgsfield backend works without spending credits."""
    from . import higgsfield, higgsfield_cli
    backend = args.backend or config.HIGGSFIELD_BACKEND
    if backend == "cli":
        print("backend: cli  (higgsfield on PATH:", higgsfield_cli.cli_path() or "NO", ")")
        print(higgsfield_cli.check())
        print(f"model in .env: {config.HIGGSFIELD_CLI_MODEL}; or `generate --photoshoot product_shot` for the product-photoshoot command")
        return 0
    try:
        url = higgsfield.check_credentials(Path(args.sample) if args.sample else None)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print("FAILED:", higgsfield.explain_error(e, config.HIGGSFIELD_MODEL))
        return 1
    print("Higgsfield credentials OK. Uploaded test image ->", url)
    print(f"model in .env: {config.HIGGSFIELD_MODEL}  (reference field: {config.HIGGSFIELD_IMAGE_ARG})")
    print("next: python pdp.py generate <product> --prompt \"...\" --num 1   (one image, to confirm the model id)")
    return 0


def cmd_hf_models(args) -> int:
    """Probe Higgsfield model ids with an empty request: 404 = missing, validation error = exists (and names its fields)."""
    import higgsfield_client
    from . import higgsfield
    client = higgsfield_client.SyncClient(timeout=30.0)
    ids = args.model_id or list(higgsfield.CANDIDATE_MODELS)
    found = []
    for mid in ids:
        status, detail = higgsfield.probe_model(client, mid)
        if status == "exists":
            fields = higgsfield.required_fields(detail)
            found.append(mid)
            print(f"EXISTS   {mid}   required: {', '.join(fields) or detail[:160]}")
        elif status == "missing":
            print(f"missing  {mid}")
        else:
            print(f"?        {mid}   {detail}")
    if found:
        print("\nset in .env:  HIGGSFIELD_MODEL=<one of the EXISTS ids that takes reference images>")
        print("              HIGGSFIELD_IMAGE_ARG=<its image field: image_urls / image_url / images / input_images>")
    return 0 if found else 1


def cmd_hf_fields(args) -> int:
    """Print the validator's answer to a deliberately invalid request: names the fields a model knows."""
    import higgsfield_client
    from . import higgsfield
    client = higgsfield_client.SyncClient(timeout=30.0)
    for mid in args.model_id:
        print(f"== {mid}")
        result = higgsfield.map_fields(client, mid, log_fn=lambda m: print("   ", m))
        print("fields the model knows:")
        for k, v in result["known"].items():
            print(f"   {k:22s} {v}")
        image_fields = [k for k in result["known"] if k in higgsfield.IMAGE_FIELD_CANDIDATES]
        print("rejected / ignored candidates:", ", ".join(result["unknown"]) or "none")
        if image_fields:
            print(f"\n=> reference-image field: {image_fields[0]}   (set HIGGSFIELD_IMAGE_ARG={image_fields[0]} in .env if different from the default)")
        print()
    return 0


def cmd_shopify_check(args) -> int:
    """Mint/verify the Admin API token and confirm the app has the scopes `upload` needs."""
    from . import shopify_admin
    admin = shopify_admin.ShopifyAdmin()
    info = admin.whoami()
    print(f"store  : {info['shop']['name']} ({info['shop']['myshopifyDomain']})")
    print(f"scopes : {', '.join(info['scopes']) or '(none)'}")
    if info["missing"]:
        print(f"MISSING: {', '.join(info['missing'])} -> add them under the app's Access scopes in the Dev Dashboard, release a new version, and reinstall the app on the store")
        return 1
    print("OK: write_products and write_files present; `upload` will work")
    return 0


def cmd_inspect(args) -> int:
    """Explain what the extractor sees in a page already saved by `grab`, so a store that
    yielded the wrong images can be diagnosed without fetching it again."""
    import json as _json
    import re as _re
    from bs4 import BeautifulSoup
    from . import scrape

    pdir = _product_dir(args.product)
    html_path = pdir / "page_source.html"
    if not html_path.is_file():
        raise SystemExit(f"{html_path} not found; run `grab` for this product first")
    html = html_path.read_text(encoding="utf-8", errors="replace")
    facts = _facts(pdir)
    url = facts.get("url", "")
    print(f"page    : {html_path}  ({len(html) / 1024:.0f} KB)")
    print(f"url     : {url}")
    print(f"platform: {facts.get('platform', '?')}   product.json present: {(pdir / 'product.json').exists()}")

    handles = _re.findall(r"/products/([a-z0-9][a-z0-9\-_%]{1,120})(?=[\"'?#/\s\\]|$)", html, _re.I)
    counts: dict[str, int] = {}
    for h in handles:
        counts[h] = counts.get(h, 0) + 1
    print("\nproduct links on the page:")
    if counts:
        for h, n in sorted(counts.items(), key=lambda kv: -kv[1])[:10]:
            print(f"   {n:4d}x  /products/{h}")
        print(f"   -> would use: /products/{scrape.find_product_handle(html)}")
    else:
        print("   none: this page never links to a /products/ URL")

    pids, vids = scrape.page_product_ids(html)
    print(f"\nids on the page: product {sorted(pids)[:5] or 'none'}   variant {sorted(vids)[:5] or 'none'}")
    if not counts and not pids and not vids:
        print("   (nothing to match against the store catalogue either)")

    refs = scrape.extract_image_refs(html, url or "https://example.com")
    gallery = [r for r in refs if r.kind == "gallery"]
    print(f"\nimages found: {len(refs)} total, {len(gallery)} gallery")
    soup = BeautifulSoup(html, "html.parser")
    shown = 0
    for tag in soup.find_all("img"):
        src = next((tag.get(a) for a in ("src", "data-src", "srcset", "data-srcset") if tag.get(a)), None)
        if not src or shown >= args.show:
            continue
        chain = []
        node = tag
        for _ in range(4):
            node = getattr(node, "parent", None)
            if node is None or not getattr(node, "get", None):
                break
            marker = " ".join(node.get("class") or []) or node.get("id") or ""
            if marker:
                chain.append(marker[:40])
        print(f"   {'GALLERY' if scrape.in_gallery_container(tag) else '  page '}  {src.split()[0][-70:]}")
        print(f"            in: {' < '.join(chain) or '(no classed ancestors)'}")
        shown += 1

    cdn = set(_re.findall(r"https?://[^\s\"'<>]+?/cdn/shop/[^\s\"'<>)]+?\.(?:jpe?g|png|webp|avif)", html, _re.I))
    print(f"\nCDN image URLs in the raw source: {len(cdn)}")
    for u in sorted(cdn)[:args.show]:
        print(f"   {u[-90:]}")
    print("\nIf the gallery count is 0 and no /products/ link or id appears above, the page builds its")
    print("scroller in JavaScript from data this file does not contain. Send me this page_source.html.")
    return 0


def cmd_list(args) -> int:
    root = config.OUTPUT_ROOT
    if not root.exists():
        print(f"nothing yet in {root}")
        return 0
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        comp = d / "competitor_imgs"
        n_comp = sum(1 for p in comp.iterdir() if p.suffix.lower() in (".jpg", ".png", ".webp", ".jpeg")) if comp.exists() else 0
        gens = [g for g in d.iterdir() if g.is_dir() and g.name.endswith("_shopify_PDP_imgs")]
        n_gen = sum(1 for g in gens for p in g.iterdir() if p.suffix.lower() in (".jpg", ".png", ".webp", ".jpeg"))
        guide = "guide" if list(d.glob("*_fudge_guide.pdf")) else "-"
        uploaded = "uploaded" if any((g / "shopify_upload.json").exists() for g in gens) else "-"
        print(f"{d.name:40s} competitor={n_comp:3d} generated={n_gen:3d} {uploaded:9s} {guide}")
    return 0


def cmd_compress(args) -> int:
    """Heavy-compress every image in a product folder into compressed/ (what compress_images.bat runs)."""
    from . import images
    target = Path(args.folder).expanduser()
    if not target.is_dir():
        candidate = config.product_dir(config.slugify(args.folder))
        if candidate.is_dir():
            target = candidate
        else:
            raise SystemExit(f"{args.folder} is not a folder (and there is no product called that under {config.OUTPUT_ROOT})")
    if not images.available():
        raise SystemExit("Pillow is not installed: run  python -m pip install pillow")
    target = target.resolve()
    where = "in place" if args.in_place else str(Path(args.out) if args.out else target / images.COMPRESSED_DIR)
    print(f"compressing images under {target} -> {where}")
    results = images.compress_folder(target, out=Path(args.out) if args.out else None, fmt=args.format,
                                     quality=args.quality, max_px=args.max_px, in_place=args.in_place, redo=args.redo)
    done = [r for r in results if not r["skipped"]]
    for r in done:
        note = f" ({r['note']})" if r.get("note") else ""
        print(f"  {r['source']:50s} {r['source_bytes'] / 1024:7.0f} KB -> {r['bytes'] / 1024:6.0f} KB  {r['out']}{note}")
    skipped = len(results) - len(done)
    if not results:
        print("  no images found (jpg / png / webp) in that folder or its subfolders")
    else:
        print(f"{len(done)} compressed" + (f", {skipped} already done (--redo to repeat them)" if skipped else "")
              + f": {_size_line(results)}")
    return 0


# --------------------------------------------------------------------------- parser
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pdp.py", description="Clone a competitor PDP: images, summary, Higgsfield renders, Shopify upload, Fudge guide.")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="command", required=True)

    def add_image_opts(sp):
        g = sp.add_argument_group("images")
        g.add_argument("--no-compress", action="store_true",
                       help="save images exactly as the store served them (no resize, no re-encode)")
        g.add_argument("--keep-originals", action="store_true",
                       help="save the untouched files too, in competitor_imgs/originals/")
        g.add_argument("--max-px", type=int, metavar="N",
                       help=f"longest side after resize (default {config.IMAGE_MAX_PX}; 0 = never resize)")
        g.add_argument("--quality", type=int, metavar="N", help=f"JPEG/WebP quality (default {config.IMAGE_QUALITY})")
        g.add_argument("--format", choices=("jpeg", "webp", "png"), help=f"output format (default {config.IMAGE_FORMAT})")

    def add_product(sp):
        sp.add_argument("product", help="product slug (folder under pdp_output/) or a folder path")
        sp.add_argument("--name", help="override the product name used for folder / Shopify title")

    def add_generate_opts(sp):
        sp.add_argument("--prompt", action="append", help="Higgsfield prompt (repeat for several); default: prompts.txt in this folder")
        sp.add_argument("--prompt-file", help="text file, prompts separated by blank lines (default prompts.txt)")
        sp.add_argument("--ref", action="append", help="explicit reference image path (repeat); default: first gallery images")
        sp.add_argument("--num", type=int, help=f"images per prompt (default {config.HIGGSFIELD_NUM_IMAGES})")
        sp.add_argument("--model", help=f"Higgsfield model id (api default {config.HIGGSFIELD_MODEL}; cli default {config.HIGGSFIELD_CLI_MODEL})")
        sp.add_argument("--backend", choices=("api", "cli"), help=f"api = HF_KEY on platform.higgsfield.ai, cli = `higgsfield` CLI (default {config.HIGGSFIELD_BACKEND})")
        sp.add_argument("--photoshoot", metavar="MODE", help="use `higgsfield product-photoshoot create --mode MODE` (cli backend): product_shot, lifestyle_scene, hero_banner, ...")

    def add_upload_opts(sp):
        sp.add_argument("--handle", help="attach to the existing Shopify product with this handle")
        sp.add_argument("--product-id", help="attach to this Shopify product id (number or gid)")
        sp.add_argument("--title", help="title for a new draft product (default: competitor title)")
        sp.add_argument("--with-description", action="store_true", help="also copy the competitor description/vendor onto the new draft")

    s = sub.add_parser("grab", help="download every image on a competitor PDP + write product_summary")
    s.add_argument("url")
    s.add_argument("--browser", action="store_true", help="require the headless Chromium render (fail instead of falling back to static HTML)")
    s.add_argument("--no-browser", action="store_true", help="static HTML only, no Chromium render")
    s.add_argument("--all-images", action="store_true", help=argparse.SUPPRESS)   # the default now
    s.add_argument("--gallery-only", action="store_true", help="keep only the product gallery photos, not the rest of the page")
    s.add_argument("--no-claude", action="store_true", help="skip the Claude rewrite of the summary")
    add_image_opts(s)
    s.set_defaults(func=cmd_grab)

    s = sub.add_parser("generate", help="Higgsfield images using competitor_imgs as references")
    add_product(s)
    add_generate_opts(s)
    s.add_argument("--dry-run", action="store_true", help="print the request without calling Higgsfield")
    s.set_defaults(func=cmd_generate)

    s = sub.add_parser("upload", help="upload the generated images to Shopify (draft product)")
    add_product(s)
    add_upload_opts(s)
    s.add_argument("--folder", help="upload this folder instead of <name>_shopify_PDP_imgs")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_upload)

    s = sub.add_parser("guide", help="PDF build instructions for Fudge from the template + product_summary")
    add_product(s)
    s.add_argument("--template", help="reference PDP template (md/txt/docx/pdf/html); default PDP_TEMPLATE in .env")
    s.add_argument("--no-claude", action="store_true")
    s.set_defaults(func=cmd_guide)

    s = sub.add_parser("run", help="grab -> generate -> upload -> guide in one go")
    s.add_argument("url")
    s.add_argument("--name")
    s.add_argument("--browser", action="store_true")
    s.add_argument("--no-browser", action="store_true")
    s.add_argument("--all-images", action="store_true", help=argparse.SUPPRESS)
    s.add_argument("--gallery-only", action="store_true")
    s.add_argument("--no-claude", action="store_true")
    add_generate_opts(s)
    add_upload_opts(s)
    s.add_argument("--skip-upload", action="store_true")
    s.add_argument("--template")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("hf-check", help="verify HF_KEY by uploading one tiny image (no credits spent)")
    s.add_argument("--sample", help="api backend: upload this image instead of a 1x1 placeholder")
    s.add_argument("--backend", choices=("api", "cli"))
    s.set_defaults(func=cmd_hf_check)

    s = sub.add_parser("hf-models", help="find which Higgsfield model ids exist (free: empty requests only)")
    s.add_argument("model_id", nargs="*", help="ids to probe (default: a built-in list of likely image models)")
    s.set_defaults(func=cmd_hf_models)

    s = sub.add_parser("hf-fields", help="show which request fields a Higgsfield model accepts (free: invalid request only)")
    s.add_argument("model_id", nargs="+")
    s.set_defaults(func=cmd_hf_fields)

    s = sub.add_parser("shopify-check", help="verify the Shopify app credentials and scopes (mints the token if needed)")
    s.set_defaults(func=cmd_shopify_check)

    s = sub.add_parser("batch", help="grab every product URL in a spreadsheet export (CSV)")
    s.add_argument("csv", nargs="?", default="products.csv", help="CSV exported from your sheet (default products.csv)")
    s.add_argument("--guide", action="store_true", help="also write the Fudge guide for each product")
    s.add_argument("--upload", action="store_true", help="also upload each product's generated images to Shopify")
    s.add_argument("--all-images", action="store_true", help=argparse.SUPPRESS)   # the default now
    s.add_argument("--gallery-only", action="store_true", help="keep only the product gallery photos, not the rest of the page")
    s.add_argument("--limit", type=int, help="only the first N products")
    s.add_argument("--redo", action="store_true", help="grab again even if the product was grabbed before")
    s.add_argument("--browser", action="store_true", help="require the Chromium render for every row (fail rather than fall back)")
    s.add_argument("--no-browser", action="store_true", help="static HTML only, no Chromium render")
    s.add_argument("--dry-run", action="store_true", help="list what would be grabbed, fetch nothing")
    add_image_opts(s)
    s.set_defaults(func=cmd_batch)

    s = sub.add_parser("inspect", help="explain what the extractor sees in an already-grabbed page")
    s.add_argument("product", help="product slug (folder under pdp_output/) or a folder path")
    s.add_argument("--show", type=int, default=12, help="how many images to list (default 12)")
    s.set_defaults(func=cmd_inspect)

    s = sub.add_parser("compress", help="heavy-compress every image in a product folder into compressed/ (what compress_images.bat runs)")
    s.add_argument("folder", help="a product folder (or its name under pdp_output/); subfolders are included")
    s.add_argument("--format", choices=["webp", "jpeg", "png"], help=f"output format (default {config.HEAVY_FORMAT})")
    s.add_argument("--quality", type=int, help=f"WebP/JPEG quality (default {config.HEAVY_QUALITY})")
    s.add_argument("--max-px", type=int, help=f"longest side in pixels, 0 = keep size (default {config.HEAVY_MAX_PX})")
    s.add_argument("--out", help="write the compressed files somewhere other than <folder>/compressed/")
    s.add_argument("--in-place", action="store_true", help="replace each image with its compressed version instead")
    s.add_argument("--redo", action="store_true", help="recompress files already done on an earlier run")
    s.set_defaults(func=cmd_compress)

    s = sub.add_parser("list", help="what has been grabbed / generated / uploaded")
    s.set_defaults(func=cmd_list)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _setup_logging(args.verbose)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130
