"""Build the PDF instructions guide for Fudge (the Shopify page-builder agent).

Inputs: our reference PDP template (any of .md / .txt / .docx / .pdf / .html) and the product
summary. Claude merges the two into a section-by-section build spec; without an API key the
guide is assembled mechanically (template text followed by the summary) so the pipeline
still produces a usable document.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

from . import config

log = logging.getLogger("pdpkit.guide")

GUIDE_SYSTEM = """You prepare the per-product build guide that "Fudge", our AI Shopify page builder, follows to build a product
page from our Universal PDP Template (a 22-block, block-by-block framework). You receive:
  (1) the full template text: global design system, copy rules, the Product Brief field list (B1-B16), 22 block cards
      (each with layout, styling, behavior, a copy formula, a worked example for a fictional demo product, Shopify data
      sources, a paste-ready build prompt, and a DO NOT list) and appendices (category matrix, replace-registry, QA);
  (2) product_summary: facts scraped from a competitor's page for the product we are launching under OUR brand;
  (3) our brand name, our product title, and the list of generated image files available for the page.

Produce the guide in Markdown, exactly this structure:

# PDP build guide: <our product title>
One paragraph: what the product is, the angle we take, and which template category (Appendix A) applies.

## 1. Product Brief
A table with every field B1..B16 filled for OUR product. Use our brand (never the competitor's), the three-tier one-time
offer exactly as the template defines it (Buy 1 / Buy 2 get 1 free / Buy 3 get 2 free, tier 2 pre-selected) with prices
derived from the unit price in product_summary, and the competitor's pains, mechanism, components, quality signals, FAQ
and review themes rewritten in our voice. If a field has no real data (clinician counts, studies, partner/mission,
cross-sell products), write "none - block dropped" rather than inventing it.

## 2. Blocks
One subsection per block, "### BLOCK NN - <name>", in template order 00..21, each containing:
- **Status:** BUILD or DROP, with the one-line reason (the template rule: a block whose Brief field is empty is dropped).
- **Copy:** every copy slot of the block filled with final text, following that block's copy formula and the global copy
  rules (second person, sentence-case headlines, specific numbers only when real, asterisk on unverifiable claims,
  reusable micro-copy verbatim). Reviews: reuse the competitor's review THEMES but write new, realistic review text
  attributed to first name + initial; never copy their reviews verbatim.
- **Images:** which files to place, chosen from the generated image list (gen_01.jpg ...) by what each slot needs; say
  what each image must show. If more images are needed than exist, say which additional Higgsfield prompt to run.
- **Build prompt:** the block's paste-ready build prompt (section 7 of the card) rewritten with our product's values
  substituted for the demo product's, kept to the same length and specificity.
- **Do not:** the block's DO NOT list, carried over verbatim.

## 3. Replace-registry
A table of every value in this guide that is an assumption or placeholder (prefix each in the text with [ASSUMED]),
with what to replace it with before publish.

## 4. QA checklist
The template's Appendix D checklist condensed to the items relevant to the blocks marked BUILD.

Rules: never mention the competitor by name anywhere in the guide; use only facts from product_summary plus the
template; mark anything invented [ASSUMED]; Markdown only, no preamble, no closing remarks."""


# --------------------------------------------------------------------------- template reading
def read_template(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt", ".markdown"):
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup
        return BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser").get_text("\n", strip=True)
    if suffix == ".docx":
        try:
            import docx  # python-docx, optional
        except ImportError as e:
            raise SystemExit("pip install python-docx to read .docx templates") from e
        d = docx.Document(str(path))
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        return "\n".join(parts)
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # optional
        except ImportError as e:
            raise SystemExit("pip install pypdf to read .pdf templates") from e
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(path)).pages)
    raise SystemExit(f"unsupported template type: {path.suffix}")


# --------------------------------------------------------------------------- content
def claude_guide(template_text: str, summary_md: str, generated_files: list[str], *, brand: str = "", our_title: str = "") -> str | None:
    if not config.ANTHROPIC_ENABLED:
        return None
    try:
        import anthropic
    except ImportError:
        return None
    client = anthropic.Anthropic()
    user = (
        "## Reference PDP template\n\n" + template_text.strip() +
        f"\n\n## Our brand\n\nBrand name: {brand or config.BRAND_NAME}\nOur product title (Shopify title): {our_title}\n" +
        "\n\n## product_summary (scraped from the competitor page)\n\n" + summary_md.strip() +
        "\n\n## Generated image files available\n\n" + ("\n".join(generated_files) if generated_files else "(none yet)")
    )
    try:
        with client.messages.stream(
            model=config.ANTHROPIC_MODEL,
            max_tokens=64000,
            system=[{"type": "text", "text": GUIDE_SYSTEM}],
            messages=[{"role": "user", "content": [
                {"type": "text", "text": user.split("\n\n## Our brand")[0], "cache_control": {"type": "ephemeral"}},   # template: stable across products
                {"type": "text", "text": "\n\n## Our brand" + user.split("\n\n## Our brand", 1)[1]},
            ]}],
        ) as stream:
            msg = stream.get_final_message()
    except anthropic.APIError as e:
        log.warning("Claude guide failed (%s); assembling a mechanical guide", e)
        return None
    if msg.stop_reason == "refusal":
        return None
    return "".join(b.text for b in msg.content if b.type == "text").strip() or None


def mechanical_guide(product_name: str, template_text: str, summary_md: str, generated_files: list[str]) -> str:
    return "\n".join([
        f"# PDP build guide: {product_name}",
        "",
        "> Assembled without Claude (no ANTHROPIC_API_KEY). Fudge: follow the template below, using the product summary for facts.",
        "",
        "## Reference PDP template",
        "",
        template_text.strip(),
        "",
        "## Generated images",
        "",
        *([f"- {f}" for f in generated_files] or ["- (none yet)"]),
        "",
        "## product_summary",
        "",
        summary_md.strip(),
    ])


# --------------------------------------------------------------------------- pdf rendering
def _inline(text: str) -> str:
    """Minimal Markdown inline -> ReportLab mini-HTML."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", text)
    return text


