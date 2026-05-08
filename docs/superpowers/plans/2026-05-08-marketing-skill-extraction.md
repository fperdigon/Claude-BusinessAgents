# Marketing Skill Code Extraction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract ~360 lines of inline code from `marketing.md` into `scripts/`, `snippets/`, and `templates/` sibling folders, replacing each block with a one-line Read instruction or Bash command, reducing skill size by ~26%.

**Architecture:** Five files are extracted from `marketing.md` into three new folders under `.claude/skills/BusinessAgents/`. Each extracted file is self-contained and referenced by the skill via Read tool or Bash. The skill file is edited in-place using the Edit tool — no regeneration. The snippets for doc-title and caption-tabs are bundled as self-contained HTML fragments (with their own `<style>` and `<script>` tags) to keep injection simple. The `.copy-btn` class shared by both components is added to the base template CSS.

**Tech Stack:** Python 3 (argparse, Playwright, ReportLab), HTML/CSS/JS, Markdown

---

### Task 1: Create `scripts/generate-pdf.py`

**Files:**
- Create: `.claude/skills/BusinessAgents/scripts/generate-pdf.py`

- [ ] **Step 1: Create the scripts directory and write the script**

Write `.claude/skills/BusinessAgents/scripts/generate-pdf.py` with this exact content:

```python
#!/usr/bin/env python3
"""Generate a PDF from a carousel HTML file. All session values passed as CLI args."""
import argparse, os, re


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from carousel HTML")
    parser.add_argument("--width",  type=int, required=True, help="Card width in px")
    parser.add_argument("--height", type=int, required=True, help="Card height in px")
    parser.add_argument("--slides", type=int, required=True, help="Number of slides")
    parser.add_argument("--html",   required=True, help="Path to carousel HTML file")
    parser.add_argument("--pdf",    required=True, help="Path for output PDF file")
    args = parser.parse_args()

    CARD_W     = args.width
    CARD_H     = args.height
    NUM_SLIDES = args.slides
    html_path  = os.path.abspath(args.html)
    pdf_path   = os.path.abspath(args.pdf)
    html_dir   = os.path.dirname(html_path)
    pv_path    = os.path.join(html_dir, "carousel-print-view.html")

    # Step 1 — build a stripped print-view HTML (no nav / instructions / caption-box / JS)
    with open(html_path, encoding="utf-8") as f:
        src = f.read()

    for tag in ("nav", "instructions", "caption-box", "doc-title-row"):
        src = re.sub(
            rf'<div[^>]*class="[^"]*{tag}[^"]*".*?</div>\s*',
            "", src, flags=re.DOTALL | re.IGNORECASE,
        )
    src = re.sub(r"<script[\s\S]*?</script>", "", src, flags=re.IGNORECASE)
    src = src.replace(
        "body {",
        "body { flex-direction: column !important; align-items: center !important; gap: 0 !important; padding: 0 !important; background: #080810;",
        1,
    )
    # Replace display:none in the .card rule with display:flex — no !important so JS inline
    # styles can override it per-slide during screenshotting
    src = re.sub(
        r'(\.card\s*\{[^}]*?)display:\s*none',
        r'\1display: flex',
        src,
    )
    with open(pv_path, "w", encoding="utf-8") as f:
        f.write(src)

    # Step 2 — screenshot each slide individually with Playwright
    from playwright.sync_api import sync_playwright

    slide_paths = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": CARD_W, "height": CARD_H})
        page.goto(f"file://{pv_path}")
        page.wait_for_load_state("networkidle", timeout=8000)

        for i in range(NUM_SLIDES):
            page.evaluate(f"""
                document.querySelectorAll('.card').forEach((c, idx) => {{
                    c.style.display = idx === {i} ? 'flex' : 'none';
                }});
            """)
            slide_file = os.path.join(html_dir, f"_slide_{i+1:02d}.png")
            page.screenshot(
                path=slide_file,
                clip={"x": 0, "y": 0, "width": CARD_W, "height": CARD_H},
            )
            slide_paths.append(slide_file)

        browser.close()

    # Step 3 — assemble PDF with ReportLab
    from reportlab.pdfgen import canvas as rl_canvas

    c = rl_canvas.Canvas(pdf_path, pagesize=(CARD_W, CARD_H))
    for sp in slide_paths:
        c.drawImage(sp, 0, 0, CARD_W, CARD_H)
        c.showPage()
    c.save()

    # Step 4 — clean up temp files
    os.remove(pv_path)
    for sp in slide_paths:
        os.remove(sp)

    print(f"PDF saved: {pdf_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the script parses correctly**

Run:
```bash
python .claude/skills/BusinessAgents/scripts/generate-pdf.py --help
```

Expected output:
```
usage: generate-pdf.py [-h] --width WIDTH --height HEIGHT --slides SLIDES --html HTML --pdf PDF
...
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BusinessAgents/scripts/generate-pdf.py
git commit -m "feat(marketing): extract PDF generation script to scripts/generate-pdf.py"
```

---

### Task 2: Create `snippets/linkedin-mobile.css`

**Files:**
- Create: `.claude/skills/BusinessAgents/snippets/linkedin-mobile.css`

- [ ] **Step 1: Write the CSS file**

Write `.claude/skills/BusinessAgents/snippets/linkedin-mobile.css` with this exact content (extracted verbatim from `marketing.md`):

```css
/* ── linkedin-mobile typography & sizing (1080 × 1350) ── */
/* Two headline tiers + body tier + labels tier. Min font: 2.5rem (40px). */

