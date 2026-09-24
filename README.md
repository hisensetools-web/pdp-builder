# PDP builder

Give it a competitor product page and it produces everything needed to launch our own version of that page. One folder per product under `pdp_output/<slug>/`:

| what | where | command |
|---|---|---|
| every image on the competitor's page, rendered in headless Chromium so JavaScript-only slides and lazy images are included, size suffixes stripped so you get the full-size files, compressed (`--gallery-only` keeps just the product scroller) | `competitor_imgs/` + `manifest.json` (source URL, alt text, kind) | `grab` |
| summary of the competitor page (title, price/compare-at, variants, copy, headings in order, bullets, FAQ, trust lines, reviews) | `product_summary.md` + `product_summary.json` | `grab` |
| new images rendered by Higgsfield from your prompt, with the competitor images as references | `<product name>_shopify_PDP_imgs/` + `generation_log.json` | `generate` |
| those images uploaded to a **draft** Shopify product | `shopify_upload.json` | `upload` (`shopify-check` first) |
| PDF build guide for Fudge: the Universal PDP Template's Product Brief (B1-B16) filled, then every block card with copy, image assignment and build prompt for this product | `<slug>_fudge_guide.pdf` (+ `.md`) | `guide` |


## Setup (Windows, PowerShell)

```powershell
git clone https://github.com/hisensetools-web/pdp-builder.git
cd pdp-builder
python -m pip install -r requirements.txt
copy .env.example .env      # then fill in the keys (see below)
python pdp.py shopify-check
python pdp.py hf-check
python pdp.py hf-models     # which Higgsfield model ids exist; pick one for HIGGSFIELD_MODEL
```

Update later with `git pull`. Tests: `python -m unittest discover -s tests`.

## Commands

```bash
python pdp.py grab https://competitor.com/products/glow-neck-massager
python pdp.py generate glow-neck-massager                     # prompts from prompts.txt (one per paragraph, {title} etc. filled in)
python pdp.py generate glow-neck-massager --prompt "Studio shot on white, soft shadow, same product"   # or inline
python pdp.py upload glow-neck-massager                       # creates a DRAFT product with the competitor title
python pdp.py guide glow-neck-massager                        # template: templates/universal_pdp_template.md
python pdp.py run https://competitor.com/products/x           # all four, prompts from prompts.txt
python pdp.py list                                            # what has been grabbed / generated / uploaded
```

Keys in `.env` (see `.env.example`): `ANTHROPIC_API_KEY` (summary brief + guide text; without it you get the
raw-facts summary and a mechanical guide), Higgsfield credentials (below), Shopify app credentials (below),
`PDP_TEMPLATE` for the default template.

**Shopify app (for `upload`).** Since January 2026 custom apps are created in the Shopify Dev Dashboard and hand
you a Client ID + Client secret instead of a token; `pdp.py` mints the Admin API token itself (client credentials
grant, valid 24 h, cached in `data/shopify_token.json`). One-time setup, about five minutes:

1. Shopify admin > **Settings > Apps and sales channels > Develop apps > Build apps in Dev Dashboard** (or go to
   dev.shopify.com/dashboard and sign in with the same account). If it asks you to create an organization, do so;
   the store and the app must live in the same organization.
