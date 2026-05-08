# Design Spec: Marketing Skill — Code Extraction for Token Efficiency

**Date:** 2026-05-08
**Goal:** Reduce `marketing.md` from 1389 lines (~25,500 tokens) to ~1030 lines by extracting verbatim code blocks and templates into dedicated sibling folders. Primary driver is context window efficiency — the skill is loaded in full on every invocation.

---

## Problem

`marketing.md` embeds ~360 lines of raw code inline:
- A Python PDF generation script (~80 lines) with 5 session-specific values baked in
- A verbatim CSS block for `linkedin-mobile` format (~60 lines)
- An HTML+CSS carousel base template with fill-in points (~170 lines)
- Two HTML+CSS+JS snippets for the document title and caption tab switcher (~50 lines combined)

These blocks inflate every invocation's context load even when they're not yet needed (the PDF script only runs at the end; the linkedin-mobile CSS only applies to one of nine formats).

---

## Solution: Three Sibling Folders

Extract code into three folders alongside `marketing.md`:

```
.claude/skills/BusinessAgents/
  marketing.md                     ← main skill (~1030 lines after extraction)
  scripts/
    generate-pdf.py                ← reusable Python utility (argparse interface)
  snippets/
    linkedin-mobile.css            ← verbatim CSS, linkedin-mobile format only
    doc-title.html                 ← document title HTML + CSS + JS (copy button)
    caption-tabs.html              ← caption tab switcher HTML + CSS + JS
  templates/
    carousel-base.html             ← base HTML+CSS carousel shell with {{placeholders}}
```

All paths referenced in the skill are relative to the project root, consistent with how the skill already reads `memory/` and `outputs/` files.

---

## Extracted Files — Detail

### `scripts/generate-pdf.py`

A reusable CLI utility. Accepts all session-specific values as named arguments — never modified, never copied to the output folder.

**Interface:**
```bash
python .claude/skills/BusinessAgents/scripts/generate-pdf.py \
  --width <format-w> \
  --height <format-h> \
  --slides <slide-count> \
  --html <absolute-or-relative-path-to-html> \
  --pdf <absolute-or-relative-path-to-pdf> \
  2>&1 | tail -3
```

**What it does:** Screenshots each slide individually with Playwright (headless Chromium) at exact card dimensions, assembles them into a PDF with ReportLab, then deletes all temp files. Prints `PDF saved: <path>` on success.

**Skill instruction replaces:** The entire "Write a Python script... [80 lines]" block in the PDF Export section. No Write step, no Read step — just one Bash call with the values the model already holds in memory.

---

### `snippets/linkedin-mobile.css`

The verbatim CSS block currently under "### Base CSS block for `linkedin-mobile` — copy verbatim." Contains all mobile typography overrides (two headline tiers + body tier + labels tier, min font 2.5rem, no font below 40px).

**Skill instruction replaces:** The 60-line CSS block. New instruction: *"Read `.claude/skills/BusinessAgents/snippets/linkedin-mobile.css` and append its contents inside the `<style>` tag, after the base CSS."* Only fires when `<format-slug>` = `linkedin-mobile`.

---

### `templates/carousel-base.html`

The base HTML+CSS carousel shell. Contains all structural HTML, full CSS (layout, card system, navigation, print rules), and JavaScript (keyboard nav, dot indicators, print-to-PDF). Session-specific values are marked with `{{double-brace}}` placeholders; generated content uses `<!-- COMMENT_MARKERS -->` injection points.

**Placeholder reference:**

| Placeholder | Substituted with |
|---|---|
| `{{carousel-title}}` | Generated carousel title (in `<title>` tag) |
| `{{bg}}` | Background color hex |
| `{{accent}}` | Accent color hex |
| `{{text}}` | Text color |
| `{{text-muted}}` | Muted text color |
| `{{card-w}}` | Format width in px (e.g. `1080`) |
| `{{card-h}}` | Format height in px (e.g. `1080`) |
| `<!-- SLIDES_PLACEHOLDER -->` | All generated `.card` divs |
| `<!-- DOC_TITLE_PLACEHOLDER -->` | Content of `snippets/doc-title.html` (with `{{generated-title}}` substituted) |
| `<!-- CAPTION_TABS_PLACEHOLDER -->` | Content of `snippets/caption-tabs.html` (with `{{short-caption}}` and `{{long-caption}}` substituted) |

**Format-specific typography overrides** are not placeholders — the skill instructs the model to apply `<format-typography>` entries by rewriting matching CSS values in the already-read template text. The template stays format-agnostic.

**LinkedIn Mobile CSS injection** — no placeholder in the template. Skill instruction: *"If format is `linkedin-mobile`, read `snippets/linkedin-mobile.css` and append its contents inside the `<style>` tag after the base CSS."* Conditional, lazy.

**Skill instruction replaces:** The "Use this base HTML template..." block and the ~170 lines of inline HTML+CSS.

---

### `snippets/doc-title.html`

The document title block (shown above caption tabs in browser preview, hidden in print). Contains the title display div, copy button, and their CSS and JS.

**Placeholders:** `{{generated-title}}` (the actual title text).

**Skill instruction replaces:** The "Add this above the caption tabs" block.

---

### `snippets/caption-tabs.html`

The two-tab caption switcher (Short / Long). Contains the tab HTML, CSS, and JS toggle logic.

**Placeholders:** `{{short-caption}}`, `{{long-caption}}`.

**Skill instruction replaces:** The "Always generate two caption versions" HTML block.

---

## Assembly Order (HTML generation step)

1. Read `templates/carousel-base.html`
2. Substitute all `{{placeholders}}` with session values
3. If format is `linkedin-mobile`: read `snippets/linkedin-mobile.css`, append inside `<style>` tag
4. Apply `<format-typography>` overrides to CSS values
5. Generate all `.card` divs; replace `<!-- SLIDES_PLACEHOLDER -->`
6. Read `snippets/doc-title.html`; substitute `{{generated-title}}`; replace `<!-- DOC_TITLE_PLACEHOLDER -->`
7. Read `snippets/caption-tabs.html`; substitute `{{short-caption}}` and `{{long-caption}}`; replace `<!-- CAPTION_TABS_PLACEHOLDER -->`
8. Write assembled HTML to `<carousel-output-path>`

---

## What Does NOT Change

- All skill logic, Q&A flow, color suitability check, visual theme loading, slide layout selection, content generation rules, topic validation, registry update — unchanged.
- The Sonnet sub-agent prompt — unchanged.
- Hard Rules section — unchanged (one line in the PDF Export rule is updated to reflect the new Bash command instead of the Write step).
- All other skills — unaffected.

---

## Token Impact

| | Lines | Est. tokens |
|---|---|---|
| Before | 1389 | ~25,500 |
| After | ~1030 | ~18,900 |
| Saved | ~360 | ~6,600 (26%) |

Extracted files are loaded lazily (only when their step executes), not on skill invocation.
