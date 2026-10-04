# imageGrabber — how to operate this tool

You are running on a team member's Windows laptop inside the `imageGrabber` folder. The team tracks products
in ClickUp (space *TT - Dropshipping*, list *Product Research*). This tool downloads every image from a
product card's competitor page into the team's shared Google Drive folder, then ticks the card's
`z-imagesPulled` checkbox and posts a comment on it. Python is `py` on this machine.

## What to run

| The person says | Run |
|---|---|
| "grab / pull the images for **X**" (a product name, a ClickUp link, or a card id) | `py imageGrabber.py pull "X"` |
| "pull everything that's ready", "run the queue", "do today's pull" | `py imageGrabber.py batch` (every card in the *ready for lp* column) |
| "pull X again", "redo X" | `py imageGrabber.py pull "X" --redo` |
| "grab the images from this link" (a competitor URL, not in ClickUp) | `py imageGrabber.py grab <url> --name "X"` |
| "compress the images for X" / after Higgsfield images were added to a folder | `py imageGrabber.py compress "X"` |
| "is ClickUp connected", "check the setup" | `py imageGrabber.py clickup-check` |
| "what have we pulled" | `py imageGrabber.py list` |

Run the command and report what it printed: the product, how many images, where they went
(`images go to: ...` is the shared Drive folder), and whether the ClickUp card was ticked and commented.

## Things to know

- Several cards may match a short name; `pull` then lists them and stops. Ask which one, or use the card link.
- A card with no competitor link (empty *Main Competitor* field and no product link in the description) cannot
  be pulled; say so and ask for the link. Research links (TikTok, Instagram, pipiads) are ignored on purpose.
- Etsy and Amazon show a "verify you are human" check: a browser window opens by itself, the person clicks
  through it, and the run continues. Tell the person to solve it and leave the window open. Do not close it.
- The tool never changes a card's status; only the checkbox and a comment. Moving cards between columns is
  the team's job.
- Output goes to the team's Google Drive folder, with a copy in `Desktop\imageGrabber images`. Don't move or rename
  those folders; other laptops rely on them.
- `.env` holds the ClickUp key. Never print it, paste it into ClickUp, or commit it.
- If a command fails, show the last lines it printed; `START_HERE.md` has a table of messages and fixes.
- Don't edit the tool's code on a team laptop; report the problem instead so the tool can be fixed once for everyone.
