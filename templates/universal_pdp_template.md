# Universal PDP Template · Build Guide v1.0

<!-- page 1 -->
UNIVERSAL PDP TEMPLATE · BUILD GUIDE V1.0
The Block-by-Block Product Page
Framework
A 22-block, conversion-first product detail page (PDP) modelled on the reference
landing page. Every block is documented as a stand-alone build card —
reference screenshots, layout, styling tokens, behavior, copy formula, a fully-
filled worked example, and a paste-ready build prompt — so an AI page builder
can construct the page one block at a time with any Shopify product plugged in.
Prepared September 2026 · Works for supplements, skincare, devices, apparel, food & beverage, and more
Demo product used in every worked example: Solace Labs — Nightfall Sleep Gummies (fictional). All statistics, study figures, clinician
counts and review counts in this document are invented placeholders written as finished copy — see Appendix B for the replace-registry.


<!-- page 2 -->
How to use this document
Read this first if you are the AI page builder. This guide is designed to be consumed one block at a time. Do not attempt to
build the whole page from a single pass. Build BLOCK 00, verify it against the screenshot, then move to BLOCK 01, and so
on. Each block card is self-contained: it repeats the design tokens it needs, names the Shopify fields it pulls from, and ends
with a paste-ready build prompt. If you only have the product's Shopify data and this one block card, you have everything
required to build that block.
THE WORKFLOW (FOR THE HUMAN OPERATOR)
1. Fill the Product Brief (page 4) for the product you are testing. Ten minutes. Everything downstream derives from it.
2. Feed the page builder one block card at a time: the screenshot pair + sections 1–8 of the card + the product brief. Ask it
to build only that block.
3. Check the block against the reference screenshot using the QA checklist in Appendix D before moving on.
4. Replace invented numbers: every statistic, study, clinician count, review count and partner name in the worked examples
is fabricated so you can judge the finished quality. Appendix B lists every one of them with a "replace with" instruction.
WHAT IS UNIVERSAL VS. WHAT CHANGES PER PRODUCT
Never changes (the template)
Changes per product (the plug-ins)
Block order, block count, section widths,
card radius, spacing rhythm, button shapes,
tab and accordion patterns, review-card
anatomy, the position and wording pattern
of every CTA, the one-time three-tier offer
(Buy 1 / Buy 2 get 1 free / Buy 3 get 2 free)
with tier 2 pre-selected, the asterisk-
disclaimer convention, the footer.
Product name, images, unit price, variants, the "right for you if" bullets, the value stack
contents, the 6 mechanism steps, the 5 feature icons, the 4–5 stat callouts, the
ingredient/component cards, FAQ questions, the comparison-table rows, the
partner/mission story, and the brand color values (the roles of the colors never change).
BLOCK INDEX
#
Block
Conversion job
#
Block
Conversion job
00
Announcement bar
Offer framing
11
Clinical / performance stats
Proof (quantified)
01
Header / navigation
Orientation
12
Professional endorsement
Authority
02
Hero gallery + title
Attention, offer anchor
13
Ingredient / component cards
Proof (specific)
03
"Right for you if" qualifier
Self-identification
14
Order perks grid
Value reassurance
04
What's included (value stack)
Perceived value
15
Mission / impact
Brand affinity
05
Clinicians' Choice strip
Authority (early)
16
Transparency comparison table
Competitor framing
06
Bundle & Save tier selector
Offer selection
17
UGC photo carousel
Social proof (visual)
07
CTA stack
Conversion
18
Reviews widget
Social proof (volume)
08
Headline + 4 review cards
Social proof (curated)
19
FAQ + help card
Objection handling
09
How it works (6 steps)
Mechanism / belief
20
Cross-sell
AOV
10
Feature icon row
Quality signals
21
Footer
Trust, capture, compliance


<!-- page 3 -->
Blocks marked Conditional are kept when the product has the data to support them, and dropped (never faked with weak content) when it doesn't.
Every other block is required.


