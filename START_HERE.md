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

**4. Google Drive (required — this is where the images go)**
- Install Google Drive for Desktop from <https://www.google.com/drive/download/> and sign in with the Google account
  the team folder was shared with.
- Open the team's **imageGrabber** folder link in your browser. Right-click the folder name at the top → **Organise** →
  **Add shortcut** → **My Drive** → Add.
- Wait a minute, then double-click `SETUP.bat` once more. It should print *images go to: G:\My Drive\imageGrabber (Google Drive)*.

The tool only saves into that folder. If Drive isn't set up, `RUN.bat` stops and prints these same steps.

**Updates:** when there's a new version you'll get a new zip. Extract it over the old folder (say Yes to replacing
files). Your downloaded images in `pdp_output` are kept.

## Every day

Open the `imageGrabber` folder and **double-click `RUN.bat`**. Nothing else.

What it does, in order (you'll see each step in the window):

1. Reads the **Product Research** list in ClickUp and takes every card in the **ready for lp** column that has a competitor link (in *Main Competitor* or in the card's description).
2. Downloads every image from each competitor page into `pdp_output\<product name>\custom-images\`. Images are compressed and there are no duplicates.
3. Ticks **z-imagesPulled** on the card and leaves a comment saying where the images went, so nobody pulls it twice.
4. Skips cards it already did, so running it again is quick.

Sometimes a **browser window opens by itself** showing a "verify you are human" puzzle (Etsy and Amazon do this). Solve the puzzle in that window and leave it alone - the tool waits for you (up to 3 minutes) and then carries on. Don't close the window yourself.

At the end it prints a summary (`grabbed: 3  skipped: 4`) and the window says **Done**. Press any key to close it.

## Talking to Claude instead of double-clicking (optional)

The `imageGrabber` folder contains a `CLAUDE.md` that teaches Claude how to run the tool. Once the Claude desktop app is
pointed at the folder, you just say what you want.

1. Install the **Claude desktop app** from <https://claude.ai/download> and sign in with the team's Claude account.
2. In the app, open the **Code** tab, click **Open folder** (or **New session**) and choose your `imageGrabber` folder.
3. Type, in plain words, for example:
   - *grab the images for Fall Tumbler*
   - *pull everything that's ready*
   - *pull Halloween Tumbler again*
   - *compress the images for Energy Drink Plush*
   - *is ClickUp connected?*

Claude runs the tool and tells you how many images it got, where they went, and that the ClickUp card was ticked.
If a browser window with a "verify you are human" puzzle appears, solve it and leave the window open — Claude will
say so. Claude may ask you to allow a command the first time; that's normal, click Allow.

Two things Claude won't do: move cards between columns (that's yours), or change the tool itself on your laptop.

## Where things end up

In the team's Google Drive folder, **and** a copy in `Desktop\imageGrabber images` on your own computer (the window
says `images go to: ...` and `and a copy to: ...` at the start of every run). Inside, one folder per product:

```
imageGrabber (Drive)\
    swinging-ghost-decor\
      custom-images\        <- the downloaded photos: gallery_01.jpg (product photos first), then page_01.jpg ...
      compress_images.bat     <- see below
      product_summary.md      <- the competitor page's text: title, price, bullets, FAQ
    bling-ghostface-collection\
      ...
```

`batch_log.csv` in the tool's own folder has one line per product per run.
```

## After Higgsfield: compressing the new images

When you've made the new product images in Higgsfield, save or paste them anywhere inside that product's folder
(for example into `swinging-ghost-decor\`). Then **double-click `compress_images.bat`** in that folder. Every image
in the folder, the downloaded ones and yours, is written to a `compressed\` folder as small WebP files ready for
Shopify. The originals are left untouched. Run it again whenever you add more images; it only does the new ones.

## Getting a product pulled

In ClickUp, open the product's card, make sure **Main Competitor** holds the link to the competitor's product page
(the page with the product photos, not the shop's home page; extra links can go in the description), then move the
card to **ready for lp**. Next time you run `RUN.bat` it's included. Once pulled, the card gets **z-imagesPulled**
ticked and a comment with the folder name. Moving the card on (ready to launch, testing, ...) is up to you.

## If something looks wrong

| The window says | What it means | What to do |
|---|---|---|
| `Python is not installed yet` | Step 1 of setup was skipped or the PATH box wasn't ticked | Reinstall Python, tick **Add python.exe to PATH** |
| `The ClickUp key is missing` | `.env` has no key | Run `SETUP.bat` (or `RUN.bat`) again and paste the key when asked |
| `Google Drive for Desktop is not installed` / `no 'imageGrabber' folder in it` | Drive isn't set up on this computer | Do setup step 4 |
| `could not read ClickUp` | No internet, or the ClickUp key is wrong / expired | Check you're online. Ask for a fresh key and run `SETUP.bat` again |
| `no product link on: ...` | That card is in *ready for lp* but has no competitor link | Put the link in *Main Competitor* on the card |
| `0 products` | No card is in *ready for lp* with a competitor link | Check ClickUp |
| `FAILED: HTTP 404` next to a product | The link on the card is dead | Open it in your browser; fix the link on the card |
| `the bot check was not cleared in time` | A puzzle window opened and wasn't solved within 3 minutes | Run again and solve it |
| `already grabbed` next to every product | Nothing new since last run | That's normal |
| A folder name in another language | The store is foreign and the tool used its title | It's the right product; rename the folder if you like |

Anything else: screenshot the window and send it to whoever gave you the tool.