/* Headline tier: 80–90 px */
.hook-headline { font-size: 5.625rem; font-weight: 800; line-height: 1.1;  color: var(--text); margin-bottom: 1.5rem; }
h2             { font-size: 5rem;     font-weight: 700; line-height: 1.12; color: var(--text); margin-bottom: 1.25rem; }
.cta-action    { font-size: 5rem;     font-weight: 800; color: var(--text); line-height: 1.1; margin-bottom: 1rem; }

/* Body tier: 60 px */
p              { font-size: 3.75rem; line-height: 1.55; color: var(--text-muted); margin-bottom: 0.6rem; }
ul             { list-style: none; padding: 0; margin-top: 0.5rem; }
li             { font-size: 3.75rem; line-height: 1.55; color: var(--text-muted); padding: 0.5rem 0 0.5rem 3.5rem; position: relative; }
li::before     { content: "→"; color: var(--accent); position: absolute; left: 0; font-weight: 700; }
.swipe-hint    { font-size: 3.375rem; color: var(--text-muted); margin-top: 1.5rem; }
.big-stat      { font-size: 6.5rem;   font-weight: 800; color: var(--accent); line-height: 1; margin-bottom: 0.5rem; }

/* Labels tier: 44–48 px */
.slide-num     { font-size: 3rem;    font-weight: 700; letter-spacing: 0.12em; color: var(--accent); }
.brand-name    { font-size: 2.75rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }
.kicker        { font-size: 3rem;    font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); margin-bottom: 0.9rem; }
.cta-label     { font-size: 2.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); margin-bottom: 0.75rem; }
.tagline       { font-size: 2.75rem; color: var(--text-muted); }
.accent-bar    { height: 3px; background: var(--accent); border-radius: 2px; width: 40px; }

/* Icons */
.icon          { display: inline-flex; align-items: center; flex-shrink: 0; }
.icon svg      { width: 72px;  height: 72px;  color: var(--accent); }
.icon-lg svg   { width: 120px; height: 120px; }
.icon-md svg   { width: 96px;  height: 96px;  }
.slide-header  { display: flex; align-items: center; gap: 24px; margin-bottom: 1.5rem; }
.hook-icon     { display: flex; justify-content: center; margin-bottom: 2rem; }

