# PDP builder - how to use it (no coding needed)

This tool reads the product sheet and downloads every image from each competitor page into a folder on your
computer, one folder per product, ready for Higgsfield. You run it once a day. That's it.

## One-time setup (about 15 minutes)

You need three things installed. Do them in this order.

**1. Python** (the language the tool is written in)
- Go to <https://www.python.org/downloads/> and click the big yellow **Download Python** button.
- Run the installer. On the first screen **tick the box "Add python.exe to PATH"** (bottom of the window). Then click **Install Now**.

**2. Git** (lets the tool update itself)
- Go to <https://git-scm.com/download/win>, download the 64-bit installer, run it, and click **Next** through every screen. The defaults are fine.

**3. The tool itself**
- Ask for access to the GitHub project `hisensetools-web/pdp-builder` (whoever gave you this can add you as a collaborator).
- Decide where you want the tool to live, for example your Desktop.
- Open the folder in File Explorer, click in the address bar at the top, type `cmd` and press Enter. A black window opens.
- Paste this line and press Enter:

  ```
  git clone https://github.com/hisensetools-web/pdp-builder.git
  ```

  A `pdp-builder` folder appears. (If it asks you to sign in to GitHub, sign in with your GitHub account in the window that pops up.)
- Open the `pdp-builder` folder and **double-click `SETUP.bat`**. It downloads the tool's parts and a browser; wait until it says *Setup finished*, then press any key.

If a step complains, take a screenshot of the window and send it to whoever gave you the tool.

## Every day

Open the `pdp-builder` folder and **double-click `RUN.bat`**. Nothing else.

What it does, in order (you'll see each step in the window):

1. Updates itself if there's a newer version.
2. Downloads the **Main TikTok Prods V2** tab of the *Product Research TT 2.0* sheet.
3. Lists the products it will take: every row whose **LP Status** is **Pending** and whose **Competition** cell has a link to the product page.
4. Downloads every image from each product page into `pdp_output\<product name>\competitor_imgs\`. Images are compressed and there are no duplicates.
5. Skips products it already has, so running it again is quick.

Sometimes a **browser window opens by itself** showing a "verify you are human" puzzle (Etsy and Amazon do this). Solve the puzzle in that window and leave it alone - the tool waits for you (up to 3 minutes) and then carries on. Don't close the window yourself.

At the end it prints a summary (`grabbed: 3  skipped: 4`) and the window says **Done**. Press any key to close it.

## Where things end up

```
pdp-builder\
  pdp_output\
    swinging-ghost-decor\
      competitor_imgs\        <- the downloaded photos: gallery_01.jpg (product photos first), then page_01.jpg ...
      compress_images.bat     <- see below
      product_summary.md      <- the competitor page's text: title, price, bullets, FAQ
    bling-ghostface-collection\
      ...
  batch_log.csv               <- one line per product per run: what happened
```

## After Higgsfield: compressing the new images

When you've made the new product images in Higgsfield, save or paste them anywhere inside that product's folder
(for example into `swinging-ghost-decor\`). Then **double-click `compress_images.bat`** in that folder. Every image
in the folder, the downloaded ones and yours, is written to a `compressed\` folder as small WebP files ready for
Shopify. The originals are left untouched. Run it again whenever you add more images; it only does the new ones.

## Adding a product to the sheet

In the sheet, fill in **Product Name**, paste the competitor's product page link in **Competition** (the page with
the product photos, not the shop's home page; several links in one cell are fine), and set **LP Status** to
**Pending**. Next time you run `RUN.bat` it's included. When a product is done, change its LP Status to anything
other than Pending and it's left alone.

## If something looks wrong

| The window says | What it means | What to do |
|---|---|---|
| `Python is not installed yet` | Step 1 of setup was skipped or the PATH box wasn't ticked | Reinstall Python, tick **Add python.exe to PATH** |
| `could not download the sheet` | No internet, or the sheet's sharing was changed | Check you're online. The sheet must be shared as *Anyone with the link - Viewer* |
| `0 products` | No row has LP Status = Pending with a product link | Check the sheet |
| `FAILED: HTTP 404` next to a product | The link in the Competition cell is dead | Open it in your browser; fix the link in the sheet |
| `the bot check was not cleared in time` | A puzzle window opened and wasn't solved within 3 minutes | Run again and solve it |
| `already grabbed` next to every product | Nothing new since last run | That's normal |
| A folder name in another language | The store is foreign and the tool used its title | It's the right product; rename the folder if you like |

Anything else: screenshot the window and send it to whoever gave you the tool.