2. **Create app** > name it `pdp-uploader` (anything) > start from scratch / no template.
   The script has no web interface, so the URL fields are formalities: **App URL** =
   `https://shopify.dev/apps/default-app-home` (Shopify's own placeholder for apps without a UI), **Redirect URLs** =
   the same value if the form insists on one, **Embedded in Shopify admin** = off. Webhooks API version = the latest.
3. In the app: **Access** (or **Configuration > Access scopes**) > add `write_products` and `write_files` > save.
4. **Release** a version (top right; name optional).
5. **Home > Install app** > pick your store > **Install**.
6. **Settings** (left panel) > copy **Client ID** and **Client secret** into `.env` as `SHOPIFY_CLIENT_ID` /
   `SHOPIFY_CLIENT_SECRET`, plus `SHOPIFY_STORE=your-store.myshopify.com` (the myshopify domain, not the custom domain).
7. `python pdp.py shopify-check` prints the store name and the scopes the token carries, and says exactly which
   scope is missing if any (add it under Access, release again, reinstall).

An older admin-created app whose `shpat_...` token you still have keeps working: put it in `SHOPIFY_ADMIN_TOKEN`
and leave the client id/secret empty.

**Higgsfield: two backends.** `generate --backend cli` (or `HIGGSFIELD_BACKEND=cli`) drives the official
`higgsfield` CLI on your normal account: install it once with
`curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh` and run `higgsfield auth login`.
This is the recommended route for product pages because `generate --photoshoot product_shot` (or `lifestyle_scene`,
`hero_banner`, `closeup_product_with_person`, `ad_creative_pack`, ...) uses Higgsfield's `product-photoshoot` command,
whose backend prompt enhancer is built for exactly this; without `--photoshoot` it runs `generate create <model>`
with every reference passed as `--image` (default model `nano_banana_2`, change with `HIGGSFIELD_CLI_MODEL` or `--model`).
`generate --backend api` uses the developer API on platform.higgsfield.ai with `HF_KEY=key:secret` from
cloud.higgsfield.ai; `HIGGSFIELD_MODEL` / `HIGGSFIELD_IMAGE_ARG` pick the model and the request field that carries the
reference-image URLs (default `openai/gpt-image-2/edit` / `image_urls`). `python pdp.py hf-check [--backend cli|api]`
verifies the credentials without spending credits, and `generate --dry-run` prints the exact request or command.
Shopify pages are read through `/products/<handle>.json`; every page is also rendered in headless Chromium
when Playwright is installed (`--no-browser` skips that, `--browser` requires it).
**Prompts** live in `prompts.txt` in this folder (created from `prompts.example.txt` on first use, then yours to edit,
not tracked by git): one prompt per paragraph, `#` lines ignored, `{title}` `{handle}` `{vendor}` `{price}`
`{product_type}` filled from the grabbed product. `--prompt` / `--prompt-file` override it for one run.
Useful flags: `generate --ref path.jpg` (choose references by hand), `--num`, `upload --handle x` / `--product-id N` (attach to an existing product), `upload --with-description`,
`--dry-run` on `generate` and `upload`. A starter template is in `templates/pdp_template.example.md`.

## The short version

```powershell
git pull
python pdp.py batch          # every product in products.csv -> one folder each, images compressed
```

One folder per product under `pdp_output/`, named from your sheet, holding **every image on the competitor's
page** (compressed, no duplicates, product scroller first as `gallery_NN`, the rest as `page_NN`) plus
`product_summary.md` with the page's facts. Nothing is re-downloaded on a second run. What you do with the folder
afterwards is manual: Higgsfield, then Shopify.

## A whole spreadsheet at once

Open the tab you want (a CSV export contains **only the tab you are looking at**, which is how you pick one sheet out
of a workbook), then **File > Download > Comma-separated values**, save it in this folder as `products.csv`, and run:

```bash
python pdp.py batch                 # grab every product in the sheet
python pdp.py batch --guide         # ... and write each one's Fudge guide
python pdp.py batch --limit 3       # try the first three first
python pdp.py batch --dry-run       # list what it would grab, fetch nothing
python pdp.py batch mysheet.csv     # any other CSV
```

No column setup needed: the URL column is found by looking at the values, so research links (pipiads, TikTok,
Instagram, Google) are ignored and the product link is used, with tracking parameters stripped. Marketplace links
(Amazon, Etsy, AliExpress) count as product pages, since a sheet often cites them as the source. A store that blocks
plain requests is retried once in headless Chromium without the plain fetch; `--no-browser` skips rendering. Rows that
repeat a product with a blank name inherit it, duplicates are dropped, and a store that blocks us or 404s is logged and
the run carries on. Products already grabbed are skipped unless you pass `--redo`. Every row's outcome lands in
`batch_log.csv`. `products.example.csv` is the starter list; `products.csv` is yours and is not tracked by git.

## Finding the product's own photos

Every image on the page is saved by default. When Playwright is installed the page is first rendered in headless
Chromium: lazy images are forced to load, every carousel is scrolled to its end and its "next" button clicked, and
every image the browser fetches is captured off the network, so slides that exist only after a click and images the
store refuses to serve to a plain request (hot-link protection) still land in the folder. `--no-browser` skips the
render (static HTML only); `--browser` makes it required instead of best effort.

The files are named after where the image sits: the product scroller (top of fold) as `gallery_NN`, everything else as
`page_NN`, so the ones for Higgsfield are at the top of the folder. `--gallery-only` saves just the scroller. That
scroller is found these ways, in order of reliability:

1. **`/products/<handle>.json`** when the URL is a normal Shopify product page.
2. **The product behind a landing page.** A URL like `/the-sol-light` has no product JSON of its own, so the page is
   searched for the product it is built around (canonical URL first, then the most-referenced `/products/<handle>`)
   and that product's gallery is used.
3. **The store's catalogue.** A landing page that never links to a product still carries its variant id in the
   add-to-cart form, so `/products.json` is matched on product id, then variant id, then title.
4. **Page builders.** Tilda, Elementor, Webflow and Shogun hang the real image off a `<div>` (`data-original`,
   `data-bg`, `data-content-cover-bg`) with only a blurred placeholder in the inline style, and keep the remaining
   slides in an embedded JSON blob. Those attributes are read on every tag, not just `<img>`, and any image URL in
   the raw source is swept up, including the escaped `a\/b\/c.jpg` form used inside JSON.
5. **Gallery containers.** Images inside elements whose class or id reads as a product gallery, carousel, slider,
   swiper or thumbnail strip count as gallery images. Related-product carousels, testimonial sliders, headers and
   footers are excluded.

If none of them recognises a scroller, everything is still saved as `page_NN` and the run says so.

When a store still gives the wrong images, `python pdp.py inspect <product>` explains what the extractor saw in the
page already saved: the product links and ids on the page, which one it would use, every image with the containers
around it, and the CDN URLs in the raw source.

## Image compression

Every downloaded image is straightened (EXIF orientation), capped at 2048px on its longest side and re-encoded as
JPEG at quality 82, so a folder that arrives as 27 MB of store originals lands as about 1.3 MB. Transparency is
flattened onto white rather than black. An image that needs no resizing and would re-encode bigger than the store's
own file is kept exactly as downloaded, so compression never makes a file worse. `manifest.json` records both sizes
and the final pixel dimensions per image.

Per run, on `grab` and `batch`:

```bash
python pdp.py batch --no-compress        # save the store's files exactly as served
python pdp.py batch --keep-originals     # compressed images plus the untouched ones in competitor_imgs/originals/
python pdp.py batch --max-px 3000 --quality 90    # bigger and sharper
python pdp.py batch --format webp        # or png
```

The same settings as defaults in `.env`: `PDP_COMPRESS`, `PDP_IMAGE_MAX_PX` (0 disables resizing),
`PDP_IMAGE_QUALITY`, `PDP_IMAGE_FORMAT`, `PDP_KEEP_ORIGINALS`. Needs Pillow, which `requirements.txt` installs; without it
images are saved as downloaded and the run says so once.

## Branding

Everything we create is ours, not the competitor's: `BRAND_NAME` (default SoleneLife) replaces their brand in the
product title, so "Ruffs™ Calming Diffuser Kit" becomes "SoleneLife Calming Diffuser Kit" for the Shopify draft
product, the generated-images folder and the `{title}` placeholder in prompts (`{product}` is the unbranded name,
`{competitor_title}` the original). `--name` overrides the title for one run.

## Template

`templates/universal_pdp_template.md` is the text of our Universal PDP Template Guide (the PDF, converted). `guide`
hands it to Claude together with the product summary and produces the per-product companion Fudge needs: the filled
Product Brief, then for every block BUILD or DROP, the final copy, which generated image goes where, and the block's
build prompt with our values. Keep the PDF itself next to it for the reference screenshots (PDFs in `templates/` are
not committed).

## Offer and pricing

Fixed on every product, one-time purchase, no subscriptions, no free gifts:

| tier | price | compare-at |
|---|---|---|
| Buy 1 | $39.95 | $79.90 |
| Buy 2 Get 1 Free (default) | $79.90 | $119.85 |
| Buy 3 Get 2 Free | $119.85 | $199.75 |

`upload` creates the draft product with a "Bundle" option and one variant per tier carrying these prices, and the
guide states them as the Brief's B11 so Fudge's Block 06 maps tiers to variants. Override with `PDP_PRICING` in `.env`.