def markdown_to_pdf(md: str, pdf_path: Path, title: str) -> Path:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors

    styles = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10, leading=14, spaceAfter=4)
    h = {1: ParagraphStyle("h1", parent=styles["Heading1"], fontSize=18, spaceBefore=10, spaceAfter=8),
         2: ParagraphStyle("h2", parent=styles["Heading2"], fontSize=14, spaceBefore=10, spaceAfter=6),
         3: ParagraphStyle("h3", parent=styles["Heading3"], fontSize=11.5, spaceBefore=8, spaceAfter=4)}
    quote = ParagraphStyle("quote", parent=body, leftIndent=12, textColor=colors.HexColor("#444444"))

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=title)
    story = []
    bullets: list[str] = []
    table_rows: list[list[str]] = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            story.append(ListFlowable([ListItem(Paragraph(_inline(b), body), leftIndent=10) for b in bullets], bulletType="bullet", leftIndent=14))
            bullets = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            width = max(len(r) for r in table_rows)
            rows = [[Paragraph(_inline(c), body) for c in r + [""] * (width - len(r))] for r in table_rows]
            t = Table(rows, repeatRows=1, hAlign="LEFT")
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            story.append(Spacer(1, 6))
            table_rows = []

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("|"):
            flush_bullets()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            table_rows.append(cells)
            continue
        flush_table()
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush_bullets()
            level = min(len(m.group(1)), 3)
            if level == 1 and story:
                story.append(Spacer(1, 6))
            story.append(Paragraph(_inline(m.group(2)), h[level]))
            continue
        m = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)", line)
        if m:
            bullets.append(m.group(1))
            continue
        flush_bullets()
        if line.strip() == "---":
            story.append(PageBreak())
        elif line.startswith(">"):
            story.append(Paragraph(_inline(line.lstrip("> ")), quote))
        elif line.strip():
            story.append(Paragraph(_inline(line), body))
        else:
            story.append(Spacer(1, 4))
    flush_bullets()
    flush_table()
    doc.build(story)
    return pdf_path


def build_guide(product_dir: Path, product_name: str, template_path: Path, *, use_claude: bool = True) -> Path:
    summary_path = product_dir / "product_summary.md"
    if not summary_path.exists():
        raise SystemExit(f"{summary_path} missing; run `grab` first")
    summary_md = summary_path.read_text(encoding="utf-8")
    template_text = read_template(template_path)
    gen_dir = product_dir / config.generated_dir_name(product_name)
    generated = sorted(p.name for p in gen_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")) if gen_dir.exists() else []
    md = (claude_guide(template_text, summary_md, generated, our_title=product_name) if use_claude else None) or mechanical_guide(product_name, template_text, summary_md, generated)
    slug = config.slugify(product_name)
    (product_dir / f"{slug}_fudge_guide.md").write_text(md, encoding="utf-8")
    return markdown_to_pdf(md, product_dir / f"{slug}_fudge_guide.pdf", f"PDP build guide: {product_name}")
