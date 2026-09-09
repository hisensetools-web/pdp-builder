# PDP builder

Give it a competitor product page and it produces everything needed to launch our own version of that page. One folder per product under `pdp_output/<slug>/`:

| what | where | command |
|---|---|---|
| every image on the competitor page (gallery first, then page images, size suffixes stripped so you get the originals) | `competitor_imgs/` + `manifest.json` (source URL, alt text, kind) | `grab` |
| summary of the competitor page (title, price/compare-at, variants, copy, headings in order, bullets, FAQ, trust lines, reviews) | `product_summary.md` + `product_summary.json` | `grab` |
| new images rendered by Higgsfield from your prompt, with the competitor images as references | `<product name>_shopify_PDP_imgs/` + `generation_log.json` | `generate` |
| those images uploaded to a **draft** Shopify product | `shopify_upload.json` | `upload` (`shopify-check` first) |
| PDF build instructions for Fudge, merged from our reference PDP template + the summary | `<slug>_fudge_guide.pdf` (+ `.md`) | `guide` |


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
python pdp.py generate glow-neck-massager --prompt "Studio shot on white, soft shadow, same product" --prompt "Lifestyle shot, woman on sofa using it"
python pdp.py upload glow-neck-massager                       # creates a DRAFT product with the competitor title
python pdp.py guide glow-neck-massager --template templates/pdp_template.md
python pdp.py run https://competitor.com/products/x --prompt "..." --template templates/pdp_template.md   # all four
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
reference-image URLs (default `bytedance/seedream/v4/edit` / `image_urls`). `python pdp.py hf-check [--backend cli|api]`
verifies the credentials without spending credits, and `generate --dry-run` prints the exact request or command.
Shopify pages are read through `/products/<handle>.json`; other platforms fall back
to HTML parsing and, when the page is JavaScript-rendered, a headless Chromium pass (`grab --browser` forces it).
Useful flags: `generate --ref path.jpg` (choose references by hand), `--num`, `--prompt-file` (blank-line separated
prompts), `upload --handle x` / `--product-id N` (attach to an existing product), `upload --with-description`,
`--dry-run` on `generate` and `upload`. A starter template is in `templates/pdp_template.example.md`.
