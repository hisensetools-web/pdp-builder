# imageGrabber - how to use it (no coding needed)

This tool reads the ClickUp product list and downloads every image from each competitor page into a folder on
your computer, one folder per product, ready for Higgsfield. You run it once a day. That's it.

## One-time setup (about 10 minutes)

**1. Install Python** (the language the tool is written in)
- Go to <https://www.python.org/downloads/> and click the big yellow **Download Python** button.
- Run the installer. On the first screen **tick the box "Add python.exe to PATH"** (bottom of the window). Then click **Install Now**.

**2. Unzip the tool**
- You were given `imageGrabber.zip`. Right-click it > **Extract All...** > Extract. Put the `imageGrabber` folder somewhere easy, like your Desktop.
- Don't run anything from inside the zip itself; always from the extracted folder.

**3. Run setup once**
- Open the `imageGrabber` folder and **double-click `SETUP.bat`**. It downloads the tool's parts and a browser (a few minutes).
- At the end it asks for the **ClickUp key** — a long code starting with `pk_`. Whoever gave you this tool has it. Paste it in and press Enter. (Right-click pastes in that black window.)
- When it says *Setup finished*, press any key.

If a step complains, take a screenshot of the window and send it to whoever gave you the tool.

**Updates:** when there's a new version you'll get a new zip. Extract it over the old folder (say Yes to replacing
files). Your downloaded images in `pdp_output` are kept.

## Every day

Open the `imageGrabber` folder and **double-click `RUN.bat`**. Nothing else.

What it does, in order (you'll see each step in the window):

1. Reads the **Product Research** list in ClickUp and takes every card in the **ready to build** column that has a competitor link (in *Main Competitor* or in the card's description).
2. Downloads every image from each competitor page into `pdp_output\<product name>\competitor_imgs\`. Images are compressed and there are no duplicates.
3. Ticks **z-imagesPulled** on the card and leaves a comment saying where the images went, so nobody pulls it twice.
4. Skips cards it already did, so running it again is quick.

Sometimes a **browser window opens by itself** showing a "verify you are human" puzzle (Etsy and Amazon do this). Solve the puzzle in that window and leave it alone - the tool waits for you (up to 3 minutes) and then carries on. Don't close the window yourself.

At the end it prints a summary (`grabbed: 3  skipped: 4`) and the window says **Done**. Press any key to close it.

## Where things end up

```
imageGrabber\
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

## Getting a product pulled

In ClickUp, open the product's card, make sure **Main Competitor** holds the link to the competitor's product page
(the page with the product photos, not the shop's home page; extra links can go in the description), then move the
card to **ready to build**. Next time you run `RUN.bat` it's included. Once pulled, the card gets **z-imagesPulled**
ticked and a comment with the folder name. Moving the card on (ready to launch, testing, ...) is up to you.

## If something looks wrong

| The window says | What it means | What to do |
|---|---|---|
| `Python is not installed yet` | Step 1 of setup was skipped or the PATH box wasn't ticked | Reinstall Python, tick **Add python.exe to PATH** |
| `could not read ClickUp` | No internet, or the ClickUp key is wrong / expired | Check you're online. Ask for a fresh key and run `SETUP.bat` again |
| `no product link on: ...` | That card is in *ready to build* but has no competitor link | Put the link in *Main Competitor* on the card |
| `0 products` | No card is in *ready to build* with a competitor link | Check ClickUp |
| `FAILED: HTTP 404` next to a product | The link on the card is dead | Open it in your browser; fix the link on the card |
| `the bot check was not cleared in time` | A puzzle window opened and wasn't solved within 3 minutes | Run again and solve it |
| `already grabbed` next to every product | Nothing new since last run | That's normal |
| A folder name in another language | The store is foreign and the tool used its title | It's the right product; rename the folder if you like |

Anything else: screenshot the window and send it to whoever gave you the tool.
