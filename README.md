# PDP builder

Give it a competitor product page and it produces everything needed to launch our own version of that page. One folder per product under `pdp_output/<slug>/`:

| what | where | command |
|---|---|---|
| the competitor's gallery images (top of fold; `--all-images` for the rest of the page), size suffixes stripped so you get the originals | `competitor_imgs/` + `manifest.json` (source URL, alt text, kind) | `grab` |
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
Shopify pages are read through `/products/<handle>.json`; other platforms fall back
to HTML parsing and, when the page is JavaScript-rendered, a headless Chromium pass (`grab --browser` forces it).
**Prompts** live in `prompts.txt` in this folder (created from `prompts.example.txt` on first use, then yours to edit,
not tracked by git): one prompt per paragraph, `#` lines ignored, `{title}` `{handle}` `{vendor}` `{price}`
`{product_type}` filled from the grabbed product. `--prompt` / `--prompt-file` override it for one run.
Useful flags: `generate --ref path.jpg` (choose references by hand), `--num`, `upload --handle x` / `--product-id N` (attach to an existing product), `upload --with-description`,
`--dry-run` on `generate` and `upload`. A starter template is in `templates/pdp_template.example.md`.

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