<!-- page 4 -->
Global design system
These tokens are referenced by role name in every block. When plugging in a different brand, change the value, never the role.
The reference page is calm, clinical-but-warm, with a lot of off-white surface and one saturated action color; keep that balance.
COLOR ROLES
Navy · --c-ink #24425C
All headlines, body text, dark panels
(endorsement card, savings bar, "not
interested" box), footer-adjacent solids.
Teal · --c-action #50B3A7
The ONLY color used for the Add-to-Cart
button. Nothing else is teal.
Sky blue · --c-accent #6CB4DA
Star ratings, step-number bubbles, progress
bars, "Best Seller" badge, avatar circles,
check icons in the comparison table.
Pink · --c-highlight #EB8AAD
"Savings" amounts in the value stack only.
Communicates money saved. Use sparingly.
Purple · --c-promo #7A76B3
Announcement bar only (and the "Follow on
Shop" button, which is Shopify's own).
Blush surface · --c-surface #FCF8F7
Background of every card, review tile, perk
tile, ingredient card, info box and the full-
width transparency section.
Pale blue · --c-tab #E3F1FA
Selected tab pill background (ingredients
tabs, transparency tabs).
Gold · --c-seal #F0B23A
The "$55 FREE Gifts" starburst seal on the
hero image only.
White · --c-bg #FFFFFF
Page background. Cards sit on white; full-
width tinted bands use --c-surface.
TYPOGRAPHY ROLES
Role
Reference treatment
Where used
Display serif -
-f-display
High-contrast editorial serif (e.g. Tiempos Headline,
Playfair Display, Fraunces). Bold, tight leading (1.05), ink
color. 36–44px desktop / 30–34px mobile.
ONLY three places: the social-proof headline (Block 08),
"Here's how it works" (Block 09), the mission headline
(Block 15). These are the emotional beats of the page.
UI sans --f-
sans
Geometric humanist sans (Inter, Manrope, Plus Jakarta
Sans). Regular 400 for body, Semibold 600 for
labels/prices, Bold 700 for section headlines.
Everything else. Section headlines 28–32px desktop / 24–
26px mobile; body 16px; captions 13–14px; micro-legal
12px.
Serif small-caps
accent
A decorative serif with ornamental brackets, e.g. ❨ ⚕
Clinicians' Choice ❩
Block 05 only (rendered by the third-party clinician-review
widget; replicate if building natively).
SHAPE, SPACING AND ICONOGRAPHY
Radius: cards 16px; hero/gallery 20px; buttons and badges
fully rounded (999px); inputs 10px; small thumbnails 10px.
Section rhythm: 72–96px vertical padding between blocks
on desktop, 48–56px on mobile. Container max-width
1200px, 24px side gutters on mobile.
Cards: no drop shadows. Elevation is expressed by surface
tint (--c-surface on white) or a 1px #E6ECF2 border. Only the
Icons: 1.5px-stroke line icons, navy, inside a 44px circle with
1px navy outline (feature row) or naked (perk tiles). Never
filled/colored icons except the sky-blue verified badge and
check-circles.
Stars: 5 filled sky-blue stars, 18px, tight tracking. Always all
five in curated reviews.


<!-- page 5 -->
buy-box cards use a border.
Buttons: primary = teal pill, white 16px semibold text, 56px
tall, full width in the buy box. Secondary = navy pill. Tertiary
= white pill with 1px navy border ("Show more").
Check marks: thin grey ✓ inside ingredient cards; sky-blue
filled ✓-circle vs. thin navy ✕ in comparison table.
Asterisks: every benefit claim that is not objectively
verifiable ends with * , resolved once by the disclaimer box
in the footer.
GLOBAL PAGE SKELETON (ORDER IS FIXED)
00 Announcement → 01 Header → [02 Gallery | 03 Qualifier → 04 Value stack → 05 Clinicians → 06
Bundle tier selector → 07 CTA stack] → 08 Social proof → 09 How it works → 10 Feature icons → 11
Stats (tinted band) → 12 Endorsement → 13 Ingredients → 14 Perks → 15 Mission → 16 Transparency
(tinted band) → 17 UGC → 18 Reviews → 19 FAQ → 20 Cross-sell → 21 Footer (tinted)
There is no subscription anywhere on the page: every purchase is one-time, through the three-tier bundle selector in Block 06. On desktop, blocks 02
and 03–07 form a two-column sticky layout (gallery left 50%, buy column right 50%, buy column scrolls; gallery sticks). On mobile they stack in
numeric order. Blocks 08 onward are single full-width sections on both.


<!-- page 6 -->
The Product Brief (fill this once per product)
Every block's copy formula references these fields. The demo values below are the ones used in every worked example in this
document. They describe a fictional product.
B1 · Brand name
Solace Labs
B2 · Product name (Shopify title)
Nightfall Sleep Gummies · handle nightfall-sleep-gummies
B3 · Offer (identical on every product)
One-time purchase, three tiers: Buy 1 · Buy 2 get 1 free (default, "FOR BEST RESULTS") · Buy
3 get 2 free ("MOST VALUE"). No subscriptions. Free gifts (if any) ride with tiers 2 and 3.
B4 · Category type
Ingestible supplement (gummy). See Appendix A for other categories.
B5 · Core promise (one line, ≤ 9 words)
Fall asleep faster, wake up clear.
B6 · Primary audience noun
"restless sleepers" (used in headlines: "Over 400,000 restless sleepers…")
B7 · Top 5 pains / desires (customer
language)
1 Lying awake 45+ minutes · 2 Waking at 3am and not getting back to sleep · 3 Grogginess
from melatonin or OTC sleep aids · 4 Racing thoughts at bedtime · 5 Wanting something
non-habit-forming
B8 · Mechanism (how it works, 4–6
steps)
Magnesium bisglycinate calms the nervous system → L-theanine quiets racing thoughts →
tart cherry supplies natural melatonin precursors → apigenin (chamomile) supports deeper
sleep stages → B6 supports the body's own melatonin production → consistent nightly use
resets the sleep rhythm
B9 · Hero components / ingredients (4–
8)
Magnesium Bisglycinate 200mg · L-Theanine 200mg · Tart Cherry Extract 500mg · Apigenin
50mg · Vitamin B6 2mg · Lemon Balm 150mg
B10 · Quality signals (5)
Third-party tested · Melatonin-free & non-habit-forming · Sugar-free (allulose) · Vegan &
gelatin-free · No artificial colors or flavors
B11 · Pricing
Unit $39.99 (compare-at $79.98) · Buy 2 get 1 free $79.98 (value $119.97, −33%) · Buy 3 get
2 free $119.97 (value $199.95, −40%)
B12 · Free gifts (value)
Mulberry-silk sleep mask ($18.00) · Calm Herbal Tea 5-sachet sampler ($12.00) · Nightfall
travel tin ($12.00). Total gift value $42.00. Included with tiers 2 and 3.
B13 · Proof assets (invented for demo)
8-week consumer study, n=212 · 3,184 reviews at 4.8 · 842 clinician endorsements · Dr.
Maya Okafor, PhD sleep scientist quote
B14 · Mission / partner (invented for
demo)
Rest Fund — 120,000+ sleep kits donated to shelters
B15 · Cross-sell products
The Wind-Down Kit (from $58.49) · The Calm Day Kit (from $52.24)
B16 · Compliance mode
Supplement: FDA disclaimer required; all benefit claims asterisked; no disease words (cure,
treat, insomnia as a diagnosis).
Rule for the builder: if a Brief field is empty for a real product, the block that depends on it is dropped, not filled with
generic filler. A missing block is invisible; a weak block is a trust leak.


<!-- page 7 -->
Global copy rules
VOICE
Second person, present tense. "You're experiencing…",
"Your purchase…". The page talks to one person.
Plain, confident, un-hyped. No exclamation marks in brand
copy (reviews may have them). No "revolutionary",
"miracle", "game-changing".
Benefit → mechanism → proof. Every claim on the page
appears in that order somewhere: qualifier (benefit) → how
it works (mechanism) → stats/ingredients (proof).
Sentence-case headlines. Only the first word capitalized
("Here's how it works"). Badges and eyebrows are ALL CAPS.
Numbers are specific. "1,227 clinicians", "6,473 reviews",
"83%". Never "thousands" or "most".
Brand name + ® on first mention in a section, then the plain
product name.
COMPLIANCE CONVENTIONS
Asterisk every structure/function claim ("supports",
"helps", "promotes"). One footer disclaimer resolves all of
them. Non-supplement categories drop the FDA sentence
but keep the asterisk pattern for "results may vary".
Reviews are quoted verbatim, typos included. Curated
reviews may be ellipsized ("…") but never rewritten.
Free-gift legal line appears wherever gifts are shown: "FREE
gifts included with Buy 2 Get 1 Free and Buy 3 Get 2 Free
bundles. Available while supplies last, items subject to
change."
Study language always names the population, duration and
measure: "In an 8-week study of 212 adults, 84%
reported…". Never "clinically proven" without a "Show
studies" link immediately adjacent.
Professional endorsements carry full credentials and the
phrase "without compensation" when true; otherwise
disclose.
REUSABLE MICRO-COPY (VERBATIM ACROSS ALL PRODUCTS)
Slot
Copy
Qualifier heading
This product is right for you if:
Value stack heading
What's included:
Tier selector eyebrow
BUNDLE & SAVE — tiles: Buy 1 / Standard Price · Buy 2 get 1 free / You save 33% · Buy 3 get 2 free
/ You save 40% — header bars: FOR BEST RESULTS · MOST VALUE
CTA button + summary
ADD TO CART · You pay ${tier price} today {struck} · {qty} {units} · {tier name}
Points line
☆ Earn Points with every purchase: Redeem for free products or extra discounts! View my points
Shipping line
Shipping calculated at checkout.
Mechanism headline
Here's how it works
Stats proof link
Scientifically proven: our clinical results — Show studies
Ingredients headline
Scientifically proven ingredients to get you results
Perks headline
Every order comes with more
Transparency headline
Offering you full transparency, always
Reviews headline
Customer reviews
FAQ headline
Frequently Asked Questions
Cross-sell headline
See other bundles (or "Pairs well with" for single products)


<!-- page 8 -->
Footer disclaimer
* These statements have not been evaluated by the Food and Drug Administration. This product
is not intended to diagnose, treat, cure, or prevent any disease.


<!-- page 9 -->


## BLOCK 00 · Announcement bar

Offer framing
Required
What this block does. A single-line, full-width bar above the header that names the offer on this page and its headline value.
It is the first thing read and it pre-frames the price the visitor will see 600px later.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Full viewport width, 40px tall, centered text 14px/600, white
on --c-promo purple.
Entire bar is a link to the offer anchor (#buy-box) — not just
the arrow.
Mobile (≤767px)
Same bar, 44px tall, 13px text, text wraps to max two lines
never truncates.
Dismiss "×" is NOT present in the reference; omit it.
### 2 · ANATOMY & STYLING
Background
--c-promo #7A76B3 (purple — deliberately outside the brand palette so it reads as
"promo", not "brand")
Text
White, 14px, weight 600, letter-spacing 0
Leading emoji
One emoji, category-appropriate (🎁 for gifts, 🌙 for sleep, ✨ for skincare). Exactly one.
Trailing arrow
"→" (U+2192) with a preceding space; not an icon font
### 3 · BEHAVIOR & INTERACTION
Sticky: no. It scrolls away with the page (the header may become sticky; the bar does not).
Click anywhere → smooth-scroll to Block 06.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Formula: {emoji} {Product name}: Buy 2, Get 1 FREE — plus {N} free gifts worth ${gift value} →
Lead with the product name and the universal bundle offer, not the brand.
The bundle offer is identical on every product, so only the product name and gift value change.
If there are no gifts: {emoji} {Product name}: Buy 2, Get 1 FREE — or Buy 3, Get 2 FREE →
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
🌙 Nightfall Sleep Gummies: Buy 2, Get 1 FREE — plus 3 free gifts worth $42 →
### 6 · SHOPIFY DATA SOURCE
Offer name
Product Brief B3
Gift value
Sum of Brief B12 compare-at prices


<!-- page 10 -->
Link target
#buy-box (Block 06 anchor)
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 00 only: a full-width announcement bar above the header. Background #7A76B3, height 
40px desktop / 44px mobile, text centered, white, 14px, semibold. Text: "🌙 Nightfall Sleep 
Gummies: Buy 2, Get 1 FREE — plus 3 free gifts worth $42 →". The whole bar links to #buy-box. Not 
sticky. No close button. Match the reference screenshot's proportions exactly.
### 8 · DO NOT
Do not use the brand teal or navy here; the bar must look like a promo, not navigation.
Do not add a countdown timer or "limited time" language; the reference relies on value, not pressure.
Do not stack multiple messages or rotate messages.


<!-- page 11 -->


## BLOCK 01 · Header / navigation

Orientation
Required
What this block does. A minimal, white, three-zone header: navigation left, centered logo, utility icons right. Its job is to stay
out of the way while signalling a real store (search, account, cart).
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Height 72px, white, 1px bottom border #EEF1F4.
Left: text links "Menu · Products · Bundles" 14px/500 navy,
24px gap.
Center: logo, ~140px wide, absolutely centered.
Right: navy pill button "Take our Quiz" (14px/600, 40px tall)
→ search icon → account icon → bag icon, 20px line icons,
20px gap.
Mobile (≤767px)
Height 64px. Left: hamburger (☰, 24px). Center: logo
~120px. Right: search icon + bag icon.
"Take our Quiz" moves into the drawer menu.
Header becomes sticky on scroll-up (optional, not visible in
reference).
### 2 · ANATOMY & STYLING
Icon style
1.5px stroke, navy, no fills
Logo
Monochrome brand logo, pink/brand mark allowed
Quiz button
The only solid button in the header: --c-ink navy pill, white text
### 3 · BEHAVIOR & INTERACTION
Bag icon shows a count badge (sky blue circle, white number) when cart > 0.
Search icon opens an overlay search; account icon → /account.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Fixed labels. Replace "Bundles" with the store's second-most-important collection (e.g. "Kits", "Sets", "Routines"). "Take our
Quiz" stays if the brand has a quiz; otherwise "Find your product".
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
☰     SOLACE LABS     🔍 👜   (desktop: Menu · Products · Bundles  |  logo  |  [Take our Quiz] 🔍 👤 👜)
### 6 · SHOPIFY DATA SOURCE
Logo
Shopify theme settings → logo
Nav links
Main menu (limit to 3 top-level items)
Cart count
cart.item_count


<!-- page 12 -->
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 01 only: a white 72px header (64px mobile) with a 1px #EEF1F4 bottom border. Desktop: 
left text links "Menu", "Products", "Bundles" (14px navy #24425C); logo perfectly centered 
(~140px); right side a navy pill button "Take our Quiz" then search, account and bag line icons 
(20px, 1.5px stroke). Mobile: hamburger left, logo center, search + bag right. Bag shows a small 
sky-blue #6CB4DA count badge when the cart is not empty. Match the reference screenshots.
### 8 · DO NOT
Do not add a mega-menu, promo text, or a second nav row.
Do not color the icons; navy line icons only.
Do not make the header taller than 72px — it competes with the hero.


<!-- page 13 -->


## BLOCK 02 · Hero gallery + product title

Attention · offer anchor
Required
What this block does. The left column (desktop) / first screen (mobile). Title + type badge, then a large square-ish hero image
with a navy headline strip baked into its top edge, then a horizontal thumbnail strip with a scroll-progress bar. The first image
is a composed "flat-lay of everything you get" with a gold value seal — not a plain packshot.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Left column, 50% of a 1200px container (~580px). Sticky
(top: 96px) while the right column scrolls.
Title is NOT in this column on desktop — it sits at the top of
the right column (Block 03). This column is image-only on
desktop.
Main image: 580×~500px, radius 20px, background #F4F1F0
(light warm grey). Navy strip across the top: 48px tall, white
18px/600 text, centered.
Thumbnails: 8 tiles, 64×64px, radius 10px, 10px gap, 1px
border #E6ECF2; selected tile has 2px navy border. Below: a
3px track with a navy progress fill proportional to scroll
position.
Mobile (≤767px)
Order: title row (H1 28px/700 left + badge right) → hero
image full-bleed within 16px gutters, radius 16px →
thumbnail strip (5.5 tiles visible, 72px, horizontal swipe) →
progress bar.
The hero image itself is swipeable; thumbnails sync.
### 2 · ANATOMY & STYLING


<!-- page 14 -->
Type badge
Navy pill, white 11px/700 uppercase: BUNDLE / BEST SELLER / NEW / KIT. Right-aligned to
the title baseline.
Image 1 (mandatory composition)
Flat-lay of product + every free gift, each labelled with a small navy caption ("FREE Exclusive
Tote Bag*"), plus a gold starburst seal reading "${value} FREE Gifts". A one-line legal
footnote in 9px grey at the image bottom.
Images 2–8 (recommended sequence)
2 "How these products work together" infographic · 3 packshot of gifts · 4 review-quote card
on a color background · 5 "This works" stat card on navy · 6 lifestyle/model shot · 7
supplement-facts / spec panel · 8 clinician / press card
Headline strip
Overlaid on image 1 only. Pattern: "{Product}: Buy 2, Get 1 FREE" (+ " + {N} FREE Gifts" when
gifts exist). The universal offer is on the image itself.
### 3 · BEHAVIOR & INTERACTION
Click thumbnail → swap main image with 200ms crossfade.
Main image supports pinch-zoom on mobile and click-to-lightbox on desktop.
Progress bar width = (current index + 1) / total.
Video tiles show a ▶ overlay and autoplay muted when selected.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Title: Shopify product title verbatim. Badge: BUNDLE if it contains ≥2 products; otherwise BEST SELLER if it is the store's top SKU;
otherwise NEW.
Strip formula: {Product name}: Buy 2, Get 1 FREE + {N} FREE Gifts — identical structure on every product. Seal
formula: ${gift value}\nFREE\nGifts . Image captions: FREE {Gift name}* and {N} FREE {Sample name}* .
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
TITLE ROW
Nightfall Sleep Gummies   BEST SELLER
IMAGE 1 HEADLINE STRIP (NAVY)
Nightfall Sleep Gummies: Buy 2, Get 1 FREE + 3 FREE Gifts
IMAGE 1 CAPTIONS
FREE Mulberry-Silk Sleep Mask* · 5 FREE Calm Tea Sachets* · FREE Limited Edition Travel Tin* · Gold seal: "$42 FREE
Gifts" · Footnote: *FREE gifts included with Buy 2 Get 1 Free and Buy 3 Get 2 Free bundles. FREE gifts only available
while supplies last — items subject to change.
THUMBNAILS 2–8
2 "How Nightfall works while you sleep" infographic · 3 gift packshot · 4 quote card: "Asleep in 20 minutes instead of an
hour. No grogginess." ★★★★★ · 5 navy card: "THIS WORKS — 84% fell asleep faster in 14 days*" · 6 model holding jar,
blue backdrop · 7 Supplement Facts panel · 8 "Recommended by 842 clinicians" card
### 6 · SHOPIFY DATA SOURCE


<!-- page 15 -->
Title
product.title
Badge
product.tags contains "bundle" → BUNDLE; "bestseller" → BEST SELLER
Images
product.media in order; alt text = caption
Gift value
metafield offer.gift_value
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 02 only: the product gallery. Desktop: this is the left 50% column of a two-column 
layout, sticky at top:96px. Main image 580px wide, radius 20px, light warm grey background, with a 
48px navy #24425C strip across the top containing white 18px semibold centered text "Our #1 Sleep 
Gummy For Deeper Rest + 3 FREE Gifts". Below it a row of eight 64px thumbnails (radius 10px, 1px 
#E6ECF2 border, selected = 2px navy border) and a 3px navy scroll-progress bar. Mobile: first 
render a title row — H1 "Nightfall Sleep Gummies" 28px bold navy left, navy pill badge "BEST 
SELLER" right — then the image (radius 16px, 16px gutters), then a swipeable thumbnail strip with 
the progress bar. Image 1 must be a flat-lay of three jars (the Buy 2 Get 1 Free quantity) plus the 
three free gifts with small navy captions and a gold starburst seal "$42 FREE Gifts". Use the 
product's media in order.
### 8 · DO NOT
Do not use a plain white packshot as image 1 — the flat-lay with labelled gifts and the gold seal is what sells the value.
Do not put price or reviews in this column on desktop.
Do not add arrows over the main image on desktop; thumbnails are the navigation.


<!-- page 16 -->


## BLOCK 03 · "This product is right for you if" qualifier

Self-identification
Required
What this block does. Top of the buy column (desktop) / directly under the gallery (mobile). Five square-bulleted "You…"
statements that let the visitor diagnose themselves, a grey serving-size box, and two underlined utility links (facts panel,
reviews). This is the highest-leverage copy on the page: the visitor should nod at three of the five lines.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Right column top. H1 title 28px/600 + navy badge on the
same line (desktop only; on mobile the title lives in Block
02).
Sub-heading "This product is right for you if:" 14px/700,
16px below title.
Five bullets, 14px/400, 8px apart, small square navy bullets
(■ 6px), text wraps under text not under bullet.
Serving box: full column width, --c-surface , 8px radius,
12px padding, 13px text.
Two links row: 14px underlined navy, 32px gap.
Mobile (≤767px)
Same stack, bullets 17px/400 with 14px spacing; serving box
15px text; links 17px.
Heading is 20px/700.
### 2 · ANATOMY & STYLING
Bullet glyph
Filled square ■, navy, 6px, vertically centered on the first line
Asterisks
Every bullet ends with * (structure/function claims)
Serving box
Pattern: "1 {unit} = {N} servings of each product + exclusive bonus items"
Links
"View Supplement Facts" (opens modal) · "Read reviews" (scrolls to Block 18). For non-
supplements: "View specifications" / "Size guide" / "Ingredients list".
### 3 · BEHAVIOR & INTERACTION
"View Supplement Facts" opens a modal with the facts panel image + full ingredient list.


<!-- page 17 -->
"Read reviews" smooth-scrolls to Block 18.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Bullet formula (write exactly five):
1 · Symptom now: "You're experiencing {pain 1 in customer words}*"
2 · Pattern / history: "You've experienced recurring {pain 2}*"
3 · Situation / lifestyle trigger: "You're {activity or life situation that causes the problem}*"
4 · Aspiration (adjacent benefit): "You're looking to support {secondary benefit}*"
5 · Holistic goal: "You want to {bigger outcome that combines benefits}*"
Each ≤ 12 words. Use the exact vocabulary from Brief B7. Quote a colloquialism in quotes if customers use it ("intimate",
"wired but tired").
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
TITLE + BADGE (DESKTOP)
Nightfall Sleep Gummies   BEST SELLER
This product is right for you if:
You're lying awake 45 minutes or more before falling asleep*
You've experienced recurring 3 a.m. wake-ups you can't shake*
You're "wired but tired" at bedtime from screens, stress, or late work*
You're looking to support calmer evenings without melatonin grogginess*
You want to reset your sleep rhythm and wake up clear-headed*
1 jar = 30 servings · Buy 2 get 1 free = 90 servings + exclusive bonus items
View Supplement Facts      Read reviews
### 6 · SHOPIFY DATA SOURCE
Title/badge
product.title, product.tags
Bullets
metafield pdp.right_for_you (list of 5 strings)
Serving line
metafield pdp.serving_line
Facts panel
metafield pdp.facts_image
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 03 only: the top of the buy column. Desktop: H1 "Nightfall Sleep Gummies" 28px navy 
semibold with a navy pill badge "BEST SELLER" right-aligned on the same row (mobile: omit the title 
row, it is already in Block 02). Then bold 14px "This product is right for you if:" and five 
bullets with small filled square navy bullets: "You're lying awake 45 minutes or more before 
falling asleep*", "You've experienced recurring 3 a.m. wake-ups you can't shake*", "You're "wired 
but tired" at bedtime from screens, stress, or late work*", "You're looking to support calmer 
evenings without melatonin grogginess*", "You want to reset your sleep rhythm and wake up clear-
headed*". Then a #FCF8F7 rounded box: "1 jar = 30 servings · Buy 2 get 1 free = 90 servings + 


<!-- page 18 -->
exclusive bonus items". Then two underlined navy links side by side: "View Supplement Facts" (opens 
a modal) and "Read reviews" (scrolls to the reviews block). Match the reference spacing.
### 8 · DO NOT
Do not write feature bullets ("Contains 200mg magnesium") here — this block is about the reader, not the product.
Do not exceed five bullets or use check marks; square bullets are the signature.
Do not put the price here; the value stack (Block 04) earns the price first.


<!-- page 19 -->


## BLOCK 04 · What's included

(value stack)
Perceived value
Conditional (shown when the selected tier includes free gifts, or the product is a multi-item kit)
What this block does. A blush card listing every item in the offer with a thumbnail, a one-line benefit, the item name, and a
right-aligned price column showing compare-at (struck), the actual price (or "FREE"), and a pink "$X Savings" line. A navy
footer bar totals the savings. It converts "$79.98 for a bundle" into "$161.97 of stuff".
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Full buy-column width. Card: --c-surface , radius 16px,
20px padding. Heading "What's included:" 15px/700.
Rows: 48px thumbnail (radius 10px, tinted background
matching the item's pack color) · text column (12px grey
benefit line above, 14px/600 navy name below) · price
column right-aligned, 96px wide.
Footer bar: navy, radius 0 0 16px 16px, 14px/600 white
"Discount code savings:" left, 16px/700 total right.
Mobile (≤767px)
Identical structure; thumbnails 60px; benefit line 14px;
name 16px/600; price column 110px.
Footer bar text 17px.
### 2 · ANATOMY & STYLING
Price column
Line 1: compare-at in grey 12px strikethrough (+ "FREE" bold navy on the same line for
gifts). Line 2: actual price 14px/700 navy (omitted for gifts). Line 3: "${diff} Savings" 12px
pink --c-highlight .
Legal lines
Two grey 12px lines under the rows: (1) which tiers include gifts; (2) gift availability terms.
Ordering
Paid products first (highest price first), then gifts (highest value first).


<!-- page 20 -->
### 3 · BEHAVIOR & INTERACTION
Row 1 recomputes when the visitor switches tier in Block 06 (× 1 / × 3 / × 5 units and the matching struck value).
The gift rows (and the whole card, if there are no kit components) appear only while tier 2 or 3 is selected; selecting Buy 1
collapses them with a 200ms height transition.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Row formula: benefit line = For {outcome 1}, {outcome 2}, and {outcome 3} (≤ 8 words); name = product title without
brand. Gift benefit lines describe use, not hype ("Urinary Tract health + hydration", "Stainless steel premium gua sha"). Total =
Σ(compare-at − price).
For a product with no free gifts and no kit components, drop this block entirely; the tier tiles in Block 06 already carry the value
story.
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
What's included:
🟦
For faster sleep onset, fewer wake-ups, and clear mornings
Nightfall Sleep Gummies × 3 (Buy 2 get 1 free)
$119.97
$79.98
$39.99 Savings
⬜
Blocks light for deeper sleep stages
Mulberry-Silk Sleep Mask
$18.00 FREE
$18.00 Savings
🟩
Caffeine-free wind-down ritual
5 Calm Herbal Tea Sachets
$12.00 FREE
$12.00 Savings
⬛
Limited edition, keeps 10 gummies fresh
Nightfall Travel Tin
$12.00 FREE
$12.00 Savings
FREE gifts are included with Buy 2 get 1 free and Buy 3 get 2 free bundles.
FREE gifts are available only while supplies last, items are subject to change.*
Bundle + gift savings:
$81.99
### 6 · SHOPIFY DATA SOURCE
Rows
Bundle components (Shopify Bundles app) or metafield offer.items [{title, benefit,
image, compare_at, price, is_gift}]
Total
Computed client-side
Recurring note
metafield offer.recurring_note
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 04 only: a "What's included:" value-stack card in the buy column. Card background 
#FCF8F7, radius 16px, 20px padding. Four rows, each with a 48px rounded thumbnail (tinted 
background), a grey 12px benefit line above a navy 14px semibold item name, and a right-aligned 
price column. Row 1: "For faster sleep onset, fewer wake-ups, and clear mornings" / "Nightfall 
Sleep Gummies × 3 (Buy 2 get 1 free)" / $119.97 struck, $79.98, pink "$39.99 Savings". Row 2: 


<!-- page 21 -->
"Blocks light for deeper sleep stages" / "Mulberry-Silk Sleep Mask" / $18.00 struck + "FREE", pink 
"$18.00 Savings". Row 3: "Caffeine-free wind-down ritual" / "5 Calm Herbal Tea Sachets" / $12.00 
struck + FREE, "$12.00 Savings". Row 4: "Limited edition, keeps 10 gummies fresh" / "Nightfall 
Travel Tin" / $12.00 struck + FREE, "$12.00 Savings". Under the rows, grey 12px: "FREE gifts are 
included with Buy 2 get 1 free and Buy 3 get 2 free bundles." and "FREE gifts are available only 
while supplies last, items are subject to change.*". Finish with a navy #24425C footer bar (bottom 
corners 16px) reading "Bundle + gift savings:" left and "$81.99" right in white. Pink = #EB8AAD.
### 8 · DO NOT
Do not show a "total value" without the per-row savings; the line-by-line math is what makes the total believable.
Do not use icons instead of real thumbnails of each item.
Do not hide the "recurring order includes only…" line; it prevents chargebacks and builds trust.


<!-- page 22 -->


## BLOCK 05 · Clinicians' Choice strip

Authority (early)
Conditional (needs a real professional-endorsement source)
What this block does. A compact bordered card between the value stack and the plan selector: an ornamental serif label,
one sentence quantifying professional endorsement with a "Learn more" link, and a row of three clinician avatars beside
"Read their reviews ›". In the reference this is a third-party widget (FrontrowMD); replicate its look natively if the brand has
any verifiable professional endorsements.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Full buy-column width, white card, 1px #E6ECF2 border,
radius 12px, 16px padding, thin grey scrollbar hint on the
right edge (the widget is a scroll container).
Line 1: "❨ ⚕ Clinicians' Choice ❩" 16px serif.
Line 2: 13px, bold count, italic source name, underlined
"Learn more".
Line 3: three overlapping 24px circular avatars + "Read their
reviews ›" 14px/600.
Mobile (≤767px)
Same; text 15px; avatars 28px.
### 2 · ANATOMY & STYLING
Serif label
Decorative serif with bracket ornaments; use a real serif font, not an image
Count
Bold, comma-formatted integer
Source
Italic platform name
Avatars
Real headshots, 2px white ring, overlap −8px
### 3 · BEHAVIOR & INTERACTION
"Learn more" → tooltip/modal explaining the endorsement program.
"Read their reviews ›" → opens the clinician-review panel (widget) or scrolls to Block 12.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Formula: {N} clinicians, including {most relevant specialty}, share this on {platform} without
compensation. Learn more . Category adaptations: dermatologists (skincare) · physiotherapists (devices) · registered
dietitians (food) · "professional stylists" (apparel — rename the label "Stylists' Choice").
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT


<!-- page 23 -->
❨ ⚕ Clinicians' Choice ❩
842 clinicians, including sleep specialists, share this on FrontrowMD without compensation. Learn more
◉◉◉  Read their reviews ›
### 6 · SHOPIFY DATA SOURCE
Count / platform
metafield proof.clinician_count , proof.clinician_platform
Avatars
metafield proof.clinician_avatars (3 images)
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 05 only: a white bordered card (1px #E6ECF2, radius 12px, 16px padding) in the buy 
column. Line 1 in a serif font, 16px: "❨ ⚕ Clinicians' Choice ❩". Line 2, 13px navy: "842 
clinicians" in bold, then ", including sleep specialists, share this on " then "FrontrowMD" in 
italics then " without compensation. " then an underlined "Learn more" link. Line 3: three 
overlapping 24px circular headshot avatars followed by "Read their reviews ›" in 14px semibold. 
Match the reference.
### 8 · DO NOT
Do not include this block with an invented count on a live page — it is the one block where fabrication is a legal risk. Fill it only
from a real program.
Do not style it in teal or pink; it is deliberately neutral so it reads as third-party.


<!-- page 24 -->


## BLOCK 06 · Bundle & Save tier selector

Offer selection
Required
What this block does. The pricing card. Three side-by-side quantity tiers — Buy 1 / Buy 2 Get 1 Free / Buy 3 Get 2 Free —
with the middle tier pre-selected and labelled "FOR BEST RESULTS", the third labelled "MOST VALUE". Each tile shows a
stacked packshot (1, 3 or 5 units), the tier name, a saving line, the price and a struck full value. One-time purchase only: there
is no subscription option anywhere on the page. This offer is identical on every product; only the unit price changes.
Reference · DESKTOP
Reference for this block (replaces the reference page's subscribe-first selector). The ADD TO CART button shown belongs to Block 07. Mobile keeps the
same three tiles side by side.
### 1 · LAYOUT
Desktop (≥1024px)
Card region full buy-column width. Eyebrow: a thin 1px line
with centered uppercase label "BUNDLE & SAVE" (13px/700,
letter-spacing .06em, navy) breaking the line.
Three tiles, equal width, 12px gap, radius 12px, 1px
#DCE3E9 border, 16px padding, content centered. Tile 1 has
no header bar. Tiles 2 and 3 carry a full-width header bar
(36px, --c-ink navy, radius 12px 12px 0 0, white 12px/700
uppercase): "FOR BEST RESULTS" / "MOST VALUE".
Selected tile (tile 2 by default): 2px --c-ink border + --
c-tab pale tint fill.
Tile content: packshot cluster (1 / 3 / 5 units, 64px tall) →
tier name 18px/700 → saving line 14px grey ("Standard
Price" / "You save 33%" / "You save 40%") → price 22px/700
--c-ink → struck full value 15px grey.
Mobile (≤767px)
Tiles stay side by side at all widths (min tile width ~104px).
Packshot 48px; tier name 15px/700; saving line 12px; price
17px/700; struck value 12px; header bars 11px text.


<!-- page 25 -->
16px below the tiles the CTA stack (Block 07) begins —
nothing sits between them.
### 2 · ANATOMY & STYLING
Tier names
Fixed: "Buy 1" · "Buy 2 get 1 free" · "Buy 3 get 2 free"
Header bars
Fixed: none · "FOR BEST RESULTS" · "MOST VALUE"
Default selection
Tile 2 — always
Price math
Tier 2 = 2 × unit price, struck 3 × unit (33% off). Tier 3 = 3 × unit, struck 5 × unit (40% off).
Tier 1 = unit price; struck value only if Shopify compare_at_price is set — never invent one.
Free gifts
If the product has free gifts (Block 04), they are included with tiers 2 and 3; the tile saving
line becomes "You save 33% + free gifts".
Colors
Tiles use navy for selection and prices (NOT pink — pink is reserved for the value-stack
savings). Teal appears only on the Add-to-cart button in Block 07.
### 3 · BEHAVIOR & INTERACTION
Click tile → select; the summary line under the Block 07 button and the Block 04 value stack (if present) update.
Selection persists on the sticky ATC.
Tier quantity is passed as line-item quantity (1 / 3 / 5) with the bundle discount applied automatically (Shopify Function /
bundle app), not as three separate SKUs.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Eyebrow: fixed "BUNDLE & SAVE". Tier copy (fixed): tile 1 "Buy 1 / Standard Price"; tile 2 "Buy 2 get 1 free / You save 33%"; tile 3
"Buy 3 get 2 free / You save 40%". Only the numbers are product-specific: price = unit × {1 | 2 | 3} and struck =
unit × {1 (only if compare-at exists) | 3 | 5} . Units word comes from the product ("jar", "bottle", "pair", "pack").
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
BUNDLE & SAVE
[1 jar]
Buy 1
Standard Price
$39.99
$79.98
FOR BEST RESULTS
[3 jars]
Buy 2 get 1 free
You save 33%
$79.98
$119.97
MOST VALUE
[5 jars]
Buy 3 get 2 free
You save 40%
$119.97
$199.95
### 6 · SHOPIFY DATA SOURCE
Unit price
product.selectedVariant.price
Compare-at (tile 1 only)
variant.compare_at_price — omit the strike if null


<!-- page 26 -->
Tier discounts
Automatic discount / Shopify Function: qty 3 → 1 free (33%), qty 5 → 2 free (40%); tiles pass
quantity 1 / 3 / 5
Units word
metafield offer.unit_word ("jar")
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 06 only: a "BUNDLE & SAVE" tier selector. Start with a thin horizontal rule broken by 
the centered uppercase label "BUNDLE & SAVE" (13px bold navy #24425C, letter-spacing .06em). Then 
three equal-width tiles side by side (12px gap, radius 12px, 1px #DCE3E9 border, centered content) 
— they must stay side by side on mobile too. Tile 1: a single jar packshot, "Buy 1" (18px bold), 
"Standard Price" (14px grey), "$39.99" (22px bold navy), "$79.98" struck in grey. Tile 2 is 
selected by default: 2px navy border, pale-blue #E3F1FA fill, and a full-width navy header bar 
across its top reading "FOR BEST RESULTS" in white 12px bold uppercase; content: a cluster of three 
jars, "Buy 2 get 1 free", "You save 33%", "$79.98", "$119.97" struck. Tile 3: navy header bar "MOST 
VALUE", a cluster of five jars, "Buy 3 get 2 free", "You save 40%", "$119.97", "$199.95" struck. 
Nothing else in this block — no subscription or refill option of any kind. Clicking a tile selects 
it and updates the price summary in Block 07. Do not use teal or pink anywhere in this block.
### 8 · DO NOT
Do not pre-select "Buy 1" or "Buy 3" — tile 2 is the intended default on every product.
Do not invent a struck price on the Buy 1 tile; use the real compare-at or show none.
Do not add a subscription / refill / "subscribe & save" option anywhere; the page is one-time purchase only.
Do not stack the tiles vertically on mobile; shrink them.


<!-- page 27 -->


## BLOCK 07 · CTA stack

Conversion
Required
What this block does. The action cluster under the tier selector: a full-width teal ADD TO CART button (uppercase, heavy,
hard shadow) with a one-line price summary beneath it, a loyalty points line, an HSA/FSA eligibility badge, and the shipping
line. Every element is centered and stacked with decreasing visual weight. Purchase is one-time only, so there is no "buy
once" or subscription link here.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Button: full buy-column width, 64px, teal pill, 20px/800
uppercase white "ADD TO CART", with a 4px hard offset
shadow in --c-ink (as in the bundle reference image).
10px below: 14px navy "You pay $79.98 today" + grey struck
"$119.97" + grey "· 3 jars · Buy 2 get 1 free" (updates with
the selected tier).
20px below: ☆ + 13px/600 "Earn Points with every
purchase:" then 12px grey line with underlined "View my
points".
16px below: HSA|FSA badge (~150px wide logo lockup). 8px
below: 12px "Shipping calculated at checkout."
Mobile (≤767px)
Identical, button 56px, 17px text. Consider a sticky bottom
bar (56px, teal button + price) appearing after the visitor
scrolls past this block — not in the reference but standard
practice; keep it optional.
### 2 · ANATOMY & STYLING
Button label
Fixed "ADD TO CART" — the price lives in the summary line, not the button
Summary line
You pay ${tier price} today ${struck value} · {qty} {units} ·
{tier name}
HSA/FSA
Only for eligible products (supplements often via Flex/TrueMed). Otherwise replace with
payment icons row (Shop Pay, Apple Pay) or omit.
Points line
Requires a loyalty app; otherwise omit both lines
### 3 · BEHAVIOR & INTERACTION
Click → adds the selected tier quantity (1 / 3 / 5) with the automatic bundle discount; opens the cart drawer; button shows a
600ms "ADDED ✓" state.


<!-- page 28 -->
Summary line updates instantly on any Block 06 change.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Fixed micro-copy (see Global copy rules). Only the numbers change in the summary line: You pay ${tier price} today
${struck} · {qty} {units} · {tier name} .
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
ADD TO CART
You pay $79.98 today $119.97 · 3 jars · Buy 2 get 1 free
☆ Earn Points with every purchase:
Redeem for free products or extra discounts! View my points
✔ HSA | FSA Powered by flex
Shipping calculated at checkout.
### 6 · SHOPIFY DATA SOURCE
Price
selected tier quantity × variant price with the automatic bundle discount
Struck value
tier quantity × unit price (3× or 5×)
Points
Loyalty app snippet
HSA/FSA
metafield offer.hsa_eligible boolean
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 07 only: the CTA stack under the bundle selector, everything centered. A full-width 
64px teal #50B3A7 pill button with white 20px extra-bold uppercase text "ADD TO CART" and a 4px 
hard offset shadow in navy #24425C. Below it a 14px line: "You pay $79.98 today" in navy, "$119.97" 
struck in grey, then "· 3 jars · Buy 2 get 1 free" in grey; this line updates whenever a tier 
changes in Block 06. Then a star glyph and 13px semibold "Earn Points with every purchase:" with a 
second grey line "Redeem for free products or extra discounts! View my points" (link underlined). 
Then an "HSA | FSA · Powered by flex" badge lockup about 150px wide, and finally 12px "Shipping 
calculated at checkout." with "Shipping" underlined. Add-to-cart opens the cart drawer.
### 8 · DO NOT
Do not add a second button (e.g. "Buy now" / PayPal) beside Add to cart; one button, one color.
Do not show "in stock" counters or urgency timers.
Do not put the price inside the button — the summary line beneath it carries the numbers.
Do not add any subscription or "buy once" link.


<!-- page 29 -->


## BLOCK 08 · Social-proof headline + 4 curated reviews

Social proof (curated)
Required
What this block does. The first full-width section after the buy box. A big serif headline quantifying the customer base, then
four blush review cards: five sky-blue stars, a bold title, a verbatim (ellipsized) body, and an avatar + name + "Verified Buyer
✓" footer. The four reviews are hand-picked to cover the four strongest objections.
Reference · MOBILE
Reference · DESKTOP
Mobile crop shown as three side-by-side strips of one continuous scroll.
### 1 · LAYOUT
Desktop (≥1024px)
Container 1200px. Headline left-aligned, display serif
40px/700 navy, max-width 720px.
4 cards in one row, 20px gap, equal height, --c-surface ,
radius 16px, 24px padding.
Card: stars (5×16px sky blue) → title 14px/700 → body
14px/400 (line-height 1.5, 8–12 lines) → footer: 32px avatar
circle (sky blue, white initials) + name 13px/600 + "Verified
Buyer" 13px + sky-blue verified badge.
Mobile (≤767px)
Headline 32px, wraps to two lines.
Cards stack vertically full width, 16px gap; stars 18px; body
17px; avatar 44px.
No carousel — all four are visible by scrolling (they double
as long-form copy on mobile).
### 2 · ANATOMY & STYLING
Stars
Always five, filled, --c-accent
Ellipsis
Use "…" to cut reviews; never paraphrase
Avatar
Initials on sky-blue circle; real photos not used here (they are in Block 17)
Verified badge
Sky-blue rosette with white check, 16px
### 3 · BEHAVIOR & INTERACTION
Static on desktop. On mobile, cards are static too (no swipe).
Optional: clicking a card scrolls to Block 18.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Headline formula: Over {round customer count} {audience noun} have already found {relief | results |
their fit} . Review selection rule — one card each for: (1) "nothing else worked" skeptic · (2) long-suffering, life-changed · (3)
graphic before/after symptoms in raw language · (4) speed of result + prevention. Title = the reviewer's own title. Keep 60–110
words per body.


<!-- page 30 -->
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Over 400,000 restless sleepers have already found their off switch
★★★★★
Nothing else worked
I started these a month ago after nearly 2 years of trying
everything… Melatonin left me foggy, and the
prescription stuff scared me. With Nightfall I was asleep
within about 20 minutes on night three and I haven't had
a 3 a.m. wake-up since. I finally feel like myself in the
morning.
◉ Priya R. · Verified Buyer ✔
★★★★★
Don't keep looking. This is the one.
This changed my life. I had been struggling… for 7+ years.
Sleep trackers, white noise, blackout curtains, hopeless
products and dollars and endless research and then I
found Solace… Y'all, the first week I took these,
everything changed…
◉ Marcus T. · Verified Buyer ✔
★★★★★
Truly a freaking LIFESAVER
I would lie there with my heart pounding and my brain
replaying the whole day, if not that then I'd wake at 3
and stare at the ceiling till 5… Since taking these the
racing thoughts are almost completely gone, I'm not
waking up in the night, and I don't feel drugged in the
morning like I did with melatonin.
◉ Xiomara G. · Verified Buyer ✔
★★★★★
Best money I've ever spent.
So, I have had broken sleep basically the entire time I've
been working nights… IT WORKS LIKE MAGIC! It not only
fixed my sleep within 4 days, it keeps me on a rhythm
even on my days off. I've stopped dreading bedtime.
◉ Monica A. · Verified Buyer ✔
### 6 · SHOPIFY DATA SOURCE
Headline count
metafield proof.customer_count
Reviews
metafield proof.featured_reviews (4 review IDs from the reviews app) — title, body,
author, verified
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 08 only: a full-width white section (1200px container, 80px vertical padding). Headline 
in a bold editorial serif, 40px desktop / 32px mobile, navy #24425C, left-aligned: "Over 400,000 
restless sleepers have already found their off switch". Below, four equal-height review cards in 
one row on desktop (stacked on mobile), background #FCF8F7, radius 16px, 24px padding. Each card: 
five filled sky-blue #6CB4DA stars, a bold 14px title, a 14px body, then a footer with a 32px sky-
blue circle showing initials, the name in semibold, "Verified Buyer" and a sky-blue verified 
rosette icon. Use these four reviews verbatim: (1) Title "Nothing else worked" — "I started these a 
month ago after nearly 2 years of trying everything… Melatonin left me foggy, and the prescription 
stuff scared me. With Nightfall I was asleep within about 20 minutes on night three and I haven't 
had a 3 a.m. wake-up since. I finally feel like myself in the morning." — Priya R., Verified Buyer. 
(2) Title "Don't keep looking. This is the one." — "This changed my life. I had been struggling… 
for 7+ years. Sleep trackers, white noise, blackout curtains, hopeless products and dollars and 
endless research and then I found Solace… Y'all, the first week I took these, everything changed…" 
— Marcus T., Verified Buyer. (3) Title "Truly a freaking LIFESAVER" — "I would lie there with my 
heart pounding and my brain replaying the whole day, if not that then I'd wake at 3 and stare at 


<!-- page 31 -->
the ceiling till 5… Since taking these the racing thoughts are almost completely gone, I'm not 
waking up in the night, and I don't feel drugged in the morning like I did with melatonin." — 
Xiomara G., Verified Buyer. (4) Title "Best money I've ever spent." — "So, I have had broken sleep 
basically the entire time I've been working nights… IT WORKS LIKE MAGIC! It not only fixed my sleep 
within 4 days, it keeps me on a rhythm even on my days off. I've stopped dreading bedtime." — 
Monica A., Verified Buyer. No carousel, no arrows.
### 8 · DO NOT
Do not show 4.3-star reviews here; curated cards are all five stars (the honest distribution lives in Block 18).
Do not add photos to these cards.
Do not center the headline; left-aligned serif is the signature of this section.


<!-- page 32 -->


## BLOCK 09 · How it works — 6-step mechanism timeline

Mechanism / belief
Required
What this block does. The belief-building section. Centered serif headline + a 2–3 line intro that names the components and
the connection between them, then a two-column layout: a lifestyle photo (models holding the product) left, and a vertical
timeline of six numbered steps right — each with a bold title and a 60–80 word paragraph. Alternating filled/outlined
number bubbles are joined by a thin vertical line.
Reference · MOBILE
Reference · DESKTOP
Mobile crop shown as three side-by-side strips.
### 1 · LAYOUT
Desktop (≥1024px)
Headline centered, display serif 36px. Intro centered, 15px,
max-width 760px, navy.
Row: image 46% (radius 16px, sticky top:120px while steps
scroll) · 54% timeline with 48px left padding.
Timeline: 1.5px vertical line #DCE9F3 running full height at
x=16px. Number bubbles 32px on the line: odd steps filled -
-c-accent with white number, even steps white with
1.5px pale-blue border and pale-blue number. Step title
16px/600; body 14px/400 grey-navy; 40px between steps.
Mobile (≤767px)
Headline 30px; intro 17px centered.
Image full width (radius 16px) ABOVE the timeline.
Timeline line at x=36px; bubbles 44px; title 18px/600; body
17px. Steps run the full mobile width.
### 2 · ANATOMY & STYLING
Bubble rhythm
Filled, outlined, filled, outlined, filled, filled — the last step is always filled (the "you win"
step)
Image
Two people, product in hand, flat pastel background (sky blue), radius 16px
Asterisks
Every step body ends with *


<!-- page 33 -->
### 3 · BEHAVIOR & INTERACTION
Optional scroll-spy: bubble fills as its step reaches the viewport center.
Image sticks on desktop only.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Intro formula: Our {Brand}® {Offer} combines {N} {powerhouse formulas | components} designed to {core
promise}. By pairing {A} with {B}, you're addressing {primary outcome} while simultaneously
supporting {secondary outcome} — because {A-system} and {B-system} are deeply connected.
Six-step arc (fixed): 1 first component acts on root cause → 2 second component removes the obstacle → 3 rebalancing /
repopulating → 4 strengthening / protecting → 5 body's own mechanism restored → 6 whole-system outcome + "consistent use
maintains it". Titles ≤ 6 words, verb-led ("We eliminate…", "Your whole system flourishes").
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Here's how it works
Our Solace Labs® Deep Sleep Starter Kit is built around one powerhouse formula designed to work with your body's own sleep chemistry.
By pairing chelated magnesium with L-theanine, tart cherry and apigenin, you're addressing how fast you fall asleep while simultaneously
supporting how deeply you stay asleep — because sleep onset and sleep depth are deeply connected.
① Magnesium calms the nervous system
Nightfall's magnesium bisglycinate is bound to glycine, an amino acid your body already uses to lower core temperature
and settle the nervous system at night. Unlike magnesium oxide, it's gentle on the stomach and absorbed efficiently, so
it reaches the neurons that regulate your sleep-wake switch. Calming the nervous system means calming bedtime.*
② We quiet the racing mind
L-theanine, the amino acid found in green tea, promotes alpha-wave brain activity — the relaxed-but-awake state you
feel in the minutes before drifting off. It takes the edge off the mental replay of your day without sedation, creating the
perfect conditions for sleep to begin naturally.*
③ We supply natural sleep signals
Studies show tart cherry is one of the richest food sources of melatonin precursors and anthocyanins. Rather than
flooding your system with synthetic melatonin, Nightfall gives your body the raw materials to produce its own, in the
amount and rhythm it's designed for.*
④ We deepen the restorative stages
Apigenin, the calming flavonoid in chamomile, binds to the same receptors that govern slow-wave sleep — the stage
where muscle repairs, memory consolidates and cortisol resets. More time in deep sleep is why a Nightfall night feels
longer than the clock says.*
⑤ Your own rhythm takes over
Vitamin B6 and lemon balm support the enzymes that convert tryptophan into serotonin and melatonin each evening.
As your natural production strengthens, you rely less on the gummy and more on your restored circadian rhythm — the
opposite of habit-forming.*


<!-- page 34 -->
⑥ Your whole day flourishes
You've achieved consistent, deep sleep without grogginess. This dual-action approach addresses the root cause of most
restless nights: a nervous system that can't downshift. Consistent nightly use helps maintain this rhythm and supports
your body's natural ability to rest and recover.*
### 6 · SHOPIFY DATA SOURCE
Intro
metafield pdp.how_intro
Steps
metafield pdp.how_steps list of {title, body} ×6
Image
metafield pdp.how_image
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 09 only: "Here's how it works" section. Centered headline in bold editorial serif (36px 
desktop / 30px mobile, navy), then a centered 15px intro paragraph (max-width 760px): "Our Solace 
Labs® Deep Sleep Starter Kit is built around one powerhouse formula designed to work with your 
body's own sleep chemistry. By pairing chelated magnesium with L-theanine, tart cherry and 
apigenin, you're addressing how fast you fall asleep while simultaneously supporting how deeply you 
stay asleep — because sleep onset and sleep depth are deeply connected.". Below, on desktop, a two-
column row: left 46% a lifestyle photo (radius 16px, sticky while the right column scrolls); right 
54% a vertical timeline with a 1.5px pale-blue #DCE9F3 line and 32px numbered bubbles — steps 1, 3, 
5 and 6 filled sky-blue #6CB4DA with white numbers, steps 2 and 4 white with a pale-blue border and 
pale-blue number. Each step: 16px semibold title and a 14px body, 40px apart. On mobile the image 
sits full-width above the timeline and bubbles are 44px with 18px titles / 17px bodies. Use the six 
steps exactly as written: 1 "Magnesium calms the nervous system" — "Nightfall's magnesium 
bisglycinate is bound to glycine, an amino acid your body already uses to lower core temperature 
and settle the nervous system at night. Unlike magnesium oxide, it's gentle on the stomach and 
absorbed efficiently, so it reaches the neurons that regulate your sleep-wake switch. Calming the 
nervous system means calming bedtime.*" 2 "We quiet the racing mind" — "L-theanine, the amino acid 
found in green tea, promotes alpha-wave brain activity — the relaxed-but-awake state you feel in 
the minutes before drifting off. It takes the edge off the mental replay of your day without 
sedation, creating the perfect conditions for sleep to begin naturally.*" 3 "We supply natural 
sleep signals" — "Studies show tart cherry is one of the richest food sources of melatonin 
precursors and anthocyanins. Rather than flooding your system with synthetic melatonin, Nightfall 
gives your body the raw materials to produce its own, in the amount and rhythm it's designed for.*" 
4 "We deepen the restorative stages" — "Apigenin, the calming flavonoid in chamomile, binds to the 
same receptors that govern slow-wave sleep — the stage where muscle repairs, memory consolidates 
and cortisol resets. More time in deep sleep is why a Nightfall night feels longer than the clock 
says.*" 5 "Your own rhythm takes over" — "Vitamin B6 and lemon balm support the enzymes that 
convert tryptophan into serotonin and melatonin each evening. As your natural production 
strengthens, you rely less on the gummy and more on your restored circadian rhythm — the opposite 
of habit-forming.*" 6 "Your whole day flourishes" — "You've achieved consistent, deep sleep without 
grogginess. This dual-action approach addresses the root cause of most restless nights: a nervous 
system that can't downshift. Consistent nightly use helps maintain this rhythm and supports your 
body's natural ability to rest and recover.*". Every body ends with an asterisk.
### 8 · DO NOT
Do not reduce to 3 steps or use icons instead of numbers; six numbered beats are the pattern.
Do not use a packshot as the image — people holding the product.


<!-- page 35 -->
Do not write feature-speak ("contains 200mg"); each step explains a cause-and-effect.


<!-- page 36 -->


## BLOCK 10 · Feature icon row (5 quality signals)

Quality signals
Required
What this block does. A quiet palate-cleanser between the mechanism story and the hard stats: five outlined line icons, each
with a short title and a one-line explanation. It answers "is this well made?" in three seconds.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Five columns, equal width, centered content, 1200px
container, 64px vertical padding, white background.
Icon: 44px circle, 1px navy outline, 20px line glyph inside.
Title 14px/500 navy below (12px gap). Description 12px
grey, max 2 lines, centered.
Mobile (≤767px)
Vertical list, left-aligned: icon (48px circle) left, title
18px/500 + description 15px grey right. 28px between rows.
Thin 1px divider (#EEF1F4) under the list before the next
tinted band.
### 2 · ANATOMY & STYLING
Icon set
Consistent 1.5px stroke set (e.g. Phosphor Thin / Lucide). Circle outline is part of the
component, not the glyph.
Count
Exactly five
### 3 · BEHAVIOR & INTERACTION
Static.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Title formula: 2–4 words, noun-led, no verbs ("Science-backed ingredients", "Delayed-release capsules"). Description: ≤ 9 words,
starts with a participle or adjective ("Validated through…", "Engineered for…", "Safe for…"). Draw from Brief B10. Category
swaps: skincare → "Dermatologist tested / Fragrance-free / Non-comedogenic / Cruelty-free / Recyclable packaging"; device →
"Medical-grade materials / 2-year warranty / USB-C rechargeable / Whisper-quiet motor / Free returns".
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT


<!-- page 37 -->
🧪 Third-party tested
Every batch verified for purity and potency.
🌙 Melatonin-free formula
Non-habit-forming, no morning grogginess.
🍬 Sugar-free gummies
Sweetened with allulose, zero glycemic impact.
🌱 Vegan & gelatin-free
Pectin-based, ethical ingredients you can trust.
🚫 No artificial stuff
Pure formulations without colors, flavors or preservatives.
### 6 · SHOPIFY DATA SOURCE
Items
metafield pdp.features list of {icon, title, text} ×5
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 10 only: a five-item feature row. Desktop: five equal centered columns in a 1200px 
container with 64px vertical padding; each has a 44px circle with a 1px navy #24425C outline 
containing a 20px thin line icon, then a 14px navy title and a 12px grey description (max 2 lines). 
Mobile: a left-aligned vertical list, icon left (48px circle), 18px title and 15px description 
right, 28px between rows, ending with a 1px #EEF1F4 divider. Items: "Third-party tested — Every 
batch verified for purity and potency." / "Melatonin-free formula — Non-habit-forming, no morning 
grogginess." / "Sugar-free gummies — Sweetened with allulose, zero glycemic impact." / "Vegan & 
gelatin-free — Pectin-based, ethical ingredients you can trust." / "No artificial stuff — Pure 
formulations without colors, flavors or preservatives." Use flask, moon, candy, leaf and crossed-
syringe style icons.
### 8 · DO NOT
Do not use colored or filled icons.
Do not give this section a heading; it is intentionally headless.
Do not stretch to 6–8 items; five fits one row.


<!-- page 38 -->


## BLOCK 11 · Clinical / performance stats

band
Proof (quantified)
Required (drop to a single stat if data is thin)
What this block does. A full-width blush band with a centered headline, then two columns of "big number" stat callouts. The
left column carries two percentage stats with explanatory paragraphs and sky-blue progress bars; the right column carries
three "word" stats ("Over 5x", "Helps", "Supports") with paragraphs, then a bordered "Scientifically proven — Show studies"
card and a lifestyle photo. The typography does the persuading: 56px numbers.
Reference · MOBILE
Reference · DESKTOP
Mobile crop shown as three side-by-side strips.
### 1 · LAYOUT
Desktop (≥1024px)
Band background --c-surface , 80px vertical padding.
Headline centered 30px/600 navy, two lines max.
Two columns, 48% / 48%, 4% gap. Left: stat A, stat B, then
"Scientifically proven" card. Right: stats C, D, E, then image
(radius 16px, 4:3).
Stat anatomy: number 56px/700 navy inline with a
16px/600 label that wraps under it; then 13px/400
paragraph (max-width 460px); then for percentage stats a
10px progress bar (track #EEE, fill --c-accent , width =
percentage, radius 5px), 20px below.
"Scientifically proven" card: white, 1px #E6ECF2, radius
10px, centered: sky-blue rosette icon + 14px "Scientifically
proven: our clinical results" + underlined "Show studies".
Mobile (≤767px)
Single column in this order: headline → A → B → C → D → E
→ studies card → image.
Number 48px; label 17px; paragraph 15px; progress bar
12px tall, 70% width.
### 2 · ANATOMY & STYLING


<!-- page 39 -->
Number treatment
Percentages "83%" · multipliers "Over 5x" · verbs "Helps" / "Supports" — the last two are
used when no number exists but the benefit still deserves a big-type callout
Label
Runs on from the number in one sentence; asterisked
Progress bar
Only under percentage stats; width equals the percentage
### 3 · BEHAVIOR & INTERACTION
"Show studies" → opens a modal listing study citations (title, journal/year or "internal consumer study", n, duration).
Progress bars animate from 0 to value on first viewport entry (600ms ease-out).
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Headline formula: Supports {primary outcome} and {whole-body / everyday} {benefit} from the inside out
(or "…in every wear" / "…every wash" for non-ingestibles). Stat set (fixed shape): A = % improved primary outcome in {duration}
· B = % reduced symptom · C = multiplier ("Over {N}x {measure}") · D = "Helps {verb phrase}" · E = "Supports {verb phrase}".
Paragraph formula: {Component} {mechanism}. In a {duration} study of {n} {population}, {N}% reported
{outcome}.*
All numbers below are invented for the demo. Appendix B lists them.
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Supports faster sleep and clear-headed mornings from the inside out
84% fell asleep faster within 14 nights, taking
Nightfall's magnesium + L-theanine complex*
Our chelated magnesium and L-theanine pairing has been shown
to support the nervous system's nightly downshift. In an 8-week
consumer study of 212 adults with occasional sleeplessness, 84%
reported falling asleep faster within the first two weeks.*
71% reported fewer night-time wake-ups*
Helps promote uninterrupted rest and supports your body's
natural sleep cycles. In the same study, 71% of participants noted
fewer 3 a.m. wake-ups by week four.*
✔ Scientifically proven: our clinical results
Show studies
Over 3x magnesium absorption
Magnesium bisglycinate supports muscle relaxation and nervous-
system balance. With over 3× the bioavailability of magnesium
oxide, adults experienced greater support with a smaller,
stomach-friendly dose.*
Helps quiet a racing mind at bedtime
L-theanine supports alpha-wave activity that eases the transition
from wakefulness, helping you let go of the day without sedation
or next-day fog.*
Supports deeper, more restorative sleep stages
By supporting slow-wave sleep and your own melatonin rhythm,
this kit helps create the optimal internal environment for both
nightly recovery and daytime focus.*
[Lifestyle photo: two friends laughing on a pink backdrop, 4:3]
### 6 · SHOPIFY DATA SOURCE
Stats
metafield proof.stats list of {number, label, body, bar_pct?} ×5


<!-- page 40 -->
Studies
metafield proof.studies (list rendered in modal)
Image
metafield proof.image
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 11 only: a full-width band with background #FCF8F7 and 80px vertical padding. Centered 
30px navy headline "Supports faster sleep and clear-headed mornings from the inside out". Two 
columns (48/48). LEFT: stat "84%" (56px bold navy) followed inline by the bold 16px label "fell 
asleep faster within 14 nights, taking Nightfall's magnesium + L-theanine complex*", then a 13px 
paragraph "Our chelated magnesium and L-theanine pairing has been shown to support the nervous 
system's nightly downshift. In an 8-week consumer study of 212 adults with occasional 
sleeplessness, 84% reported falling asleep faster within the first two weeks.*", then a 10px sky-
blue #6CB4DA progress bar at 84% width on a #EEE track; then stat "71%" / "reported fewer night-
time wake-ups*" / paragraph "Helps promote uninterrupted rest and supports your body's natural 
sleep cycles. In the same study, 71% of participants noted fewer 3 a.m. wake-ups by week four.*" / 
bar at 71%; then a white bordered card, centered: sky-blue rosette icon, "Scientifically proven: 
our clinical results", underlined "Show studies" (opens a modal). RIGHT: "Over 3x" / "magnesium 
absorption" / "Magnesium bisglycinate supports muscle relaxation and nervous-system balance. With 
over 3× the bioavailability of magnesium oxide, adults experienced greater support with a smaller, 
stomach-friendly dose.*"; "Helps" / "quiet a racing mind at bedtime" / "L-theanine supports alpha-
wave activity that eases the transition from wakefulness, helping you let go of the day without 
sedation or next-day fog.*"; "Supports" / "deeper, more restorative sleep stages" / "By supporting 
slow-wave sleep and your own melatonin rhythm, this kit helps create the optimal internal 
environment for both nightly recovery and daytime focus.*"; then a 4:3 lifestyle photo with radius 
16px. Mobile: single column in the order headline, 84%, 71%, Over 3x, Helps, Supports, studies 
card, image; numbers 48px. Bars animate from 0 on scroll into view.
### 8 · DO NOT
Do not use charts or donut graphics; giant type + a thin bar is the whole visual language.
Do not put "clinically proven" anywhere without the adjacent "Show studies" link.
Do not invent numbers on a live page — use this block's demo numbers only to judge the layout.


<!-- page 41 -->


## BLOCK 12 · Professional endorsement card

Authority
Conditional (needs a real, credentialed quote)
What this block does. A single navy card with a circular headshot, an all-caps eyebrow "RECOMMENDED BY
PROFESSIONALS", a 2–3 sentence quote in large white type, and a credential line. On desktop it is a wide horizontal card; on
mobile a tall centered card. It is the only dark-background content block, which is why it feels like a signature.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
1200px container, card background --c-ink navy, radius
16px, 48px padding, 64px top/bottom section spacing.
Layout: 120px circular headshot left (white 3px ring) · text
right: eyebrow 12px/700 white uppercase letter-spacing
.08em → quote 18px/600 white, max-width 720px →
credential 12px #CFE8F7 two lines (name + credentials /
"about {product}").
Mobile (≤767px)
Card full width within 16px gutters, 32px padding, text left-
aligned.
Headshot 180px centered at top; eyebrow 14px; quote
22px/500; credential 14px.
### 2 · ANATOMY & STYLING
Quote marks
Typographic straight quotes as part of the text ("…")
Headshot
Real person in scrubs / lab coat / uniform on a neutral background
Credential
Line 1: role prefix + name + post-nominals ("NP, Liana Baixauli, APRN, FNP-BC"); line 2:
"about {Brand} {Product}"
### 3 · BEHAVIOR & INTERACTION
Static. If multiple quotes exist, a subtle dot-pager below the credential — otherwise none.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Quote formula (30–45 words): {Audience} who have struggled with {problem} have finally found {lasting
result} with this product. For many, it's the first time they've felt a noticeable improvement.


<!-- page 42 -->
{Personal skeptic-to-believer line}. Category adaptations: dermatologist (skincare), physiotherapist / chiropractor
(devices, ergonomics), chef / RD (food), master tailor / stylist (apparel — eyebrow becomes "RECOMMENDED BY EXPERTS").
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
◯ [headshot]
RECOMMENDED BY PROFESSIONALS
"Patients who have struggled with restless sleep for years have finally found a routine that holds with
this product. For many, it's the first time they've slept through the night without feeling drugged the
next day. I was skeptical of a gummy, but the results speak for themselves."
Dr. Maya Okafor, PhD, Sleep Scientist
about Solace Labs Nightfall Sleep Gummies
### 6 · SHOPIFY DATA SOURCE
Quote
metafield proof.expert_quote {image, eyebrow, quote, name, about}
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 12 only: one navy #24425C card (radius 16px) in a 1200px container with 64px section 
spacing. Desktop: 48px padding, a 120px circular headshot with a 3px white ring on the left; on the 
right an eyebrow "RECOMMENDED BY PROFESSIONALS" (12px bold white, letter-spacing .08em), the quote 
in 18px semibold white (max-width 720px): "Patients who have struggled with restless sleep for 
years have finally found a routine that holds with this product. For many, it's the first time 
they've slept through the night without feeling drugged the next day. I was skeptical of a gummy, 
but the results speak for themselves.", and two lines in 12px pale blue #CFE8F7: "Dr. Maya Okafor, 
PhD, Sleep Scientist" / "about Solace Labs Nightfall Sleep Gummies". Mobile: full-width card, 32px 
padding, 180px headshot centered at the top, then eyebrow 14px, quote 22px, credential 14px, all 
left-aligned.
### 8 · DO NOT
Do not use stock headshots or an unnamed "Dr. Smith"; this block is unusable without a real, credentialed person.
Do not add stars or a rating to the card.
Do not use a second dark card anywhere else on the page; this one must stay unique.


<!-- page 43 -->


## BLOCK 13 · Ingredient / component cards with filter tabs

Proof (specific)
Required
What this block does. Centered headline, a horizontal row of filter tabs (All + 4–5 benefit categories), then a 3-column grid of
blush cards. Each card: a small photo of the ingredient/component, its name, a "+" expand button, and 2–3 grey check-mark
benefit lines. Six cards are visible, the rest behind a "Show more" pill. Tabs filter the grid.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Headline centered 30px/600. Tabs centered: pills 13px, 8px
14px padding; selected = --c-tab pale blue background +
navy text; others grey text on transparent. 24px gap below.
Grid 3 columns, 20px gap. Card: --c-surface , radius
16px, 20px padding. Header row: 28px ingredient photo
(circular crop, real texture photo not an icon) + name
15px/600 + 36px white circular "+" button at right. Benefit
lines: 13px grey with thin grey ✓, 6px apart.
"Show more" white pill, 1px navy border, centered, 32px
below the grid.
Mobile (≤767px)
Headline 26px. Tabs scroll horizontally (left-aligned, with a
3px grey track underneath as a scroll hint). Cards stack, full
width; 3rd card fades to white at the bottom (gradient
mask) to signal "more" before the "Show more" pill.
### 2 · ANATOMY & STYLING


<!-- page 44 -->
Photo
Macro photo of the raw material (powder, leaf, crystal) cropped in a circle
Check lines
Every line ends with *
"+" button
Expands the card inline to show a 40–60 word explanation + dose
### 3 · BEHAVIOR & INTERACTION
Tab click → filter cards with 200ms fade; "All" restores.
"+" → accordion-expand in place; "−" collapses.
"Show more" → reveals remaining cards, then hides itself.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Tabs: "All" + the 4–5 benefit categories from the product's outcomes (Brief B7/B8). Card name: the scientific / material name
customers can Google ("Lactobacillus rhamnosus", "Magnesium Bisglycinate", "Grade-5 titanium", "Merino 17.5 micron").
Benefit lines: 2–3, verb-led, ≤ 5 words: "Restores…", "Balances…", "Protects against…". Expanded text: {What it is}. {What
it does in this product}. {Dose or spec}.
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Scientifically proven ingredients to get you results
All   Sleep onset   Sleep quality   Stress & calm   Recovery   Mood
◉ Magnesium Bisglycinate ⊕
✓ Calms the nervous system*
✓ Supports muscle relaxation*
✓ Gentle on the stomach*
◉ L-Theanine ⊕
✓ Quiets racing thoughts*
✓ Promotes alpha-wave relaxation*
◉ Tart Cherry Extract ⊕
✓ Natural melatonin precursors*
✓ Supports sleep duration*
✓ Aids overnight recovery*
◉ Apigenin (Chamomile) ⊕
✓ Supports slow-wave sleep*
✓ Eases bedtime tension*
◉ Vitamin B6 ⊕
✓ Supports melatonin production*
✓ Helps regulate mood*
✓ Supports dream recall*
◉ Lemon Balm ⊕
✓ Traditionally used for calm*
✓ Supports restful sleep*
✓ Eases occasional stress*
[ Show more ] → reveals: Glycine, Passionflower
EXPANDED CARD EXAMPLE
Magnesium Bisglycinate — 200mg
A chelated form of magnesium bound to glycine. In Nightfall it supports the nervous system's nightly downshift and muscle relaxation, with
over 3× the absorption of magnesium oxide and none of the digestive upset. 200mg per serving.*
### 6 · SHOPIFY DATA SOURCE
Cards
metafield pdp.ingredients list of {name, image, tags[], benefits[], detail, dose}
Tabs
Derived from the union of tags
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)


<!-- page 45 -->
Build BLOCK 13 only: centered 30px navy headline "Scientifically proven ingredients to get you 
results". Under it a centered row of pill tabs — "All" (selected: pale-blue #E3F1FA background, 
navy text), "Sleep onset", "Sleep quality", "Stress & calm", "Recovery", "Mood" (grey text). On 
mobile the tabs scroll horizontally with a thin grey track below. Then a 3-column grid (stacked on 
mobile) of cards, background #FCF8F7, radius 16px, 20px padding: a 28px circular macro photo of the 
ingredient, its name in 15px semibold, a 36px white circular "+" button on the right, and 2–3 lines 
of 13px grey text with thin grey check marks. Cards: "Magnesium Bisglycinate" (Calms the nervous 
system* / Supports muscle relaxation* / Gentle on the stomach*), "L-Theanine" (Quiets racing 
thoughts* / Promotes alpha-wave relaxation*), "Tart Cherry Extract" (Natural melatonin precursors* 
/ Supports sleep duration* / Aids overnight recovery*), "Apigenin (Chamomile)" (Supports slow-wave 
sleep* / Eases bedtime tension*), "Vitamin B6" (Supports melatonin production* / Helps regulate 
mood* / Supports dream recall*), "Lemon Balm" (Traditionally used for calm* / Supports restful 
sleep* / Eases occasional stress*). Show six, then a centered white pill button "Show more" with a 
1px navy border that reveals two more (Glycine, Passionflower). Tabs filter the grid; "+" expands 
the card inline with a 40–60 word detail and the dose. On mobile the third card fades out at the 
bottom before the Show more button.
### 8 · DO NOT
Do not use generic icons for ingredients; the small real-texture photo is what makes it feel scientific.
Do not show doses on the collapsed card — keep it scannable; doses live in the expansion.
Do not remove the tabs even if there are only six cards; they communicate breadth.


<!-- page 46 -->


## BLOCK 14 · Order perks grid

Value reassurance
Required
What this block does. A left-aligned headline and six blush tiles in a 3×2 grid, each with a thin line icon, a bold title and a
one-line description. It restates everything a customer gets beyond the product itself — guarantee, shipping, points, gifts —
4,000px after the buy box, for the visitor who is still weighing the price.
Reference · MOBILE
Reference · DESKTOP
Reference layout; the reference copy is subscription-oriented — replace with the one-time-purchase perks below.
### 1 · LAYOUT
Desktop (≥1024px)
Headline left-aligned 30px/600 navy. Grid 3 columns × 2
rows, 20px gap. Tile: --c-surface , radius 16px, 24px
padding, icon (28px, 1.5px stroke, navy, naked — no circle)
top-left with title 16px/600 to its right, description 13px
grey under the title.
Mobile (≤767px)
Headline 26px. Tiles stack full width, 12px gap; icon 28px;
title 17px; description 15px.
### 2 · ANATOMY & STYLING
Tile count
Six, always
Icons
shield-check, box, star, calendar-check, jar, gift
### 3 · BEHAVIOR & INTERACTION
Static. Optionally the headline links back to Block 06.


<!-- page 47 -->
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Headline: fixed — "Every order comes with more". Six perk slots (fixed order): 1 money-back guarantee · 2 free shipping
threshold · 3 loyalty points · 4 early access · 5 samples / exclusives · 6 free gifts with bundles. Title ≤ 6 words, description ≤ 10
words. Swap only a perk that does not exist (then use "Cancel or change your order within 1 hour" or "Priority support, 7 days a
week").
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
🛡 60-day money-back guarantee
Not sleeping better? Full refund, even on
an empty jar.
📦 Free U.S. shipping on bundles
Every Buy 2 get 1 free and Buy 3 get 2 free
order ships free.
☆ Earn points for product + merch
Get rewarded with every purchase and
redeem for exciting items.
📅 Early access to deals + new
products
Be the first to discover and save on the
latest launches.
🫙 Exclusive NEW product samples
Try new products before anyone else, on
us!
🎁 Free gifts with every bundle
$42 of sleep essentials included with tiers
2 and 3.
### 6 · SHOPIFY DATA SOURCE
Perks
Theme setting (store-wide, not per product) order.perks ×6; tile 6 text pulls
offer.gift_value
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 14 only: left-aligned 30px navy headline "Every order comes with more", then a 3×2 grid 
(stacked on mobile) of tiles with background #FCF8F7, radius 16px, 24px padding. Each tile has a 
28px thin navy line icon at top-left, a 16px semibold title beside it and a 13px grey description 
below. Tiles: "60-day money-back guarantee — Not sleeping better? Full refund, even on an empty 
jar." (shield-check icon) / "Free U.S. shipping on bundles — Every Buy 2 get 1 free and Buy 3 get 2 
free order ships free." (box) / "Earn points for product + merch — Get rewarded with every purchase 
and redeem for exciting items." (star) / "Early access to deals + new products — Be the first to 
discover and save on the latest launches." (calendar-check) / "Exclusive NEW product samples — Try 
new products before anyone else, on us!" (jar) / "Free gifts with every bundle — $42 of sleep 
essentials included with tiers 2 and 3." (gift). No mention of subscriptions.
### 8 · DO NOT
Do not add a button here; the CTA is the buy box.
Do not circle the icons (that treatment belongs to Block 10).
Do not mention subscriptions, autoship or refills.


<!-- page 48 -->


## BLOCK 15 · Mission / impact section

Brand affinity
Conditional (needs a real partner or program)
What this block does. A two-column emotional beat: "In partnership with {logo}" eyebrow, a serif headline, one paragraph
with a bold impact number, a navy "Learn more" pill — and on the right a documentary photo with a navy stat overlay chip
("1M+ Women and children supported…"). It turns the purchase into a small act of generosity.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
1200px container, 96px vertical padding, white. Left 42%:
eyebrow 13px grey "In partnership with" + partner logo
(24px tall) → headline display serif 34px/700 → paragraph
14px with the impact number in bold → navy pill "Learn
more" (40px, 14px/600). Right 54%: photo 4:3, radius 16px,
with a navy chip (radius 8px, 14px padding) in the top-right
corner: "1M+" 24px/700 + 12px two-line caption; partner
watermark bottom-left.
Mobile (≤767px)
Stack: eyebrow+logo → headline 34px → paragraph 17px →
full-width "Learn more" pill (48px) → photo full width with
the chip.
### 2 · ANATOMY & STYLING
Headline
The most human line on the page, in the display serif
Chip
Navy, white text, semi-transparent 92%
Photo
Documentary, warm, people — never product


<!-- page 49 -->
### 3 · BEHAVIOR & INTERACTION
"Learn more" → partner page.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Headline formula: Your purchase improves your {benefit}, and someone else's, too. Paragraph: Customers
like you have helped {bold impact number + noun} {get what}, through our partnership with {Partner}.
Your {self-care | choice} ripples outward. Chip: {number}+ / {who} supported through {what} .
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
In partnership with ✦ Rest Fund
Your purchase improves your sleep, and someone else's, too.
Customers like you have helped over 120,000 people in shelters receive a warm sleep kit — a blanket, pillow and eye mask — through our
partnership with Rest Fund. Your self-care ripples outward.
Learn more
[Photo: volunteer handing a folded blanket to a smiling woman; navy chip top-right: 120K+ "Sleep kits delivered to shelters across the
U.S."]
### 6 · SHOPIFY DATA SOURCE
Partner
Theme setting mission.partner_name/logo/url
Impact number
Theme setting mission.impact_count
Photo
Theme setting mission.image
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 15 only: a two-column section (white, 96px vertical padding, 1200px container). Left 
42%: grey 13px "In partnership with" followed by the partner logo "Rest Fund" (24px tall); a bold 
editorial serif headline 34px navy "Your purchase improves your sleep, and someone else's, too."; a 
14px paragraph "Customers like you have helped over 120,000 people in shelters receive a warm sleep 
kit — a blanket, pillow and eye mask — through our partnership with Rest Fund. Your self-care 
ripples outward." with "over 120,000 people in shelters" in bold; a navy pill button "Learn more". 
Right 54%: a 4:3 documentary photo, radius 16px, with a navy chip in the top-right corner reading 
"120K+" (24px bold) and "Sleep kits delivered to shelters across the U.S." (12px), plus a small 
partner watermark bottom-left. Mobile: stack in that order with a full-width button.
### 8 · DO NOT
Do not fabricate a partner on a live page; drop the block instead.
Do not show the product in the photo.
Do not use teal for "Learn more" — teal is reserved for purchase actions.


<!-- page 50 -->


## BLOCK 16 · Transparency comparison table

Competitor framing
Required
What this block does. A full-width blush band: centered headline, three pill tabs (Label / Quality / Manufacturing
transparency), a short paragraph, then a comparison table with two image column headers — "us" (product photo on navy)
vs "other products in the market" (grey icon) — and 8 rows of sky-blue ✓ vs thin ✕. The last two rows break the pattern with
text answers ("Earthy flavor", "Third-party") to keep it credible.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Band --c-surface , 80px padding. Headline centered
30px/600. Tabs centered (same style as Block 13).
Under tabs: left column (40%) with tab title 20px/600 + 14px
paragraph; right column (60%) holds the two 120×120
column-header tiles right-aligned: tile 1 navy with product
photo, tile 2 white with a grey "other products" line icon +
10px uppercase caption "OTHER PRODUCTS IN THE
MARKET".
Mobile (≤767px)
Headline 26px; tabs horizontal-scroll; paragraph 16px;
header tiles 48px, right-aligned above the columns; rows
56px, label 16px, columns 44px each.


<!-- page 51 -->
Table: full width, rows 48px, 1px #E6ECF2 dividers, label
14px navy left; columns 2–3 centered, each 120px wide
aligned under the header tiles. ✓ = 20px sky-blue filled
circle with white check; ✕ = 20px thin navy cross; text cells
13px grey.
### 2 · ANATOMY & STYLING
Rows
Exactly 8: six binary, one text-vs-text, one link-vs-text ("Our cGMP Facility ⓘ" vs "Third-
party")
Tabs
Each tab swaps the paragraph AND the rows
### 3 · BEHAVIOR & INTERACTION
Tab click swaps paragraph + rows with fade.
"Our cGMP Facility ⓘ" → tooltip with facility details.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Paragraph formula (Label tab): Each and every one of our products is carefully formulated with the highest
quality {materials}, at their {science-backed dosages | proven specifications}. While our {blends |
designs} are proprietary, we still believe in full transparency. Every {ingredient | material} we
add makes its way to the label, so you know exactly what's inside. Rows: the 6 "free-from / built-with"
attributes competitors typically fail, phrased as the customer's wish ("No fillers & binders", "No added middleman's cut"); row 7
a subjective attribute with an honest competitor descriptor; row 8 "Manufacturing".
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Offering you full transparency, always
Label Transparency   Quality Transparency   Manufacturing Transparency
Label Transparency
Each and every one of our products is carefully formulated with the highest quality ingredients, at their science-backed dosages. While our
blends are proprietary, we still believe in full transparency. Every ingredient we add makes its way to the label, so you know exactly what's
inside.
🟦 Nightfall
⬜ OTHER PRODUCTS IN THE MARKET
Melatonin-free & non-habit-forming
●✓
✕
Sugar-free & vegan
●✓
✕
Clinically dosed (200mg chelated magnesium)
●✓
✕
No added middleman's cut
●✓
✕
No artificial sweeteners, colors or flavors
●✓
✕
Third-party tested every batch
●✓
✕
Better flavor
●✓
Chalky aftertaste


<!-- page 52 -->
Manufacturing
Our cGMP Facility ⓘ
Third-party
Quality tab paragraph: "Every batch of Nightfall is tested by an independent ISO 17025 lab for potency, heavy metals, microbes and pesticides
before it ships. We publish the certificate of analysis for every lot — scan the QR code on your jar to see yours." Rows swap to: COA published
per lot · Heavy-metal tested · Potency verified at expiry · Allergen screened · Pesticide screened · Microbial screened · Shelf-life: 24 months vs 12
months · Testing: In-house + independent vs Undisclosed.
Manufacturing tab paragraph: "Nightfall is made in our own cGMP-certified, FDA-registered facility in Boulder, Colorado — not a white-label
contract plant. That means we control sourcing, batching and packaging end to end." Rows: Made in the USA · Own facility · Small-batch (≤5,000
units) · Full ingredient traceability · Recyclable glass jar · Carbon-neutral shipping · Lead time: 14 days vs 90+ days · Ownership: Brand-owned vs
Contract manufacturer.
### 6 · SHOPIFY DATA SOURCE
Tabs + rows
metafield pdp.transparency {tab, paragraph, rows[{label, us, them}]} ×3
Header image
product featured image
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 16 only: a full-width band, background #FCF8F7, 80px vertical padding. Centered 30px 
navy headline "Offering you full transparency, always". Centered pill tabs: "Label Transparency" 
(selected, #E3F1FA background), "Quality Transparency", "Manufacturing Transparency". Then a row: 
left 40% with the tab title "Label Transparency" (20px semibold) and the paragraph "Each and every 
one of our products is carefully formulated with the highest quality ingredients, at their science-
backed dosages. While our blends are proprietary, we still believe in full transparency. Every 
ingredient we add makes its way to the label, so you know exactly what's inside."; right 60% with 
two 120px square header tiles right-aligned — a navy tile with the product photo, and a white tile 
with a grey line icon and the caption "OTHER PRODUCTS IN THE MARKET" (10px uppercase). Below, a 
full-width table with 48px rows, 1px #E6ECF2 dividers, the label in 14px navy on the left and two 
120px centered columns aligned under the tiles. Rows: "Melatonin-free & non-habit-forming" ✓/✕, 
"Sugar-free & vegan" ✓/✕, "Clinically dosed (200mg chelated magnesium)" ✓/✕, "No added middleman's 
cut" ✓/✕, "No artificial sweeteners, colors or flavors" ✓/✕, "Third-party tested every batch" ✓/✕, 
"Better flavor" ✓ / "Chalky aftertaste", "Manufacturing" "Our cGMP Facility ⓘ" / "Third-party" — ✓ 
is a 20px sky-blue #6CB4DA filled circle with a white check, ✕ is a thin navy cross, text cells are 
13px grey; row 8's "Our cGMP Facility ⓘ" is an underlined link with a tooltip. Tabs swap paragraph 
and rows. Mobile: tabs scroll horizontally, header tiles shrink to 48px, columns 44px.
### 8 · DO NOT
Do not name a competitor brand; "other products in the market" is the pattern.
Do not make all eight rows ✓/✕ — the two text rows are what make the table believable.
Do not use red for ✕.


<!-- page 53 -->


## BLOCK 17 · UGC photo carousel

Social proof (visual)
Required
What this block does. A horizontal strip of real customer photos (product in bathrooms, hands, shelves, selfies) with circular
arrow buttons, followed by the centered "Customer reviews" headline that introduces Block 18. Imperfect, phone-shot
photos are the point.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
1200px container, 64px top padding. 5 square tiles visible
(200px), 16px gap, radius 12px, object-fit cover. 40px circular
arrow buttons (white, 1px #E6ECF2 border, navy arrows)
overlapping the strip edges at left/right, vertically centered.
Headline "Customer reviews" centered 26px/600, 40px
below.
Mobile (≤767px)
One tile at a time, full width within gutters, 1:1 (radius
12px). Two circular arrow buttons (56px) centered BELOW
the image, 16px gap. Headline 26px centered below.
### 2 · ANATOMY & STYLING
Photos
Minimum 8, customer-submitted (from the reviews app), no brand photography
Arrows
← → thin, navy, in white circles
### 3 · BEHAVIOR & INTERACTION
Arrows advance one tile (desktop) / one photo (mobile); loop infinitely; swipe on mobile.
Click photo → opens the review it belongs to in a lightbox.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
No copy beyond the fixed headline "Customer reviews". Photo selection rule: product visible in every shot; ≥ 2 hands/people; ≥ 1
in-context environment (nightstand, bathroom, gym bag); no text overlays.
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT


<!-- page 54 -->
[ ← ] 🖼 jar on a nightstand beside a lamp · 🖼 hand holding two gummies · 🖼 three jars lined up on a shelf · 🖼 jar in a gym bag · 🖼
customer selfie with the jar · (+3) [ → ]
Customer reviews
### 6 · SHOPIFY DATA SOURCE
Photos
Reviews app media gallery (photo reviews) or metafield proof.ugc_images
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 17 only: a customer-photo carousel. Desktop: five square 200px tiles in a row (radius 
12px, 16px gap, cover-cropped) inside a 1200px container with 64px top padding; a 40px white 
circular button with a thin navy arrow on each side, vertically centered and overlapping the strip 
edges; arrows advance one tile and loop. Mobile: one full-width square photo at a time, swipeable, 
with two 56px circular arrow buttons centered beneath it. Then the centered 26px navy headline 
"Customer reviews". Use the eight customer photos from the reviews app; no captions or text 
overlays.
### 8 · DO NOT
Do not use studio photography here.
Do not add captions, names or stars over the photos.


<!-- page 55 -->


## BLOCK 18 · Reviews widget

Social proof (volume)
Required
What this block does. The unfiltered proof: aggregate rating, review count, "% would recommend", a Filters pill and a navy
"Write a Review" pill, a sort dropdown, and a paginated list of reviews with reviewer name + Verified Buyer, "Reviewing
{product}" label, an "I recommend this product" chip, an optional age attribute, timestamp, bold title, body, and "Was this
helpful? 👍0 👎0". A "Show More" pill loads ten more. In the reference this is the Okendo/Yotpo-style widget; match its
anatomy.
Reference · MOBILE
Reference · DESKTOP
### 1 · LAYOUT
Desktop (≥1024px)
Summary centered: "4.9 · Based on 6,473 reviews" 14px +
"96% would recommend these products" 12px.
Controls row: "☐ Filters" white pill (1px navy border) left;
"☑ Write a Review" navy pill right. Second row: "6,473
reviews" grey left; "Most Recent ▾" select (white, 1px
border, 36px) right.
Review row: 1px #E6ECF2 divider. Left 30% column: initials
avatar + name 14px/600 + "Verified Buyer ☑" 12px;
"Reviewing" 12px/700 + product name 12px; "● I
recommend this product" 13px; attribute rows ("Age 26-
30") 12px. Right 70%: timestamp 12px grey right-aligned;
title 15px/600; body 14px; "Was this helpful? 👍 0 👎 0"
12px grey.
"Show More" white pill, 1px navy border, centered.
Mobile (≤767px)
Summary, then Filters + Write a Review pills side by side,
then count + sort dropdown.
Each review as a single column: name/verified, "Reviewing"
label right-aligned, recommend chip, attribute row,
timestamp right, title 20px, body 17px, helpful row. Divider
between reviews.
### 2 · ANATOMY & STYLING
Recommend chip
Navy filled circle with white check + text


<!-- page 56 -->
Attributes
Optional per-review custom questions (Age, Skin type, Size bought)
Sort options
Most Recent · Highest Rating · Lowest Rating · Most Helpful · With Photos
### 3 · BEHAVIOR & INTERACTION
Filters → drawer with rating, attributes, "with photos".
Write a Review → modal form.
Show More → appends 10.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Copy is user-generated; the only editorial choices are the summary line and the "Reviewing {product}" label (Shopify product
title). For the demo, eight sample reviews follow.
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
4.8 · Based on 3,184 reviews
95% would recommend these products
☐ Filters   ☑ Write a Review
Tyshema
Reviewing Nightfall
Sleep Gummies
● I recommend this
product
2 days ago
5 Stars
Love it
Was this helpful? 👍 0 👎 0
Jessica M. Verified
Buyer ☑
Reviewing Nightfall
Sleep Gummies
● I recommend this
product
2 days ago
This helps
I had sleep issues I couldn't seem to beat. Have been taking Nightfall for about a month and I'm doing much
better.
Dymaria W. Verified
Buyer ☑
Reviewing Deep
Sleep Starter Kit
● I recommend this
product
Age 26-30
2 days ago
Solace Kit
Absolutely loving this kit! It gave me the perfect start and I'm really impressed with everything in the tin.
Definitely planning on buying more from them in the future. It's been so helpful and super affordable too! 🥰💖
#kit #start #mask #help #affordability
Sydney C. Verified
Buyer ☑
Reviewing Deep
Sleep Starter Kit
● I recommend this
product
Age 21-25
2 days ago
Super Happy
noticed almost immediate results with the gummies!! 3am wakeups are gone & feeling great
Laurice J. Verified
Buyer ☑
Reviewing Nightfall
Sleep Gummies
2 days ago
ON FLEEK! Sleep tracker says deep sleep up
My doctor was impressed at my annual physical! I told her to get on board with SOLACE!


<!-- page 57 -->
● I recommend this
product
Age 56-60
Gianna A. Verified
Buyer ☑
Reviewing Nightfall
Sleep Gummies
● I recommend this
product
3 days ago
Great find!
This brand was recommended to me by my therapist. I've been taking them for over a month and I'm already
noticing a difference in how quickly I fall asleep. I definitely plan on continuing to take these.
Jenny W. Verified
Buyer ☑
Reviewing Nightfall
Sleep Gummies
● I recommend this
product
Age 46-50
3 days ago
Impressed!
This is the first product I've tried that has actually worked
Mary E. Verified
Buyer ☑
Reviewing Nightfall
Sleep Gummies
● I recommend this
product
Age 36-40
3 days ago
The best so far!
I can tell these gummies do the job for me, such a relief knowing that I'm going to actually sleep after a stressful
day! 🤭
[ Show More ]
### 6 · SHOPIFY DATA SOURCE
Everything
Reviews app (Okendo / Yotpo / Judge.me) widget bound to product.id; include kit +
component product reviews in one group
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 18 only: the reviews widget. Centered summary "4.8 · Based on 3,184 reviews" (14px) and 
"95% would recommend these products" (12px). A controls row: white pill "☐ Filters" with a 1px navy 
border on the left and a navy #24425C pill "Write a Review" on the right; beneath it "3,184 
reviews" in grey on the left and a "Most Recent ▾" select on the right. Then a list of reviews 
separated by 1px #E6ECF2 dividers. Desktop: left 30% column with initials avatar, name (14px 
semibold), "Verified Buyer ☑", "Reviewing" label + product name, a navy-dot "I recommend this 
product" chip and optional "Age 26-30" attribute row; right 70% with a right-aligned grey 
timestamp, 15px semibold title, 14px body and "Was this helpful? 👍 0 👎 0". Mobile: single column, 
title 20px, body 17px. Load the eight demo reviews exactly as listed in section 5 of this card 
(Tyshema; Jessica M.; Dymaria W.; Sydney C.; Laurice J.; Gianna A.; Jenny W.; Mary E.), then a 
centered white pill "Show More" with a 1px navy border that appends ten more.
### 8 · DO NOT
Do not hide low-star reviews; the widget must show the honest distribution behind Filters.
Do not restyle the widget in teal or pink; keep it neutral navy/white so it reads as third-party.


<!-- page 58 -->


## BLOCK 19 · FAQ + help card

Objection handling
Required
What this block does. A large accordion FAQ (the reference has 45 questions) with a search box, and — to the left on
desktop, below on mobile — two blush help cards: "Need more answers…" with three link rows (all FAQs, Help Center,
Contacts) and a support-agent photo card with "Start Chat". The FAQ is deliberately exhaustive: it is the page's SEO body and
the last stop for every objection.
Reference · MOBILE
Reference · DESKTOP
Mobile crop shown as two side-by-side strips; the help cards follow the accordion on mobile (see next page).
### 1 · LAYOUT
Desktop (≥1024px)
Two columns: left 30% sticky (top:120px) with the two help
cards; right 66% with headline 24px/600, search input right-
aligned (220px, 36px tall, radius 8px, magnifier icon), then
accordion rows.
Row: 1px #E6ECF2 divider, 20px padding, question 13px/600
navy left, "+" 20px thin navy right; expanded shows answer
13px/400 grey with "−".
Help card 1: --c-surface , radius 12px, 20px padding:
13px lines + icon+underlined-link rows (FAQ icon, ⓘ, ✉).
Help card 2: 40px agent photo left + "Have a specific
question? Ask our customer support team." + 💬 "Start
Chat" link.
Mobile (≤767px)
Headline 26px, search full width (48px), rows 20px padding
with 16px/600 questions; help cards full width below the
accordion.
### 2 · ANATOMY & STYLING


<!-- page 59 -->
[🔍 Search question]
+
+
+
+
+
+
+
Question count
25–45. Groups (in order): offer/kit → who/what → usage → results timeline → safety →
ingredients → "does it help with {symptom}" ×8–12 → regulatory/quality → origin →
taste/feel → policy
Product name
Every question spells out "{Brand}® {Product}" in full for SEO
Answers
40–90 words, direct, no marketing fluff, asterisked where needed
### 3 · BEHAVIOR & INTERACTION
Search filters rows live (substring match on question + answer).
One row open at a time; first row closed by default.
"Start Chat" opens the live chat widget.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Question formula: Does {Brand}® {Product} help with {symptom}? repeated for every symptom in Brief B7 plus
adjacent ones customers search for; plus the fixed set (who is it for, how to take, refrigeration, results timeline,
pregnancy/medication, long-term safety, missed dose, allergens, FDA, "really work?", artificial ingredients, where made, taste,
returns). Answer formula: direct answer in sentence 1 → mechanism or number in sentence 2 → caveat or CTA in sentence 3.
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Frequently Asked Questions
Why does the Solace Labs® Deep Sleep Starter Kit include both the Nightfall Sleep Gummies and the free sleep mask
and tea?
Because sleep is a routine, not a pill. The gifts come free with the Buy 2 get 1 free and Buy 3 get 2 free bundles. The gummies handle the
chemistry — calming your nervous system and supporting your own melatonin rhythm — while the silk mask blocks the light that
suppresses melatonin and the caffeine-free tea gives you a 10-minute wind-down ritual. Customers who use all three report faster results
than gummies alone.*
Who is the Deep Sleep Starter Kit best for?
Adults who take 30+ minutes to fall asleep, wake in the night, or feel groggy from melatonin or OTC sleep aids. It is designed for occasional
sleeplessness. If you have been diagnosed with a sleep disorder, talk to your doctor first.
What is Solace Labs® Nightfall Sleep Gummies?
A melatonin-free nightly gummy combining 200mg chelated magnesium bisglycinate, 200mg L-theanine, 500mg tart cherry extract, 50mg
apigenin, vitamin B6 and lemon balm. Two gummies, 30 minutes before bed. Sugar-free, vegan, third-party tested.
How is Nightfall different from other sleep gummies?
Most sleep gummies are 3–10mg of synthetic melatonin plus sugar. Nightfall contains no melatonin — it supplies the precursors and
calming co-factors your body uses to make its own, so there is no morning grogginess and no tolerance build-up. It is also sugar-free
(allulose) and dosed at clinically studied amounts, not "fairy-dusted".*
How do I take Nightfall Sleep Gummies?
Take two gummies 30–60 minutes before bed, with or without food. Consistency matters more than timing — nightly use for at least 14
nights gives the best results.*
Do Nightfall Sleep Gummies need to be refrigerated?
No. Store at room temperature away from direct sunlight and heat. The jar is sealed with a desiccant to keep gummies fresh for 24 months.
When will I start seeing results?
Many customers notice they fall asleep faster within the first 3–5 nights. In our 8-week consumer study, 84% reported faster sleep onset
within 14 nights and 71% reported fewer night wakings by week four.*


<!-- page 60 -->
+
+
+
+
+
+
+
+
+
+
+
+
+
+
+
+
Can I take Nightfall while pregnant, breastfeeding, or on medication?
Nightfall is non-habit-forming and drug-free, but if you are pregnant, breastfeeding, or taking prescription medication (especially sedatives,
blood-pressure or thyroid medication) please consult your healthcare provider before use.
What does Nightfall help with?
Falling asleep faster, staying asleep through the night, waking without grogginess, and easing the "wired but tired" feeling at bedtime. It
also supports muscle relaxation and everyday stress resilience.*
What ingredients are in Nightfall Sleep Gummies?
Magnesium bisglycinate (200mg), L-theanine (200mg), tart cherry extract (500mg), apigenin from chamomile (50mg), vitamin B6 (2mg),
lemon balm (150mg), glycine and passionflower. Sweetened with allulose; pectin base; natural blackberry flavor.
What is magnesium bisglycinate and why is it special?
It is magnesium bound to the amino acid glycine. This "chelated" form is absorbed over 3× better than the magnesium oxide in most
supplements and does not cause the digestive upset oxide is known for. Glycine itself supports lower core body temperature at night, which
is part of how the body initiates sleep.*
Is Nightfall safe to take long-term?
Yes. Every ingredient is at or below established safe daily intake levels and none is habit-forming. Many customers take Nightfall nightly for
years, which is why the 3-jar and 5-jar bundles are our most popular. As always, review with your healthcare provider if you have a medical
condition.
Can I take Nightfall with other supplements or medications?
Nightfall pairs well with most daily supplements. Because it contains magnesium, separate it from antibiotics or thyroid medication by 2–4
hours, and ask your provider if you take sedatives or blood-pressure medication.
What if I miss a dose?
Just take your next dose the following night. Do not double up. Nightfall works cumulatively, so one missed night will not undo your
progress.
What allergens are in Nightfall?
None of the major nine allergens. Nightfall is free from gluten, dairy, soy, egg, tree nuts, peanuts, fish, shellfish, sesame and gelatin. It is
manufactured in a facility that also processes tree nuts; equipment is cleaned and allergen-tested between runs.
Does Nightfall help with 3 a.m. wake-ups?
Night wakings are often driven by a cortisol spike and a dip in the body's own melatonin around the fourth sleep cycle. Nightfall's
magnesium and apigenin support deeper slow-wave sleep and a steadier overnight rhythm; 71% of study participants reported fewer wake-
ups.*
Does Nightfall help with racing thoughts at bedtime?
L-theanine and lemon balm are included specifically for this. They promote calm, alpha-wave brain activity without sedation, so the mental
"replay" quiets down while you still feel like yourself.*
Does Nightfall help with morning grogginess?
It is designed to avoid it. Because Nightfall contains no melatonin or sedative herbs, there is nothing left in your system to cause a
"hangover" — most customers describe waking up clearer than before.*
Does Nightfall help with stress?
Magnesium, L-theanine and lemon balm each support the body's stress response. Many customers report calmer evenings within the first
week, and better sleep itself lowers next-day stress.*
Does Nightfall help with muscle recovery?
Tart cherry and magnesium both support recovery after exercise, and deeper slow-wave sleep is when most muscle repair happens.
Athletes are among our most loyal repeat customers.*
Is Nightfall FDA approved?
Dietary supplements are not approved by the FDA; no supplement is. Nightfall is manufactured in an FDA-registered, cGMP-certified facility
and every batch is tested by an independent lab. The FDA disclaimer at the bottom of this page applies.
Does Nightfall really work?
In our 8-week consumer study of 212 adults, 84% reported falling asleep faster within 14 nights. Across 3,184 verified reviews, 95% of
customers say they would recommend it. If it does not work for you, our 60-day money-back guarantee applies.*
Does Nightfall contain any artificial flavors, colors, or sweeteners?


<!-- page 61 -->
+
+
+
+
+
No. Blackberry flavor comes from natural fruit extracts, the color from black carrot juice, and sweetness from allulose and monk fruit. No
sugar, no sugar alcohols, no sucralose.
Where are Nightfall Sleep Gummies made?
In our own cGMP-certified, FDA-registered facility in Boulder, Colorado, from ingredients sourced in the U.S., Italy (magnesium) and Japan
(L-theanine).
What do Nightfall Sleep Gummies taste like?
Ripe blackberry with a hint of vanilla. No chalky magnesium aftertaste — that was the hardest part of the formulation to get right.
Why do I need the sleep mask and tea if the gummies work?
You do not need them — they are free with the Buy 2 get 1 free and Buy 3 get 2 free bundles. But light exposure and a wind-down ritual
are the two most-cited reasons sleep aids "stop working"; the gifts remove both obstacles.
Can I take Nightfall if I work night shifts?
Yes. Take two gummies 30–60 minutes before your intended sleep, whenever that is. Shift workers were part of our consumer study and
reported similar results to day workers.*
What is your return policy?
A 60-day money-back guarantee on your first order, even if the jar is empty. Email hello@solacelabs.com and we will refund you, no
questions asked.
HELP CARD 1
Need more answers about all our products?
📄 Check all product FAQs
Any purchase or account related information you can find in support articles.
ⓘ Help Center
Or drop us an email.
✉ Our Contacts
HELP CARD 2
◯ Have a specific question? Ask our customer support team.
💬 Start Chat
### 6 · SHOPIFY DATA SOURCE
FAQ
metafield pdp.faq list of {q, a} (product) + theme-level store FAQs appended
Help links
Theme settings
Chat
Chat app trigger


<!-- page 62 -->
Reference · MOBILE
Mobile: the two help cards sit directly under the accordion.
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 19 only: the FAQ section. Desktop: left 30% column (sticky) with two cards on #FCF8F7 
(radius 12px, 20px padding) — card 1: "Need more answers about all our products?" + link row "Check 
all product FAQs" with a FAQ icon; "Any purchase or account related information you can find in 
support articles." + link "Help Center" with an ⓘ icon; "Or drop us an email." + link "Our 
Contacts" with an envelope icon; card 2: a 40px round support-agent photo, "Have a specific 
question? Ask our customer support team." and a chat-icon link "Start Chat". Right 66%: headline 
"Frequently Asked Questions" (24px navy semibold), a 220px search input right-aligned with a 
magnifier icon, then an accordion with 1px #E6ECF2 dividers, 20px row padding, 13px semibold navy 
questions and a thin "+" on the right that toggles to "−" and reveals a 13px grey answer. Load the 
28 questions and answers exactly as listed in section 5 of this card, in that order. Search filters 
rows live. Mobile: headline, full-width search, accordion with 16px questions, then the two help 
cards.
### 8 · DO NOT
Do not collapse to 5 "top questions"; length is the feature.
Do not open the first question by default.
Do not shorten the product name in questions to "it".


<!-- page 63 -->


## BLOCK 20 · Cross-sell ("See other bundles")

AOV
Required
What this block does. Two (desktop) or a vertical pair (mobile) of related bundle cards: a large blush image tile with a white
"Add" pill in its corner, then name, one-line description and "From $X". It catches the visitor who decided this kit is not quite
right.
Reference · MOBILE
Reference · DESKTOP
Mobile crop shown as two strips.
### 1 · LAYOUT
Desktop (≥1024px)
Headline centered 26px/600. Two cards per row (reference
shows a compact list variant on desktop: 64px image tile left
+ name 14px/600 + 13px grey description). Prefer the
mobile card pattern scaled to 3 columns if more than two
products exist.
Mobile (≤767px)
Card: image tile --c-surface , 1:1, radius 16px, product
packshot centered; white pill "Add" (36px, 14px/600)
bottom-right inside the tile. Below: name 17px/600 →
description 15px grey → "From $X" 15px navy. 24px
between cards.
### 2 · ANATOMY & STYLING
Add pill
White, no border, subtle; adds the default variant to cart
Description
One line, verb-led: "Promote… and balance…", "Level up… and remove…"
### 3 · BEHAVIOR & INTERACTION
"Add" → adds to cart, opens drawer. Card → product page.
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Selection rule: the two bundles adjacent to this one in the customer journey (the "before" and the "after"), never the same
product in a different size. Description formula: {Verb} {benefit 1} and {verb} {benefit 2} ≤ 12 words. Price = the
Buy 2 get 1 free tier price, "From $X".
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
Add
[packshot on blush tile]
The Wind-Down Kit
Calm racing thoughts and ease into sleep with L-theanine drops +
Add
[packshot on blush tile]
The Calm Day Kit


<!-- page 64 -->
Nightfall
From $58.49
Level up your daytime focus and remove afternoon crashes
From $52.24
### 6 · SHOPIFY DATA SOURCE
Products
metafield pdp.cross_sell (2 product references)
Price
Buy 2 get 1 free tier price of that product
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 20 only: centered 26px navy headline "See other bundles", then two product cards (side 
by side on desktop, stacked with 24px gap on mobile). Each card: a square image tile with 
background #FCF8F7 and radius 16px showing the packshot centered, with a small white pill button 
"Add" in the bottom-right corner of the tile; below, the name in 17px semibold ("The Wind-Down Kit" 
/ "The Calm Day Kit"), a 15px grey one-line description ("Calm racing thoughts and ease into sleep 
with L-theanine drops + Nightfall" / "Level up your daytime focus and remove afternoon crashes") 
and "From $58.49" / "From $52.24" in navy. "Add" adds the default variant to cart.
### 8 · DO NOT
Do not show more than 2–3 items; this is a nudge, not a collection.
Do not show star ratings on these cards.


<!-- page 65 -->


## BLOCK 21 · Footer

Trust · capture · compliance
Required
What this block does. A blush full-width footer: centered brand tagline + "Find your product" link + four social icons, then
four link columns and an email-capture column with a "Follow on Shop" button, then the payment-icon row, legal links,
copyright with partner badge, and finally the boxed FDA disclaimer that resolves every asterisk on the page.
Reference · MOBILE
Reference · DESKTOP
Mobile crop shown as two strips.
### 1 · LAYOUT
Desktop (≥1024px)
Background --c-surface , 64px padding. Row 1 centered:
tagline 15px navy (two lines max) → underlined "Find your
product" → 4 social line icons (Instagram, Facebook, TikTok,
Reddit) 20px, 32px gap.
Row 2: five columns — Shop all / Live chat / Loyalty /
Contact us / Email capture (heading 13px/700, links 13px,
sub-labels 11px grey in parentheses). Email: 44px input with
→ button inside, radius 8px; 11px privacy line with
underlined promise; purple "♡ Follow on Shop" pill.
Row 3: 1px divider; legal links 12px grey left; 11 payment
icons right (32×20).
Row 4: © line left; disclaimer box centered (1px #DDD
border, radius 6px, 11px); partner badge right.
Mobile (≤767px)
Tagline/link/social centered. Link columns become two
columns (Shop all + Live chat, then Loyalty + Contact). Email
capture full width. Payment icons wrap over two rows,
centered. Legal links wrap. Disclaimer box full width, last
element.
### 2 · ANATOMY & STYLING
Payment icons
Amazon, Amex, Apple Pay, Diners, Discover, Google Pay, Mastercard, PayPal, Shop Pay,
Venmo, Visa (Shopify's own SVGs)
Disclaimer
Boxed, 11–12px, always last
### 3 · BEHAVIOR & INTERACTION
Email submit → Klaviyo/Shopify Email list, inline success state.


<!-- page 66 -->
### 4 · COPY FORMULA (WORKS FOR ANY PRODUCT)
Tagline formula: We're raising the standards for {category} products. Email heading: Sign up to our
mailing list and get {10}% off your first order . Privacy line: We will send you thoughtful content for
{audience}. You can unsubscribe in one click, and we will never share your email address .
5 · WORKED EXAMPLE — FILLED FOR THE DEMO PRODUCT
We're raising the standards for sleep & recovery products.
Find your product
◎ ⓕ ♪ ☺
Shop all
Bundles
Accessories
Gift cards
Live chat
(customer
service)
Track my order
Learning Center
(our blog)
Help center
Accessibility
Solace Circle
(Rewards and
Referrals)
Become a partner
Contact us
hello@solacelabs.com
+1 (720) 555-0142
About us
1450 Pearl St, Boulder
CO 80302
Sign up to our mailing list and get 10% off your
first order
[Enter your email here →]
We will send you thoughtful content for better
sleep. You can unsubscribe in one click, and we
will never share your email address
♡ Follow on shop
Terms of Service · Privacy Policy · Accessibility Statement · Returns, Refund & Exchange Policy · Messaging Terms & Conditions · Sitemap   
[11 payment icons]
© 2023-2026 Solace Labs. All Rights Reserved    ✦ Rest Fund PROUD SUPPORTER
* These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or
prevent any disease.
### 6 · SHOPIFY DATA SOURCE
Menus
Footer menus ×4
Email
Newsletter form
Disclaimer
Theme setting legal.disclaimer ; swap to "Results may vary" text for non-
supplements
### 7 · BUILD PROMPT FOR THE PAGE BUILDER (PASTE AS-IS)
Build BLOCK 21 only: the footer on background #FCF8F7 with 64px padding. Row 1 centered: "We're 
raising the standards for sleep & recovery products." (15px navy), underlined "Find your product", 
and four 20px navy line icons (Instagram, Facebook, TikTok, Reddit). Row 2, five columns (two on 
mobile, email full-width): "Shop all" (Bundles, Accessories, Gift cards); "Live chat (customer 
service)" (Track my order, Learning Center (our blog), Help center, Accessibility); "Solace Circle 
(Rewards and Referrals)" (Become a partner); "Contact us" (hello@solacelabs.com, +1 (720) 555-0142, 
About us, 1450 Pearl St, Boulder CO 80302); and the email column. Email column: heading "Sign up to 
our mailing list and get 10% off your first order", a 44px input "Enter your email here" with an 
arrow button inside, an 11px privacy line, and a purple #7A76B3 pill "♡ Follow on shop". Row 3 
after a 1px divider: legal links in 12px grey (Terms of Service, Privacy Policy, Accessibility 
Statement, Returns, Refund & Exchange Policy, Messaging Terms & Conditions, Sitemap) left and 
eleven 32×20 payment icons right. Row 4: "© 2023-2026 Solace Labs. All Rights Reserved" left, a 


<!-- page 67 -->
boxed 11px disclaimer centered "* These statements have not been evaluated by the Food and Drug 
Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.", 
and the "Rest Fund · Proud supporter" badge right.
### 8 · DO NOT
Do not omit the boxed disclaimer or move it above the payment icons; it is always the last element.
Do not use a dark footer; the blush surface keeps the page calm to the end.


<!-- page 68 -->
Appendix A · Category adaptation matrix
The block order never changes. This table tells the builder what each variable block becomes when the product is not an
ingestible supplement.
Block
Supplement (demo)
Skincare
Device / gadget
Apparel
Food & beverage
03
Qualifier
Symptoms, history,
lifestyle, aspiration,
holistic goal
Skin concerns, past
products failed,
climate/routine,
texture wish, long-
term skin goal
Pain/inconvenience, tried
alternatives, usage
context, feature wish,
outcome
Fit frustrations,
fabric sensitivity,
occasion, care
wish, style goal
Cravings/energy
dips, diet pattern,
schedule, taste wish,
health goal
03 Links
View Supplement
Facts
View full ingredients
(INCI)
View specifications
Size guide
View Nutrition Facts
05
Clinicians'
Choice
Clinicians / OB-GYNs
/ sleep specialists
Dermatologists /
estheticians
Physiotherapists /
trainers
"Stylists' Choice"
(or drop)
Registered dietitians
06 Tiers
Buy 1 / Buy 2 get 1
free / Buy 3 get 2
free — identical on
every category; units
= jars
Same tiers; units =
bottles / tubes
Same tiers; units =
devices (or device +
consumable packs)
Same tiers; units =
pieces; add a
size/color selector
above the tiles
Same tiers; units =
boxes / bags
07
HSA/FSA
HSA/FSA badge
Drop; show Shop Pay
installments
HSA/FSA if medical; else
installments
Installments
Drop
09 Six
steps
Ingredient
mechanisms
Cleanse → penetrate
→ hydrate → barrier
→ renewal → glow
Sense → act → adapt →
protect → habit →
outcome
Fiber → weave →
fit → temperature
→ durability →
confidence
Fuel → digest →
absorb → sustain →
recover → habit
10
Features
Tested, free-from,
vegan, etc.
Derm-tested,
fragrance-free, non-
comedogenic, cruelty-
free, recyclable
Materials, warranty,
battery, noise, returns
Fabric origin,
OEKO-TEX,
machine-
washable, ethical
factory, free
exchanges
Organic, no added
sugar, allergen-free,
cold-pressed,
recyclable
11 Stats
% improved, %
reduced, multiplier,
Helps, Supports
% saw smoother skin
in 4 wks, % reduced
redness, 2x hydration,
Helps, Supports
% reduced pain, % faster
setup, 3x battery, Helps,
Supports
% would rebuy, %
perfect fit first try,
4x more durable,
Keeps, Supports
% steadier energy, %
fewer cravings, 2x
protein, Helps,
Supports
13 Cards
Ingredients
Actives (INCI names)
Components (motor,
sensor, material)
Materials &
construction
details
Ingredients / macros
16 Table
rows
Free-from +
manufacturing
Free-from + testing +
packaging
Materials, warranty,
certifications,
repairability
Fabric grade,
factory audit, fit
guarantee, returns
window
Sourcing, sugar,
additives, packaging


<!-- page 69 -->
21
Disclaimer
FDA sentence
"Results may vary.
Patch-test before use."
"Not a medical device
unless stated. Results
may vary."
Drop the box;
keep legal links
FDA sentence if any
health claim


<!-- page 70 -->
Appendix B · Replace-registry of invented data
Every number, study, person and partner below was invented so the worked examples read as finished copy. None may ship on a
live page. Replace each with the real figure or drop the element that depends on it.
Block
Invented item
Replace with
00, 02, 04,
06, 07
Unit $39.99 · compare-at $79.98 · tier prices
$79.98 / $119.97 · gift value $42
Real Shopify unit price; compare-at only if genuinely set; tier math is
fixed (×2 for 3 units, ×3 for 5 units)
05
842 clinicians · FrontrowMD · sleep specialists
Real count from your clinician-review platform, or drop Block 05
08
"Over 400,000 restless sleepers"
Real cumulative customer count (round down)
08, 18
All review names, titles and bodies
Real verified reviews from the reviews app
11
84% / 71% (8-week study, n=212) · "Over 3x
absorption"
Real study figures with citation in the "Show studies" modal; if none,
keep only "Helps" and "Supports" callouts
12
Dr. Maya Okafor, PhD, Sleep Scientist
A real credentialed professional with written permission, or drop
Block 12
13
Ingredient doses
Values from the actual supplement-facts panel
15
Rest Fund · 120,000+ sleep kits
Real partner and audited impact figure, or drop Block 15
16
ISO 17025 lab, Boulder facility, 24-month shelf
life, lead times
Real manufacturing facts
18
4.8 · 3,184 reviews · 95% recommend
Live aggregate from the reviews app
19
60-day guarantee, contact details, sourcing
countries
Real policies and facts
21
Address, phone, email, © years
Real business details


<!-- page 71 -->
Appendix C · Shopify metafield schema
Create these once (Settings → Custom data → Products). Namespaces: pdp (page content), offer (pricing/gifts), proof
(evidence). Store-wide items live in theme settings. The page builder reads these; the human fills them from the Product Brief.
Key
Type
Feeds
block
Notes
pdp.right_for_you
list.single_line_text (5)
03
Exactly five, asterisked
pdp.serving_line
single_line_text
03
"1 Kit = 30 servings…"
pdp.facts_image
file
03
Facts panel / spec sheet
offer.items
json
04
[{title, benefit, image, compare_at, price,
is_gift}]
offer.gift_value
money
00 02 04
14
Sum of gift compare-at prices
offer.unit_word
single_line_text
06 07
"jar", "bottle", "pair"
Automatic discount (Shopify Function)
—
06 07
qty 3 → 1 free; qty 5 → 2 free; store-wide,
no selling plans
offer.hsa_eligible
boolean
07
proof.clinician_count · _platform ·
_avatars
number · text · list.file
05
Block hidden when count is empty
proof.customer_count
single_line_text
08
"400,000"
proof.featured_reviews
list.single_line_text (4
review IDs)
08
pdp.how_intro · pdp.how_steps ·
pdp.how_image
multi_line · json[6] · file
09
pdp.features
json[5]
10
{icon, title, text}
proof.stats · proof.studies ·
proof.image
json[5] · json · file
11
{number, label, body, bar_pct}
proof.expert_quote
json
12
Block hidden when empty
pdp.ingredients
json
13
{name, image, tags[], benefits[], detail,
dose}
pdp.transparency
json[3]
16
{tab, paragraph, rows[{label, us, them}]}
proof.ugc_images
list.file
17
Or reviews-app media
pdp.faq
json
19
[{q, a}]
pdp.cross_sell
list.product_reference (2)
20
Theme settings
—
01 14 15
21
Logo, nav, order perks ×6, mission partner,
footer menus, disclaimer text
SECTION FILES (IF BUILDING AS ONLINE STORE 2.0 SECTIONS)


<!-- page 72 -->
announcement-bar.liquid · header.liquid · pdp-gallery.liquid · pdp-buy-column.liquid (blocks 03–07
as nested blocks: qualifier, value-stack, clinicians, bundle-tiers, cta-stack) · pdp-social-
proof.liquid · pdp-how-it-works.liquid · pdp-features.liquid · pdp-stats.liquid · pdp-
endorsement.liquid · pdp-ingredients.liquid · pdp-perks.liquid · pdp-mission.liquid · pdp-
transparency.liquid · pdp-ugc.liquid · pdp-reviews.liquid · pdp-faq.liquid · pdp-cross-sell.liquid
· footer.liquid


<!-- page 73 -->
Appendix D · QA checklist (run per block, then per
page)
PER BLOCK
Side-by-side with the reference screenshot at 390px and
1280px: same element order, same alignment, same
proportions.
Only the tokens listed in the block's Anatomy table are used
(no new colors, radii or shadows).
Every benefit claim ends with an asterisk.
No placeholder text ("Lorem", "[insert]", "TBD") anywhere.
Copy word counts within the formula limits.
Interactive states exist (selected tile, expanded card, active
tab) and match the reference.
Images have alt text; none is a stretched or letterboxed
packshot.
PER PAGE
Block order 00→21 with no additions or omissions other
than declared Conditional drops.
The Buy 2 get 1 free tile is selected on load; the summary
line under ADD TO CART updates on every tier change; the
sticky/mobile CTA (if any) mirrors it.
Exactly one teal button per viewport height in the buy
column; teal appears nowhere below Block 07.
No subscription, autoship or refill language anywhere on the
page.
Display serif appears exactly three times (Blocks 08, 09, 15).
The FDA/"results may vary" box is the last element of the
page.
Every invented item in Appendix B has been replaced or its
block removed.
Lighthouse mobile ≥ 80; LCP image (hero) preloaded; below-
fold images lazy-loaded.
Total page length on mobile: 40–50 viewports (the reference
is ~44). Shorter means a block is underbuilt.
Final check: read the page top to bottom as the customer described in Product Brief B7. Every one of their five pains should
be named in Block 03, explained in Block 09, quantified in Block 11, and answered in Block 19. If any pain misses a stop, the
page is not finished.