/* Infographic — process steps (linkedin-mobile) */
.steps         { display: flex; align-items: flex-start; gap: 0; margin-top: 48px; }
.step          { display: flex; flex-direction: column; align-items: center; flex: 1; }
.step-circle   { width: 100px; height: 100px; border-radius: 50%; background: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 800; color: var(--bg); margin-bottom: 20px; flex-shrink: 0; }
.step-circle.purple { background: linear-gradient(135deg, #9d2cff, var(--accent)); color: #fff; }
.step-label    { font-size: 3rem; color: rgba(248,250,252,0.85); text-align: center; line-height: 1.3; }
.step-arrow    { flex: 0 0 48px; margin-top: 36px; color: var(--accent); font-size: 2.5rem; font-weight: 700; }

/* Infographic — comparison table (linkedin-mobile, max 3 rows) */
.comp-table    { flex: 1; display: flex; flex-direction: column; gap: 0; margin-top: 40px; }
.comp-header   { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 12px; margin-bottom: 14px; }
.comp-col-label { font-size: 3rem; font-weight: 700; text-align: center; padding: 14px; border-radius: 6px; }
.comp-col-label.old { background: rgba(255,255,255,0.05); color: rgba(248,250,252,0.4); }
.comp-col-label.new { background: rgba(34,211,238,0.15); color: var(--accent); }
.comp-row      { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 12px; margin-bottom: 14px; }
.comp-cell     { font-size: 3rem; padding: 24px 16px; border-radius: 6px; display: flex; align-items: center; justify-content: center; }
/* IMPORTANT: never set font-size on .comp-feature — it inherits from .comp-cell */
.comp-feature  { background: rgba(255,255,255,0.04); color: rgba(248,250,252,0.85); justify-content: flex-start; }
.comp-cell.no  { background: rgba(239,68,68,0.08);  color: #ef4444; font-weight: 700; }
.comp-cell.yes { background: rgba(34,197,94,0.1);   color: #22c55e; font-weight: 700; }
/* ── end linkedin-mobile typography & sizing ── */
```

- [ ] **Step 2: Verify line count**

Run:
```bash
wc -l .claude/skills/BusinessAgents/snippets/linkedin-mobile.css
```

Expected: 46 lines (content may vary by trailing newline — accept 44–48).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BusinessAgents/snippets/linkedin-mobile.css
git commit -m "feat(marketing): extract linkedin-mobile CSS to snippets/linkedin-mobile.css"
```

---

### Task 3: Create `snippets/doc-title.html`

**Files:**
- Create: `.claude/skills/BusinessAgents/snippets/doc-title.html`

- [ ] **Step 1: Write the self-contained component**

Write `.claude/skills/BusinessAgents/snippets/doc-title.html` with this content:

```html
<style>
.doc-title-row { margin-bottom: 1.1rem; }
.doc-title-label { font-size: 0.78rem; color: #64748b; display: block; margin-bottom: 0.35rem; }
.doc-title-value { color: #f8fafc; font-size: 1rem; font-weight: 600; background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 0.65rem 1rem; }
</style>
<div class="doc-title-row">
  <span class="doc-title-label">Document title (paste into LinkedIn when uploading)</span>
  <div class="doc-title-value" id="docTitle">{{generated-title}}</div>
  <button class="copy-btn" style="margin-top:0.5rem" onclick="copyTitle()">Copy title</button>
</div>
<script>
function copyTitle() {
  navigator.clipboard.writeText(document.getElementById('docTitle').innerText).then(() => {
    const btns = document.querySelectorAll('.copy-btn');
    btns[0].textContent = 'Copied!';
    setTimeout(() => btns[0].textContent = 'Copy title', 1800);
  });
}
</script>
```

Note: `.copy-btn` is defined in `carousel-base.html`'s base CSS — this snippet reuses it without redefining it.

- [ ] **Step 2: Verify the placeholder is present**

Run:
```bash
grep "{{generated-title}}" .claude/skills/BusinessAgents/snippets/doc-title.html
```

Expected: one match on the `id="docTitle"` line.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BusinessAgents/snippets/doc-title.html
git commit -m "feat(marketing): extract document title component to snippets/doc-title.html"
```

---

### Task 4: Create `snippets/caption-tabs.html`

**Files:**
- Create: `.claude/skills/BusinessAgents/snippets/caption-tabs.html`

- [ ] **Step 1: Write the self-contained component**

Write `.claude/skills/BusinessAgents/snippets/caption-tabs.html` with this content:

```html
<style>
.caption-box { margin-top: 1.5rem; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem 1.5rem; max-width: 700px; width: 100%; }
.caption-box h3 { color: #f8fafc; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
.caption-hint { color: #64748b; font-size: 0.8rem; margin-bottom: 0.9rem; }
.caption-tabs { display: flex; gap: 0.5rem; margin-bottom: 0.9rem; }
.caption-tab { background: #0f172a; border: 1px solid #334155; color: #94a3b8; border-radius: 6px; padding: 0.35rem 0.85rem; font-size: 0.78rem; font-weight: 600; cursor: pointer; }
.caption-tab.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.caption-text { color: #cbd5e1; font-size: 0.9rem; line-height: 1.75; white-space: pre-wrap; background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 1rem; margin-bottom: 0.9rem; }
@media print { .caption-box { display: none !important; } }
</style>
<div class="caption-box">
  <h3>Suggested post caption</h3>
  <p class="caption-hint">Pick a version, copy it into LinkedIn when you upload the PDF, and edit as needed.</p>
  <div class="caption-tabs">
    <button class="caption-tab active" onclick="switchCaption('short', this)">Short</button>
    <button class="caption-tab" onclick="switchCaption('long', this)">Long</button>
  </div>
  <div class="caption-text" id="captionText">{{short-caption}}</div>
  <button class="copy-btn" onclick="copyCaption()">Copy caption</button>
</div>
<script>
const captions = {
  short: `{{short-caption}}`,
  long: `{{long-caption}}`
};
function switchCaption(key, btn) {
  document.getElementById('captionText').textContent = captions[key];
  document.querySelectorAll('.caption-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
}
function copyCaption() {
  const el = document.getElementById('captionText');
  navigator.clipboard.writeText(el.innerText).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy caption', 1800);
  });
}
</script>
```

- [ ] **Step 2: Verify both placeholders are present**

Run:
```bash
grep -c "{{" .claude/skills/BusinessAgents/snippets/caption-tabs.html
```

Expected: `3` (one `{{short-caption}}` in the visible div, one `{{short-caption}}` and one `{{long-caption}}` in the JS object).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BusinessAgents/snippets/caption-tabs.html
git commit -m "feat(marketing): extract caption tab switcher to snippets/caption-tabs.html"
```

---

### Task 5: Create `templates/carousel-base.html`

**Files:**
- Create: `.claude/skills/BusinessAgents/templates/carousel-base.html`

- [ ] **Step 1: Write the template**

Write `.claude/skills/BusinessAgents/templates/carousel-base.html` with this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{carousel-title}} — LinkedIn Carousel</title>
<style>
  :root {
    --bg: {{bg}};
    --accent: {{accent}};
    --text: {{text}};
    --text-muted: {{text-muted}};
    --card-w: {{card-w}}px;
    --card-h: {{card-h}}px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #080810; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 2rem 1rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }
  .deck { position: relative; width: var(--card-w); height: var(--card-h); border-radius: 12px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.6); flex-shrink: 0; }
  .card { position: absolute; inset: 0; background: var(--bg); color: var(--text); display: none; flex-direction: column; padding: 48px; overflow: hidden; }
  .card-bg { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
  .card-scrim { position: absolute; inset: 0; background: rgba(13,31,60,0.72); pointer-events: none; z-index: 1; }
  .card-top, .card-body, .card-bottom { position: relative; z-index: 2; }
  .card.active { display: flex; }
  .card-top { display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid rgba(128,128,128,0.15); margin-bottom: 8px; }
  .slide-num { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.12em; color: var(--accent); }
  .brand-name { font-size: 0.75rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }
  .card-body { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 20px 0; }
  .card-bottom { padding-top: 20px; border-top: 1px solid rgba(128,128,128,0.15); }
  .hook-headline { font-size: 2.8rem; font-weight: 800; line-height: 1.12; color: var(--text); margin-bottom: 1.25rem; }
  h2 { font-size: 1.75rem; font-weight: 700; line-height: 1.2; color: var(--text); margin-bottom: 1.25rem; }
  .kicker { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); margin-bottom: 0.75rem; }
  p { font-size: 1rem; line-height: 1.7; color: var(--text-muted); margin-bottom: 0.6rem; }
  ul { list-style: none; padding: 0; margin-top: 0.25rem; }
  li { font-size: 1rem; line-height: 1.65; color: var(--text-muted); padding: 0.4rem 0 0.4rem 1.4rem; position: relative; }
  li::before { content: "→"; color: var(--accent); position: absolute; left: 0; font-weight: 700; }
  .big-stat { font-size: 4rem; font-weight: 800; color: var(--accent); line-height: 1; margin-bottom: 0.5rem; }
  .swipe-hint { font-size: 0.88rem; color: var(--text-muted); margin-top: 1.25rem; }
  .cta-label { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); margin-bottom: 0.6rem; }
  .cta-action { font-size: 2rem; font-weight: 800; color: var(--text); line-height: 1.15; margin-bottom: 0.8rem; }
  .tagline { font-size: 0.85rem; color: var(--text-muted); }
  .accent-bar { height: 3px; background: var(--accent); border-radius: 2px; width: 40px; }
  .nav { display: flex; align-items: center; gap: 1rem; margin-top: 1.5rem; }
  .nav-btn { background: #1e293b; border: 1px solid #334155; color: #f8fafc; width: 42px; height: 42px; border-radius: 50%; cursor: pointer; font-size: 1rem; display: flex; align-items: center; justify-content: center; }
  .nav-btn:hover { background: #334155; }
  .dots { display: flex; gap: 6px; align-items: center; }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: #334155; cursor: pointer; transition: background 0.15s, width 0.15s; }
  .dot.active { background: var(--accent); width: 20px; border-radius: 4px; }
  .instructions { margin-top: 2rem; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem 1.5rem; max-width: 700px; width: 100%; }
  .instructions h3 { color: #f8fafc; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.75rem; }
  .instructions ol { padding-left: 1.25rem; }
  .instructions li { color: #94a3b8; font-size: 0.85rem; line-height: 1.65; padding: 0; }
  .instructions li::before { display: none; }
  .copy-btn { background: var(--accent); color: #fff; border: none; border-radius: 6px; padding: 0.5rem 1.1rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; }
  .copy-btn:hover { opacity: 0.88; }
  @media print {
    @page { size: var(--card-w) var(--card-h); margin: 0; }
    body { background: var(--bg); padding: 0; display: block; }
    .deck { border-radius: 0; box-shadow: none; overflow: visible; height: auto; width: var(--card-w); position: static; }
    .card { position: relative; display: flex !important; page-break-after: always; break-after: page; height: var(--card-h); }
    .nav, .instructions { display: none !important; }
  }
</style>
</head>
<body>
<div class="deck">
<!-- SLIDES_PLACEHOLDER -->
</div>

<div class="nav">
  <button class="nav-btn" onclick="go(-1)">←</button>
  <div class="dots" id="dots"></div>
  <button class="nav-btn" onclick="go(1)">→</button>
</div>

<div class="instructions">
  <h3>How to export to LinkedIn</h3>
  <ol>
    <li>Open <strong>File → Print</strong> (or Ctrl+P / Cmd+P) in your browser</li>
    <li>Set destination to <strong>Save as PDF</strong></li>
    <li>Under "More settings", set paper size to <strong>Custom</strong> and enter <strong>{{card-w}} × {{card-h}}</strong></li>
    <li>Disable headers and footers</li>
    <li>Save the PDF — each slide becomes one page</li>
    <li>On LinkedIn, start a new post → click the <strong>document icon</strong> → upload the PDF</li>
    <li>LinkedIn displays each page as one carousel slide — add your post caption and publish</li>
  </ol>
</div>

<!-- DOC_TITLE_PLACEHOLDER -->
<!-- CAPTION_TABS_PLACEHOLDER -->

<script>
  const cards = document.querySelectorAll('.card');
  const dotsEl = document.getElementById('dots');
  let cur = 0;
  cards.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'dot' + (i === 0 ? ' active' : '');
    d.onclick = () => show(i);
    dotsEl.appendChild(d);
  });
  function show(n) {
    cards[cur].classList.remove('active');
    document.querySelectorAll('.dot')[cur].classList.remove('active');
    cur = (n + cards.length) % cards.length;
    cards[cur].classList.add('active');
    document.querySelectorAll('.dot')[cur].classList.add('active');
  }
  function go(d) { show(cur + d); }
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') go(1);
    if (e.key === 'ArrowLeft') go(-1);
  });
</script>
</body>
</html>
```

- [ ] **Step 2: Verify all seven `{{placeholders}}` and three `<!-- MARKERS -->` are present**

Run:
```bash
grep -o "{{[^}]*}}" .claude/skills/BusinessAgents/templates/carousel-base.html | sort -u
```

Expected output (7 unique placeholders):
```
{{accent}}
{{bg}}
{{card-h}}
{{card-w}}
{{carousel-title}}
{{text-muted}}
{{text}}
```

Run:
```bash
grep "PLACEHOLDER\|SLIDES_PLACEHOLDER\|DOC_TITLE\|CAPTION_TABS" .claude/skills/BusinessAgents/templates/carousel-base.html
```

Expected: 3 lines — one per marker.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BusinessAgents/templates/carousel-base.html
git commit -m "feat(marketing): extract carousel HTML template to templates/carousel-base.html"
```

---

### Task 6: Update `marketing.md` — replace the five inline blocks

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

There are five edits. Apply them one at a time using the Edit tool. Verify line count after each.

---

#### Edit 6a — Replace HTML template block with Read instruction

Find this exact string (the template intro line and opening of the code fence):

```
Use this base HTML template and fill in all slide content:

```html
<!DOCTYPE html>
<html lang="en">
```

Replace with:

```
Read `.claude/skills/BusinessAgents/templates/carousel-base.html`. Substitute all `{{placeholder}}` markers with session values:

| Placeholder | Value |
|---|---|
| `{{carousel-title}}` | Generated carousel title |
| `{{bg}}` | Background color hex |
| `{{accent}}` | Accent color hex |
| `{{text}}` | `#f8fafc` if dark bg · `#0f172a` if light bg |
| `{{text-muted}}` | `rgba(248,250,252,0.65)` if dark bg · `rgba(15,23,42,0.55)` if light bg |
| `{{card-w}}` | Format width in px (e.g. `1080`) |
| `{{card-h}}` | Format height in px (e.g. `1080`) |

Replace `<!-- SLIDES_PLACEHOLDER -->` with all generated `.card` divs (see slide structure below).

Replace `<!-- DOC_TITLE_PLACEHOLDER -->` and `<!-- CAPTION_TABS_PLACEHOLDER -->` by reading and injecting the snippets per the Post Caption section below.

If format is `linkedin-mobile`: read `.claude/skills/BusinessAgents/snippets/linkedin-mobile.css` and append its contents inside the `<style>` tag, after the base CSS.

After substituting the CSS custom properties, apply every entry in `<format-typography>` as an override — replace the matching default value in the CSS with the stored value. If `<format-typography>` is empty, skip this step.
```

- [ ] **Step 1: Apply Edit 6a**

Use the Edit tool. The `old_string` starts at `Use this base HTML template` and ends just before the closing ` ``` ` of the HTML code fence (line ~934 in the original). The `old_string` must include the full HTML template block. Use this as old_string:

```
Use this base HTML template and fill in all slide content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Carousel Title] — LinkedIn Carousel</title>
```

and the new_string as shown above (beginning with `Read \`.claude/skills/BusinessAgents/templates/carousel-base.html\`.`).

**Important:** The full old_string spans from `Use this base HTML template` through the closing ` ``` ` on its own line after `</html>`. Include the entire block. The closing fence is followed by a blank line and then `Replace all \`[TOTAL]\``.

- [ ] **Step 2: Verify the replacement landed**

Run:
```bash
grep -n "carousel-base.html" .claude/skills/BusinessAgents/marketing.md
```

Expected: one line showing the Read instruction.

Run:
```bash
grep -n "Use this base HTML template" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output (the old text is gone).

---

#### Edit 6b — Replace the `### Post Caption` doc-title HTML block

Find this exact string:

```
Add this above the caption tabs in the HTML:
```html
<div class="doc-title-row">
  <span class="doc-title-label">Document title (paste into LinkedIn when uploading)</span>
  <div class="doc-title-value" id="docTitle">[Generated title]</div>
  <button class="copy-btn" style="margin-top:0.5rem" onclick="copyTitle()">Copy title</button>
</div>
```

Add to CSS:
```css
.doc-title-row { margin-bottom: 1.1rem; }
.doc-title-label { font-size: 0.78rem; color: #64748b; display: block; margin-bottom: 0.35rem; }
.doc-title-value { color: #f8fafc; font-size: 1rem; font-weight: 600; background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 0.65rem 1rem; }
```

Add to JS:
```js
function copyTitle() {
  navigator.clipboard.writeText(document.getElementById('docTitle').innerText).then(() => {
    const btns = document.querySelectorAll('.copy-btn');
    btns[0].textContent = 'Copied!';
    setTimeout(() => btns[0].textContent = 'Copy title', 1800);
  });
}
```
```

Replace with:

```
Read `.claude/skills/BusinessAgents/snippets/doc-title.html`. Substitute `{{generated-title}}` with the actual document title text. Replace `<!-- DOC_TITLE_PLACEHOLDER -->` in the assembled HTML with the full snippet content.
```

- [ ] **Step 3: Apply Edit 6b using the Edit tool**

- [ ] **Step 4: Verify**

Run:
```bash
grep -n "snippets/doc-title.html" .claude/skills/BusinessAgents/marketing.md
```

Expected: one line.

Run:
```bash
grep -n "doc-title-row" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output (the old HTML is gone).

---

#### Edit 6c — Replace the caption-tabs HTML block

Find this exact string:

```
Add this block to the HTML immediately after the `</div>` closing the `.instructions` block:

```html
<div class="caption-box">
  <h3>Suggested post caption</h3>
  <p class="caption-hint">Pick a version, copy it into LinkedIn when you upload the PDF, and edit as needed.</p>
  <div class="caption-tabs">
    <button class="caption-tab active" onclick="switchCaption('short', this)">Short</button>
    <button class="caption-tab" onclick="switchCaption('long', this)">Long</button>
  </div>
  <div class="caption-text" id="captionText">[Short caption text — shown by default]</div>
  <button class="copy-btn" onclick="copyCaption()">Copy caption</button>
</div>
```

Add these styles inside `<style>`:
```css
.caption-box { margin-top: 1.5rem; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem 1.5rem; max-width: 700px; width: 100%; }
.caption-box h3 { color: #f8fafc; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
.caption-hint { color: #64748b; font-size: 0.8rem; margin-bottom: 0.9rem; }
.caption-tabs { display: flex; gap: 0.5rem; margin-bottom: 0.9rem; }
.caption-tab { background: #0f172a; border: 1px solid #334155; color: #94a3b8; border-radius: 6px; padding: 0.35rem 0.85rem; font-size: 0.78rem; font-weight: 600; cursor: pointer; }
.caption-tab.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.caption-text { color: #cbd5e1; font-size: 0.9rem; line-height: 1.75; white-space: pre-wrap; background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 1rem; margin-bottom: 0.9rem; }
.copy-btn { background: var(--accent); color: #fff; border: none; border-radius: 6px; padding: 0.5rem 1.1rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; }
.copy-btn:hover { opacity: 0.88; }
@media print { .caption-box { display: none !important; } }
```

Add these functions inside `<script>`:
```js
const captions = {
  short: `[Short caption text]`,
  long: `[Long caption text]`
};
function switchCaption(key, btn) {
  document.getElementById('captionText').textContent = captions[key];
  document.querySelectorAll('.caption-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
}
function copyCaption() {
  const el = document.getElementById('captionText');
  navigator.clipboard.writeText(el.innerText).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy caption', 1800);
  });
}
```
```

Replace with:

```
Read `.claude/skills/BusinessAgents/snippets/caption-tabs.html`. Substitute `{{short-caption}}` and `{{long-caption}}` with the generated caption texts. Replace `<!-- CAPTION_TABS_PLACEHOLDER -->` in the assembled HTML with the full snippet content.
```

- [ ] **Step 5: Apply Edit 6c using the Edit tool**

- [ ] **Step 6: Verify**

Run:
```bash
grep -n "snippets/caption-tabs.html" .claude/skills/BusinessAgents/marketing.md
```

Expected: one line.

Run:
```bash
grep -n "caption-box" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output.

---

#### Edit 6d — Replace the `linkedin-mobile` CSS verbatim block

Find the section heading and opening of the block:

```
### Base CSS block for `linkedin-mobile` — copy verbatim

**This block is for `linkedin-mobile` (1080 × 1350) only.**
```

The full block ends just before `### Post Caption`.

Replace the entire section — from `### Base CSS block for \`linkedin-mobile\`` through the closing ` ``` ` — with:

```
### Base CSS block for `linkedin-mobile`

If format is `linkedin-mobile`: Read `.claude/skills/BusinessAgents/snippets/linkedin-mobile.css` and append its full contents inside the `<style>` tag, after the base CSS. This block applies the two-tier headline + body + labels sizing (min font 2.5rem, no element below 40px) and all infographic sizing for this format.
```

- [ ] **Step 7: Apply Edit 6d using the Edit tool**

- [ ] **Step 8: Verify**

Run:
```bash
grep -n "snippets/linkedin-mobile.css" .claude/skills/BusinessAgents/marketing.md
```

Expected: at least one line (the Read instruction).

Run:
```bash
grep -n "copy verbatim" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output (the old section heading is gone).

---

#### Edit 6e — Replace the PDF Export script block

Find this exact string (the "Steps" section intro and start of Step 1):

```
### Steps

1. **Write** a Python script to `<carousel-subfolder>/generate-pdf.py` using the Write tool. Fill in the three constants at the top with actual values from this session (`<format-w>`, `<format-h>`, and the real slide count). Do NOT echo the HTML or any file contents — just write the script.

```python
```

The block ends just before step 2: `2. **Run the script** via the Bash tool`.

Replace from `### Steps` through the closing ` ``` ` of the Python block with:

```
### Steps

1. **Run the PDF generation script** via the Bash tool:

```bash
python .claude/skills/BusinessAgents/scripts/generate-pdf.py \
  --width <format-w> \
  --height <format-h> \
  --slides <slide-count> \
  --html <full-path-to-carousel-html> \
  --pdf <full-path-to-output-pdf> \
  2>&1 | tail -3
```

Where `<full-path-to-carousel-html>` and `<full-path-to-output-pdf>` are the paths used when saving the HTML file. Paths are relative to the project root.
```

Then find and update step 2 (renumber it):

Find:
```
2. **Run the script** via the Bash tool (suppress verbose output — only show the last 3 lines):
```
cd <carousel-subfolder> && python generate-pdf.py 2>&1 | tail -3
```
```

Replace with:

```
2. Confirm the `PDF saved:` line appears in the output.
```

And find and remove step 3 (it's now merged into step 2):

Find:
```
3. Confirm the `PDF saved:` line appears. If the script errors, show the error message and ask the founder if they want to skip the PDF step and use the HTML export instructions instead.
```

Replace with:

```
If the script errors, show the error message and ask the founder if they want to skip the PDF step and use the HTML export instructions instead.
```

- [ ] **Step 9: Apply Edit 6e (three sub-edits) using the Edit tool**

- [ ] **Step 10: Verify**

Run:
```bash
grep -n "scripts/generate-pdf.py" .claude/skills/BusinessAgents/marketing.md
```

Expected: one line showing the Bash command.

Run:
```bash
grep -n "Write.*Python script\|fill in the three constants" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output.

---

#### Edit 6f — Update the Hard Rules section (one PDF rule)

Find:
```
- PDF generation: write a self-contained Python script (`generate-pdf.py`) to the carousel subfolder, run it with `python generate-pdf.py 2>&1 | tail -3`, confirm "PDF saved:" appears — zero binary data enters the conversation context
- The script uses Playwright (headless Chromium) to screenshot each slide individually at exact card dimensions, then ReportLab to assemble the PDF — never use Scrapling MCP tools for the PDF step
- Always delete the temporary print-view HTML, per-slide PNGs, and the script itself inside the script after the PDF is saved
```

Replace with:

```
- PDF generation: run `.claude/skills/BusinessAgents/scripts/generate-pdf.py` with `--width`, `--height`, `--slides`, `--html`, and `--pdf` args; confirm "PDF saved:" appears — zero binary data enters the conversation context
- The script uses Playwright (headless Chromium) to screenshot each slide individually at exact card dimensions, then ReportLab to assemble the PDF — never use Scrapling MCP tools for the PDF step
- Always delete the temporary print-view HTML and per-slide PNGs inside the script after the PDF is saved (the script itself lives in `scripts/` and is never deleted)
```

- [ ] **Step 11: Apply Edit 6f using the Edit tool**

- [ ] **Step 12: Commit all marketing.md changes**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): replace inline code blocks with external file references"
```

---

### Task 7: Verify line count reduction and final check

**Files:**
- Read: `.claude/skills/BusinessAgents/marketing.md`

- [ ] **Step 1: Check new line count**

Run:
```bash
wc -l .claude/skills/BusinessAgents/marketing.md
```

Expected: between 1000 and 1100 lines (target ~1030; anything above 1100 means a block wasn't fully removed).

- [ ] **Step 2: Check no old inline blocks remain**

Run:
```bash
grep -n "<!DOCTYPE html>" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output.

```bash
grep -n "\.hook-headline { font-size: 5\.625rem" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output.

```bash
grep -n "CARD_W\s*=" .claude/skills/BusinessAgents/marketing.md
```

Expected: no output.

- [ ] **Step 3: Check new references are all present**

Run:
```bash
grep -n "skills/BusinessAgents/scripts\|skills/BusinessAgents/snippets\|skills/BusinessAgents/templates" .claude/skills/BusinessAgents/marketing.md
```

Expected: at least 5 lines (one per extracted file).

- [ ] **Step 4: Final commit**

```bash
git add -p  # confirm nothing unexpected is staged
git status
git log --oneline -6
```

Expected: 6 commits from this plan, all clean.
