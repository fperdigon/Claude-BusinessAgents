# Carousel Visual Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Visual Theme Kit phase to the brand skill (generates 10 SVG backgrounds + 10 infographic snippets with interactive approval) and update the marketing skill to load `visual-theme.md`, ask the founder which platform format to use, select a background per carousel, and inject per-slide infographic layouts.

**Architecture:** Two skill file edits sharing one data contract (`visual-theme.md`). The brand skill writes the kit; the marketing skill reads it. All changes are append/replace edits to existing `.claude/skills/BusinessAgents/brand.md` and `.claude/skills/BusinessAgents/marketing.md` — no new source files, no build step, no tests in the traditional sense. Verification is done by reading the saved skill file and confirming the exact text landed correctly.

**Tech Stack:** Markdown skill files only. SVG (inline, viewBox-based). HTML partials (no `<html>` wrapper). The skills themselves run inside Claude Code sessions — there is no separate runtime to configure.

---

## File Map

| File | Change |
|---|---|
| `.claude/skills/BusinessAgents/brand.md` | Append new "Visual Theme Kit" phase after the existing Brand Memory Update section |
| `.claude/skills/BusinessAgents/marketing.md` | (A) Replace Question 1 platform block with format-aware version; (B) Add visual-theme.md loading + background selection after brand colors confirmed; (C) Add per-slide infographic injection rules into the HTML template section; (D) Update `--card-size` and `@page` size to be format-driven; (E) Update hard rules |

---

## Task 1: Add Visual Theme Kit phase to brand skill — offer + concept derivation

**Files:**
- Modify: `.claude/skills/BusinessAgents/brand.md` — append after the `## Brand Memory Update` section

- [ ] **Step 1: Read the current end of brand.md to find the exact insertion point**

```bash
grep -n "## Brand Memory Update\|## Registry Update\|## Hard Rules" .claude/skills/BusinessAgents/brand.md
```

Expected output: three line numbers. The new section goes between `## Registry Update` and `## Hard Rules`.

- [ ] **Step 2: Read lines around the insertion point to get exact surrounding text**

```bash
sed -n '<registry-update-line>,<hard-rules-line>p' .claude/skills/BusinessAgents/brand.md
```

Note the exact text of the last line before `## Hard Rules` — you will use it as the `old_string` anchor in the Edit tool.

- [ ] **Step 3: Insert the Visual Theme Kit section header + offer + Step 1 (concept derivation)**

Using the Edit tool, insert the following block immediately before `## Hard Rules`:

```markdown

---

## Visual Theme Kit (optional phase)

Run this phase at the end of the brand skill flow, after the Brand Memory Update and Registry Update steps are complete. Ask:

> "Would you like me to generate a Visual Theme Kit for your carousels and slides? It creates 10 background patterns and 10 infographic layouts personalised to your business — the marketing agent will use them automatically. (Takes about 5 minutes)"

If the founder says **no**: skip this entire section. The marketing skill will fall back to built-in defaults.

If the founder says **yes**, run the four steps below.

### Step 1 — Concept derivation (silent)

Read `memory/startup-context.md` and the active brand's industry, niche, core advantage, and technology. Derive 10 visual concepts specific to this company. For each concept define:
- A **name** (e.g. "Private data vault")
- A **visual idea** (what the SVG will show — described in one sentence)
- A **mapping category** chosen from this fixed list:

| Category key | Use when the concept relates to… |
|---|---|
| `ai_technology` | AI models, neural networks, machine learning, automation |
| `infrastructure` | Circuit boards, PCBs, chips, traces |
| `data_analysis` | Charts, graphs, data visualisation |
| `privacy_security` | Locks, vaults, shields, data protection |
| `hardware` | Servers, racks, GPUs, physical compute |
| `legal_workflow` | Documents, contracts, legal processing |
| `engineering` | Blueprints, technical grids, CAD, specs |
| `network_isolation` | Firewalls, local networks, isolated nodes |
| `workflow_change` | Before/after flows, transformation diagrams |
| `local_presence` | City grids, local client maps, regional presence |

Each concept must be specific to what this company actually does — derived from the industry, niche, core advantage, and technology in `startup-context.md`. Do not use generic tech patterns.

Do **not** show the concept list to the founder. Proceed silently to Step 2.

```

- [ ] **Step 4: Verify the insertion landed correctly**

```bash
grep -n "Visual Theme Kit" .claude/skills/BusinessAgents/brand.md
```

Expected: two matches — the section header and the heading inside it.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BusinessAgents/brand.md
git commit -m "feat(brand): add Visual Theme Kit phase — offer + concept derivation (step 1)"
```

---

## Task 2: Brand skill — SVG background generation + interactive browser preview (Step 2)

**Files:**
- Modify: `.claude/skills/BusinessAgents/brand.md` — append Step 2 inside the Visual Theme Kit section

- [ ] **Step 1: Locate the end of Step 1 text**

```bash
grep -n "Proceed silently to Step 2" .claude/skills/BusinessAgents/brand.md
```

Note the line number. The new Step 2 block goes immediately after this line.

- [ ] **Step 2: Insert Step 2 — Background preview round**

Using the Edit tool, replace the line `Do **not** show the concept list to the founder. Proceed silently to Step 2.` with:

```markdown
Do **not** show the concept list to the founder. Proceed silently to Step 2.

### Step 2 — Background preview round (interactive browser)

Generate all 10 SVG backgrounds as card previews sized 700×700. Each SVG:
- Uses `viewBox="0 0 700 700"` and `preserveAspectRatio="xMidYMid slice"`
- Has opacity baked in at generation time: set the overall SVG `opacity` attribute to a value between `0.18` and `0.28` based on visual complexity (busier patterns use lower opacity)
- Uses only the brand's confirmed accent color and primary/background color — no other colors
- Shows the visual concept described in Step 1 (e.g., dots+connections, PCB traces, concentric rings+lock)

**Start the visual companion server (Option A first, Option B fallback):**

Option A — locate the superpowers script dynamically:
```bash
find ~/.claude/plugins/cache -name "start-server.sh" -path "*/brainstorming/scripts/*" | head -1
```
If a path is returned, run:
```bash
<found-path> --project-dir <absolute-path-to-project-root>
```
The server will print a URL (e.g., `http://localhost:NNNNN`). Open `.superpowers/brainstorm/<session-id>/content/` as the content directory.

Option B (fallback if Option A script not found) — create a temp preview folder and serve it:
```bash
mkdir -p /tmp/vt-preview
python3 -m http.server 0 --directory /tmp/vt-preview
```
Tell the founder the URL. In Option B mode, collect all feedback as terminal text — there are no click events.

**Generate the preview HTML file** — write a single HTML file to the content directory named `bg-preview.html` containing all 10 SVG backgrounds displayed as 700×700 card mockups with the brand colors applied, slide counter and brand name in the top bar, and click-to-select interaction (each card toggles a blue border + "✓ Approved" badge when clicked).

Show the founder in terminal:
> "I've opened 10 background previews in your browser at [URL]. Click to approve the ones you want to keep — you can keep fewer than 10. Type 'done' in the terminal when finished, or describe any you'd like changed."

Wait for the founder's response in the terminal. For any background the founder asks to change: regenerate that specific SVG with adjusted visual treatment and update the preview. Iterate until the founder types 'done'.

**Collect the final approved set** — in Option A, read the click-event state from `.superpowers/brainstorm/<session-id>/state/events` to know which cards were approved. In Option B, parse the founder's terminal description.

Store the approved SVG code for each approved background — you will write them to disk in Step 4.

```

- [ ] **Step 3: Verify**

```bash
grep -n "Background preview round\|Option A\|Option B" .claude/skills/BusinessAgents/brand.md | tail -10
```

Expected: the three phrases appear near the end of the file.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/brand.md
git commit -m "feat(brand): add Visual Theme Kit step 2 — SVG background generation and browser approval"
```

---

## Task 3: Brand skill — infographic generation + interactive browser preview (Step 3)

**Files:**
- Modify: `.claude/skills/BusinessAgents/brand.md` — append Step 3 inside the Visual Theme Kit section

- [ ] **Step 1: Locate insertion point**

```bash
grep -n "Store the approved SVG code for each approved background" .claude/skills/BusinessAgents/brand.md
```

Note line number. New content goes after this line.

- [ ] **Step 2: Insert Step 3 — Infographic preview round**

Using the Edit tool, append immediately after `Store the approved SVG code for each approved background — you will write them to disk in Step 4.`:

```markdown

### Step 3 — Infographic preview round (interactive browser)

Generate all 10 infographic layout types as 700×700 card previews. Each infographic is populated with **real content** from `memory/startup-context.md` and any available output files — never placeholder text. Use the brand's confirmed colors throughout.

The 10 layout types and their content rules:

| Layout key | File to save | Content rules |
|---|---|---|
| `how_it_works` | `infographic-process-steps.html` | 3–5 ordered steps showing how the product/service works. Steps flow left→right or top→bottom with numbered circles and short labels. |
| `comparison` | `infographic-before-after.html` | Two-column split: left = "Before" (problem state), right = "After" (solution state). 3–4 contrast points per column. |
| `results` | `infographic-stats-grid.html` | 4–6 metric tiles in a 2×2 or 2×3 grid. Each tile: large number + short label. Numbers must be real estimates from startup context or validation outputs — never fabricated. |
| `journey` | `infographic-timeline.html` | 4–6 dated or ordered events on a horizontal or vertical timeline. Use real milestones from startup context (founding, first client, product launch, etc.). |
| `capabilities` | `infographic-icon-grid.html` | 6 capability tiles in a 3×2 grid. Each tile: brand SVG icon (fetched live from icon library URL in `memory/brand.md`) + short label. **Never use emoji.** |
| `versus` | `infographic-comparison-table.html` | 2-column table: "Old way" vs "With [product]". 4–6 comparison rows. Checkmarks/X marks styled with brand colors. |
| `pipeline` | `infographic-funnel.html` | 4–5 stage funnel or pipeline diagram. Each stage: label + short outcome. Wide at top, narrow at bottom (or left→right). |
| `improvements` | `infographic-progress-bars.html` | 4–6 horizontal progress bars. Each bar: label + percentage. **All metrics must be stated positively** — what increases, not what decreases. Never show "−X%". Invert: "Review time reduced 97%" → "Review time reclaimed: 97%". |
| `testimonial` | `infographic-quote-box.html` | Style D only: contained quote box with a small inline SVG quote-mark icon (not a large `"` character), quote text inside a subtle framed box, attribution below. Only use a real quote if one exists in interview outputs — otherwise use a plausible hypothetical framed as an illustrative example. |
| `use_cases` | `infographic-hub-spoke.html` | Central hub (product/company name) with 4–6 spokes radiating outward, each spoke ending in a use-case label. |

Each infographic is saved as an **HTML partial snippet** — content and inline `<style>` only, **no `<html>`, `<head>`, or `<body>` wrapper**. It must work when dropped directly into a `.card-body` element.

**Generate the preview HTML file** — write `infographic-preview.html` to the content directory. Show all 10 infographic layouts as 700×700 card mockups with the brand colors, with click-to-select interaction (same approval UX as backgrounds).

Show the founder in terminal:
> "I've opened 10 infographic layout previews in your browser. Click to approve the ones you want to keep. Type 'done' when finished, or describe any layouts you'd like changed."

Wait for response. Iterate on rejected layouts. Collect the final approved set.

**Hard rules for infographic previews:**
- `capabilities` (icon grid): always fetch SVG icons live from the brand's icon library URL in `memory/brand.md` — never use emoji or reconstruct paths from memory
- `improvements` (progress bars): all metric labels must state what increases — invert negative statements
- `testimonial` (quote box): always use style D (contained box + small SVG quote icon) — never the large standalone `"` character

```

- [ ] **Step 3: Verify**

```bash
grep -n "Infographic preview round\|infographic-hub-spoke\|HTML partial snippet" .claude/skills/BusinessAgents/brand.md | tail -5
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/brand.md
git commit -m "feat(brand): add Visual Theme Kit step 3 — infographic generation and browser approval"
```

---

## Task 4: Brand skill — save assets + write visual-theme.md + close server (Step 4)

**Files:**
- Modify: `.claude/skills/BusinessAgents/brand.md` — append Step 4 + hard rules additions

- [ ] **Step 1: Locate insertion point**

```bash
grep -n "Collect the final approved set\." .claude/skills/BusinessAgents/brand.md | tail -1
```

Note line number. New content goes after that line.

- [ ] **Step 2: Insert Step 4 — Save assets**

Using the Edit tool, append immediately after `Collect the final approved set.` (the second occurrence — in the infographic section):

```markdown

### Step 4 — Save assets and write visual-theme.md

**Determine the output folder:**
- If `<dual-output>` = true → `<brand-output-path>recommended/visual-theme/`
- If `<dual-output>` = false → `<brand-output-path>visual-theme/`
- For idea-scoped brands → `outputs/ideas/<working-slug>/brand/recommended/visual-theme/`

Write each approved SVG background to `<visual-theme-folder>/bg-<concept-slug>.svg` where `<concept-slug>` is a lowercase hyphenated version of the concept name (e.g., "Private data vault" → `bg-private-vault.svg`).

Write each approved infographic partial to `<visual-theme-folder>/<infographic-filename>` using the filename from the layout table above (e.g., `infographic-process-steps.html`).

Write `<visual-theme-folder>/visual-theme.md` with this exact structure, populated with only the approved items:

```markdown
# Visual Theme Kit

## Formats
- linkedin-carousel (1080 × 1080)
- instagram-square (1080 × 1080)
- instagram-portrait (1080 × 1350)
- stories (1080 × 1920)
- pinterest (1000 × 1500)
- presentation (1920 × 1080)
- link-preview (1200 × 628)
- a4-letter (794 × 1123)

## Icon Library
- Source: [library name from memory/brand.md]
- Fetch URL: [fetch URL pattern from memory/brand.md]
- Recommended: [comma-separated list of icon names saved in the brand kit]

## Backgrounds
| Category | File |
|---|---|
[one row per approved background — e.g.: | ai_technology | bg-neural-network.svg |]
| default | [filename of the first approved background] |

## Infographics
| Layout key | File |
|---|---|
[one row per approved infographic layout]
```

**Close the visual companion server** after all files are written:
- Option A: the superpowers server will auto-stop when the session ends, or tell the founder they can close the browser tab
- Option B: `Ctrl+C` the Python server process

Tell the founder:
> "Visual Theme Kit saved to `[visual-theme-folder]`. The marketing agent will use it automatically from your next carousel session."

```

- [ ] **Step 3: Add Visual Theme Kit hard rules to the existing Hard Rules section**

Find `## Hard Rules` in brand.md and add these lines at the end of the hard rules list:

```markdown
- Never save any background or infographic without founder approval from the interactive preview round
- Feature icon grid preview must always use live-fetched SVG icons from the brand's icon library — never emoji
- Progress bar metrics must always be stated positively — invert the statement if needed
- Quote card must always use style D (contained box + small SVG quote icon) — never the large standalone quotation mark
- Start visual companion server (Option A) first; fall back to Python http.server (Option B) if superpowers scripts not found
- Close the visual companion server after saving assets
- Write all assets to `visual-theme/` inside the active brand's recommended folder
- SVG backgrounds must have opacity baked in (0.18–0.28) — never rely on the marketing skill to set opacity
- Infographic snippets must be HTML partials (no `<html>/<head>/<body>` wrapper) — must work dropped into a `.card-body` element
```

- [ ] **Step 4: Verify final brand.md state**

```bash
grep -n "Step 4\|visual-theme.md\|Close the visual companion\|Hard Rules" .claude/skills/BusinessAgents/brand.md | tail -15
```

Expected: Step 4 heading, visual-theme.md write instruction, server close instruction, and hard rules additions all appear.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BusinessAgents/brand.md
git commit -m "feat(brand): add Visual Theme Kit step 4 — save assets, write visual-theme.md, close server, hard rules"
```

---

## Task 5: Marketing skill — replace platform question with format-aware version

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

The current Question 1 asks "Where will you publish this carousel?" with 4 options (LinkedIn, Instagram, Facebook, Other). This needs to be replaced with a format-aware question that:
1. Loads `visual-theme.md` first (silently) to know which formats are available
2. Presents all 8 supported formats grouped clearly
3. Stores both the `<format-slug>` and `<format-dimensions>` for use in the HTML template

- [ ] **Step 1: Find the exact current Question 1 block**

```bash
grep -n "Question 1\|Where will you publish\|platform-slug" .claude/skills/BusinessAgents/marketing.md | head -10
```

Note the start and end line numbers of the Question 1 block.

- [ ] **Step 2: Read the full Question 1 block**

```bash
sed -n '<start-line>,<end-line>p' .claude/skills/BusinessAgents/marketing.md
```

Copy the exact text for use as `old_string` in the Edit tool.

- [ ] **Step 3: Replace Question 1**

Using the Edit tool, replace the entire Question 1 block (from `**Question 1 — Platform / Destination:**` through the line `Default to \`linkedin\` if the founder skips or is unsure.`) with:

```markdown
**Question 1 — Format:**

*(Different platforms have different dimensions. I'll size the carousel cards exactly right for where you're posting.)*

Before asking this question, silently attempt to read `<brand-output-path>visual-theme/visual-theme.md` (using the output path set in step 4 above). If the file exists, extract the `## Formats` list. If it does not exist, use the full default list of all 8 formats.

Present the available formats as a numbered list:

> "Which platform and format is this for?
>
> **Square (1:1)**
> 1. LinkedIn Carousel — 1080 × 1080 · PDF upload / document post
> 2. Instagram Feed Square — 1080 × 1080 · feed post, carousel
>
> **Portrait**
> 3. Instagram Portrait — 1080 × 1350 · feed post (4:5, max portrait fill)
> 4. Stories — 1080 × 1920 · Instagram / LinkedIn / Facebook full-screen
> 5. Pinterest — 1000 × 1500 · standard pin (2:3)
>
> **Landscape**
> 6. Presentation Slide — 1920 × 1080 · Google Slides / Keynote / PowerPoint
> 7. Link Preview — 1200 × 628 · LinkedIn / Twitter / Facebook shared-link thumbnail
>
> **Document**
> 8. A4 / Letter — 794 × 1123 · PDF one-pager / print leave-behind"

Wait for the founder's choice. Store:
- `<format-slug>` — the slug for the chosen format:
  1 → `linkedin-carousel`, 2 → `instagram-square`, 3 → `instagram-portrait`,
  4 → `stories`, 5 → `pinterest`, 6 → `presentation`, 7 → `link-preview`, 8 → `a4-letter`
- `<format-w>` and `<format-h>` — the pixel dimensions:
  `linkedin-carousel` → 1080×1080, `instagram-square` → 1080×1080,
  `instagram-portrait` → 1080×1350, `stories` → 1080×1920,
  `pinterest` → 1000×1500, `presentation` → 1920×1080,
  `link-preview` → 1200×628, `a4-letter` → 794×1123
- `<format-ratio>` — `square`, `portrait`, `landscape`, or `document`
  (square: linkedin-carousel, instagram-square; portrait: instagram-portrait, stories, pinterest; landscape: presentation, link-preview; document: a4-letter)

Use `<format-slug>` (not the old `<platform-slug>`) as the filename component from this point forward. For formats 1 and 2, the platform label shown in the top-right brand bar is "LinkedIn" and "Instagram" respectively. For formats 3–8, use the platform name from the list above.

```

- [ ] **Step 4: Verify the replacement**

```bash
grep -n "Question 1\|format-slug\|format-w\|format-h\|format-ratio" .claude/skills/BusinessAgents/marketing.md | head -15
```

Expected: Question 1 now references `format-slug` and lists the 8 formats.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): replace platform question with 8-format selection, store format-slug and dimensions"
```

---

## Task 6: Marketing skill — load visual-theme.md + background selection

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

After brand colors are confirmed (end of Question 5 / Color Suitability Check), add visual-theme.md loading and background selection. This happens silently before any HTML generation.

- [ ] **Step 1: Find the insertion point**

```bash
grep -n "Color Suitability Check\|Question 6\|Call to Action" .claude/skills/BusinessAgents/marketing.md | head -5
```

The new block goes between the Color Suitability Check section and Question 6.

- [ ] **Step 2: Read the exact separator line between Color Suitability Check and Question 6**

```bash
sed -n '<color-check-end-line>,<question-6-line>p' .claude/skills/BusinessAgents/marketing.md
```

- [ ] **Step 3: Insert visual-theme.md loading + background selection block**

Using the Edit tool, insert the following block immediately before `**Question 6 — Call to Action:**`:

```markdown
## Visual Theme Loading (silent — runs after brand colors are confirmed)

### Load visual-theme.md

Attempt to read `<brand-output-path>visual-theme/visual-theme.md`. Store as `<has-visual-theme>` = true or false.

If `<has-visual-theme>` = true:
- Parse the `## Backgrounds` table → store as `<bg-map>` (category → filename)
- Parse the `## Infographics` table → store as `<infographic-map>` (layout key → filename)
- Parse the `## Icon Library` section → store recommended icon names as `<brand-icons>`
- Visual theme folder: `<brand-output-path>visual-theme/`

If `<has-visual-theme>` = false:
- `<bg-map>` = empty (will use inline default below)
- `<infographic-map>` = empty (will use plain text layouts)
- `<brand-icons>` = default Heroicons list: cpu-chip, shield-check, document-text, server-stack, clock, light-bulb, users, arrow-trending-up, bolt, lock-closed

### Background selection

Read `memory/startup-context.md` and extract:
- **Company name** and any product names mentioned
- **City / region** (e.g. "Montréal", "Austin", "Berlin")
- **Industry** keywords (e.g. "legal", "engineering", "healthcare")
- **Niche / core advantage** (e.g. "private on-premise AI", "document automation")
- **Technology** keywords (e.g. "GPU", "local LLM", "CAD", "Python")

Build an augmented keyword table by extending the base categories with the extracted terms:
- Add the company's city/region name to `local_presence`
- Add the company name itself to `ai_technology` (or the most relevant category for what they do)
- Add technology keywords to their closest category (GPU → `hardware`, LLM/AI → `ai_technology`, CAD → `engineering`, etc.)

Match the carousel topic title (the founder's own words from Question 2) and the company niche against the augmented table:

| Base keywords (augmented at runtime) | Category |
|---|---|
| AI, model, neural, machine learning, automation, algorithm | `ai_technology` |
| server, hardware, infrastructure, deployment, rack | `hardware` |
| legal, contract, compliance, document, firm, clause | `legal_workflow` |
| engineering, blueprint, technical, spec, RFP, CAD | `engineering` |
| privacy, security, data, isolated, on-premise, vault | `privacy_security` |
| network, firewall, topology, local, isolated | `network_isolation` |
| workflow, process, adoption, transformation, before, after | `workflow_change` |
| city, local, community, neighbour, region, advisor | `local_presence` |
| stat, metric, ROI, result, productivity, number, percentage | `data_analysis` |
| circuit, board, PCB, trace, chip | `infrastructure` |
| no match | `default` |

Store the matched category as `<bg-category>`.

If `<has-visual-theme>` = true:
- Look up `<bg-category>` in `<bg-map>` → get filename
- Read the SVG file from `<visual-theme-folder>/<filename>` — store the full SVG code as `<bg-svg>`

If `<has-visual-theme>` = false:
- Use this inline default SVG as `<bg-svg>` (neural network nodes, opacity 0.22):

```svg
<svg viewBox="0 0 700 700" xmlns="http://www.w3.org/2000/svg" opacity="0.22" preserveAspectRatio="xMidYMid slice">
  <circle cx="120" cy="100" r="5" fill="var(--accent)"/>
  <circle cx="300" cy="180" r="7" fill="var(--accent)"/>
  <circle cx="500" cy="90" r="5" fill="var(--accent)"/>
  <circle cx="200" cy="320" r="6" fill="var(--accent)"/>
  <circle cx="420" cy="280" r="8" fill="var(--accent)"/>
  <circle cx="600" cy="350" r="5" fill="var(--accent)"/>
  <circle cx="150" cy="500" r="6" fill="var(--accent)"/>
  <circle cx="360" cy="460" r="7" fill="var(--accent)"/>
  <circle cx="550" cy="530" r="5" fill="var(--accent)"/>
  <circle cx="250" cy="620" r="6" fill="var(--accent)"/>
  <circle cx="480" cy="650" r="5" fill="var(--accent)"/>
  <line x1="120" y1="100" x2="300" y2="180" stroke="var(--accent)" stroke-width="1"/>
  <line x1="300" y1="180" x2="500" y2="90" stroke="var(--accent)" stroke-width="1"/>
  <line x1="300" y1="180" x2="200" y2="320" stroke="var(--accent)" stroke-width="1"/>
  <line x1="300" y1="180" x2="420" y2="280" stroke="var(--accent)" stroke-width="1"/>
  <line x1="420" y1="280" x2="600" y2="350" stroke="var(--accent)" stroke-width="1"/>
  <line x1="200" y1="320" x2="360" y2="460" stroke="var(--accent)" stroke-width="1"/>
  <line x1="420" y1="280" x2="360" y2="460" stroke="var(--accent)" stroke-width="1"/>
  <line x1="360" y1="460" x2="150" y2="500" stroke="var(--accent)" stroke-width="1"/>
  <line x1="360" y1="460" x2="550" y2="530" stroke="var(--accent)" stroke-width="1"/>
  <line x1="550" y1="530" x2="480" y2="650" stroke="var(--accent)" stroke-width="1"/>
  <line x1="150" y1="500" x2="250" y2="620" stroke="var(--accent)" stroke-width="1"/>
</svg>
```

One background per carousel — all cards use the same `<bg-svg>`.

---

```

- [ ] **Step 4: Verify**

```bash
grep -n "Visual Theme Loading\|bg-category\|bg-svg\|has-visual-theme" .claude/skills/BusinessAgents/marketing.md | head -10
```

Expected: all four variable names appear.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): add visual-theme.md loading and background selection with runtime keyword augmentation"
```

---

## Task 7: Marketing skill — update HTML template for format dimensions + background injection

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

The current HTML template uses hardcoded `700px`. This needs to use `<format-w>` × `<format-h>` and inject the background SVG into every `.card`.

- [ ] **Step 1: Find the CSS custom properties block in the template**

```bash
grep -n "card-size\|700px\|@page" .claude/skills/BusinessAgents/marketing.md | head -10
```

- [ ] **Step 2: Replace the `--card-size` line and `@page` print rule**

Using the Edit tool, replace:
```css
    --card-size: 700px;
```
with:
```css
    --card-w: [format-w]px;
    --card-h: [format-h]px;
```
(The agent fills in actual pixel values from `<format-w>` and `<format-h>` when generating the carousel.)

- [ ] **Step 3: Replace the `.deck` and `.card` size references**

Using the Edit tool, replace:
```css
  .deck { position: relative; width: var(--card-size); height: var(--card-size); border-radius: 12px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.6); flex-shrink: 0; }
  .card { position: absolute; inset: 0; background: var(--bg); color: var(--text); display: none; flex-direction: column; padding: 48px; }
```
with:
```css
  .deck { position: relative; width: var(--card-w); height: var(--card-h); border-radius: 12px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.6); flex-shrink: 0; }
  .card { position: absolute; inset: 0; background: var(--bg); color: var(--text); display: none; flex-direction: column; padding: 48px; overflow: hidden; }
  .card-bg { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
  .card-top, .card-body, .card-bottom { position: relative; z-index: 1; }
```

- [ ] **Step 4: Replace the `@page` print rule**

Using the Edit tool, replace:
```css
    @page { size: 700px 700px; margin: 0; }
    body { background: var(--bg); padding: 0; display: block; }
    .deck { border-radius: 0; box-shadow: none; overflow: visible; height: auto; width: 700px; position: static; }
    .card { position: relative; display: flex !important; page-break-after: always; break-after: page; height: 700px; }
```
with:
```css
    @page { size: var(--card-w) var(--card-h); margin: 0; }
    body { background: var(--bg); padding: 0; display: block; }
    .deck { border-radius: 0; box-shadow: none; overflow: visible; height: auto; width: var(--card-w); position: static; }
    .card { position: relative; display: flex !important; page-break-after: always; break-after: page; height: var(--card-h); }
```

- [ ] **Step 5: Add background SVG injection instruction**

Find the Hook slide template comment `<!-- Slide 01 — Hook -->` and add an instruction immediately above it:

Using the Edit tool, replace:
```html
  <!-- Slide 01 — Hook -->
  <div class="card active">
    <div class="card-top">
```
with:
```html
  <!--
    BACKGROUND INJECTION: Insert the following as the FIRST child of every .card element
    (before .card-top). Use the exact SVG code stored in <bg-svg>:

    <svg class="card-bg" viewBox="0 0 [format-w] [format-h]" xmlns="http://www.w3.org/2000/svg"
         opacity="[baked-in opacity from the SVG file, or 0.22 for default]"
         preserveAspectRatio="xMidYMid slice">
      [SVG path/shape content from <bg-svg> — strip the outer <svg> wrapper and keep only the inner elements]
    </svg>

    The background SVG is the SAME across ALL cards — inject identical code into every card.
  -->

  <!-- Slide 01 — Hook -->
  <div class="card active">
    <div class="card-bg">[inject <bg-svg> content here — see injection instruction above]</div>
    <div class="card-top">
```

- [ ] **Step 6: Update the export instructions text**

Find and replace the hardcoded `700 × 700` in the export instructions HTML:

```bash
grep -n "700 × 700\|700px\|paper size" .claude/skills/BusinessAgents/marketing.md | grep -v "css\|CSS\|@page\|var(--"
```

Replace the static instruction text:
```html
    <li>Under "More settings", set paper size to <strong>Custom</strong> and enter <strong>700 × 700</strong> (or select the closest square option)</li>
```
with:
```html
    <li>Under "More settings", set paper size to <strong>Custom</strong> and enter <strong>[format-w] × [format-h]</strong> (the agent fills in the actual dimensions)</li>
```

- [ ] **Step 7: Verify**

```bash
grep -n "card-w\|card-h\|card-bg\|bg-svg\|BACKGROUND INJECTION" .claude/skills/BusinessAgents/marketing.md | head -10
```

Expected: all five terms appear.

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): format-driven card dimensions and background SVG injection into HTML template"
```

---

## Task 8: Marketing skill — per-slide infographic layout selection + injection rules

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

Add a "Slide Layout Selection" section that tells the agent how to choose an infographic layout per slide and how to inject the HTML partial into the card body. This goes between the Visual Theme Loading section and Question 6.

- [ ] **Step 1: Find the exact insertion point**

```bash
grep -n "One background per carousel\|Question 6\|Call to Action" .claude/skills/BusinessAgents/marketing.md | head -5
```

The new block goes immediately after the line `One background per carousel — all cards use the same \`<bg-svg>\`.` and the `---` separator.

- [ ] **Step 2: Insert the slide layout selection section**

Using the Edit tool, insert the following block immediately before `**Question 6 — Call to Action:**`:

```markdown
### Slide layout selection (evaluated per slide, during content generation)

After deciding what content goes on each slide, evaluate whether it qualifies for an infographic layout. Plain text + bullets is always the fallback.

**Infographic layout adaptation by format ratio:**
- `<format-ratio>` = `portrait` and format = `stories` (1080×1920): prefer vertically-stacked layouts — process steps, stats grid, quote box. Avoid comparison tables and hub-spoke. Icon grid: use 2 columns × 3 rows instead of 3×2.
- `<format-ratio>` = `landscape` (presentation, link-preview): prefer horizontally-arranged layouts — before/after split, comparison table, hub-spoke, icon grid 3×2. Stats grid and funnel adapt well. Process steps: arrange horizontally.
- All other ratios: use layouts as-is.

**Layout trigger rules per template:**

Template 1 — Problem Awareness:

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| "The real cost" | 2+ metrics available | `results` |
| "The real cost" | improvement % available | `improvements` |
| "The real cost" | neither | plain |
| "Why it keeps happening" | always | plain |
| "Old way vs right way" | always | `comparison` |
| "What changes when you fix it" | 3+ distinct outcomes | `use_cases` |
| "What changes when you fix it" | fewer outcomes | plain |
| Deeper evidence (slides 6–8) | pipeline or funnel data | `pipeline` |
| Deeper evidence (slides 6–8) | feature comparison | `versus` |
| Deeper evidence (slides 6–8) | neither | plain |
| CTA | always | plain |

Template 2 — Before/After Journey:

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| Setup | always | plain |
| Before journey phases | always | plain |
| Turning point | always | `comparison` |
| After journey phases | always | plain |
| Summary benefits | time/error/quality metrics present | `results` or `improvements` |
| Summary benefits | no metrics | plain |
| CTA | always | plain |

Template 3 — Tips & Education:

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| Tip slide | tip describes 3–5 ordered steps | `how_it_works` |
| Tip slide | tip compares two approaches | `versus` |
| Tip slide | tip contains 3+ statistics | `results` |
| Tip slide | tip lists 5–6 distinct capabilities | `capabilities` |
| Tip slide | tip has one central idea + 4–6 branches | `use_cases` |
| Tip slide | none of the above | plain |
| "Most important" tip | always | plain |
| CTA | always | plain |

Template 4 — Your Story:

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| Context | always | plain |
| Breaking point | always | plain |
| Journey sequence | 3+ dated or ordered events | `journey` |
| "What changed" | always | `comparison` |
| Lessons for reader | 4–6 distinct lessons | `capabilities` |
| Lessons for reader | fewer than 4 | plain |
| CTA | always | plain |

**Quote / testimonial layout (`testimonial`):**
Only used when an actual quote exists in interview reports (`outputs/ideas/<working-slug>/interview-insights-*.md`) or the founder provides one explicitly during the session. Never fabricated. When triggered, replaces a content slide. Always uses style D (contained box + small SVG quote icon).

**How to inject an infographic layout into a slide:**

When a slide gets a non-plain layout key:
1. Look up the layout key in `<infographic-map>` → get the filename (e.g., `infographic-stats-grid.html`)
2. Read the file from `<visual-theme-folder>/<filename>`
3. The file is an HTML partial — drop its full content into the `.card-body` div, replacing the default headline + bullets structure for that slide
4. Populate all template slots in the partial with the actual slide content derived from memory and outputs
5. If `<has-visual-theme>` = false: skip step 1–3 and always use plain text layout for all slides

**Plain text layout fallback conditions** — always use plain regardless of trigger rule:
- Content is primarily narrative with no structured data
- Fewer data points than the layout minimum (e.g., fewer than 3 steps for process steps)
- `<has-visual-theme>` = false
- The slide content doesn't fit the layout meaningfully after trying

```

- [ ] **Step 3: Verify**

```bash
grep -n "Slide layout selection\|infographic-map\|how_it_works\|use_cases\|plain text layout fallback" .claude/skills/BusinessAgents/marketing.md | head -10
```

Expected: all five phrases appear.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): add per-slide infographic layout selection and injection rules for all 4 templates"
```

---

## Task 9: Marketing skill — update hard rules

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

- [ ] **Step 1: Find the Hard Rules section**

```bash
grep -n "## Hard Rules" .claude/skills/BusinessAgents/marketing.md
```

- [ ] **Step 2: Add new rules at the end of the Hard Rules list**

Using the Edit tool, find the last existing hard rule line (the one ending with `never to the flat \`outputs/\` root`) and append:

```markdown
- Ask which platform/format (Question 1) before asking for a topic — `<format-slug>` and dimensions must be set before any HTML is generated
- Size `.card` elements using `--card-w` and `--card-h` CSS variables set to the exact pixel dimensions of the chosen format — never hardcode 700px
- Apply format-ratio infographic adaptations: `stories` → vertically stacked; `presentation`/`link-preview` → horizontally arranged
- Load `visual-theme.md` silently after brand colors are confirmed — before generating any HTML
- Always read `memory/startup-context.md` to extract company name, city/region, industry, niche, and technology — extend background keyword categories with these terms before matching
- One background SVG per carousel — inject the same `<bg-svg>` into every card, never mix
- Background SVG opacity is baked into the file by the brand skill — inject it as-is, never add or override opacity in CSS
- Infographic layout selection is per-slide, not per-carousel — evaluate each slide independently
- Always fall back to plain text + bullets when content doesn't fit a layout meaningfully
- Quote/testimonial layout requires a real quote — never fabricate one
- If `visual-theme.md` does not exist for the active brand: use the inline default neural-network SVG as background and plain text layouts for all slides
- Use `<format-slug>` as the filename component (replaces `<platform-slug>` from the old naming)
```

- [ ] **Step 3: Verify**

```bash
grep -n "format-slug\|card-w\|visual-theme.md\|baked into" .claude/skills/BusinessAgents/marketing.md | tail -10
```

Expected: all four phrases appear in the hard rules section.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): update hard rules for format-aware sizing, visual theme, and infographic injection"
```

---

## Task 10: Smoke-test the brand skill additions

**Files:**
- Read: `.claude/skills/BusinessAgents/brand.md`

This is a skill file — there is no automated test runner. Verification is done by reading the file and confirming the expected structure is present and consistent.

- [ ] **Step 1: Confirm the Visual Theme Kit phase appears after the Registry Update section**

```bash
grep -n "## Registry Update\|## Visual Theme Kit\|## Hard Rules" .claude/skills/BusinessAgents/brand.md
```

Expected output (line numbers will vary):
```
NNN:## Registry Update
NNN:## Visual Theme Kit (optional phase)
NNN:## Hard Rules
```
The order must be: Registry Update → Visual Theme Kit → Hard Rules.

- [ ] **Step 2: Confirm all four steps are present**

```bash
grep -n "### Step 1\|### Step 2\|### Step 3\|### Step 4" .claude/skills/BusinessAgents/brand.md | tail -10
```

Expected: four step headings inside the Visual Theme Kit section.

- [ ] **Step 3: Confirm the 10 infographic layout keys are all listed**

```bash
grep -c "how_it_works\|infographic-before-after\|infographic-stats-grid\|infographic-timeline\|infographic-icon-grid\|infographic-comparison-table\|infographic-funnel\|infographic-progress-bars\|infographic-quote-box\|infographic-hub-spoke" .claude/skills/BusinessAgents/brand.md
```

Expected: 10 (one match per layout type).

- [ ] **Step 4: Confirm the visual-theme.md template block is present with all required sections**

```bash
grep -n "## Formats\|## Icon Library\|## Backgrounds\|## Infographics" .claude/skills/BusinessAgents/brand.md
```

Expected: all four section headings appear inside the Step 4 block.

- [ ] **Step 5: Confirm hard rules additions are present**

```bash
grep -n "opacity baked in\|HTML partial\|Option A.*Option B" .claude/skills/BusinessAgents/brand.md
```

Expected: all three phrases appear in the hard rules section.

---

## Task 11: Smoke-test the marketing skill additions

**Files:**
- Read: `.claude/skills/BusinessAgents/marketing.md`

- [ ] **Step 1: Confirm Question 1 now lists 8 formats**

```bash
grep -n "linkedin-carousel\|instagram-portrait\|stories\|pinterest\|presentation\|link-preview\|a4-letter" .claude/skills/BusinessAgents/marketing.md | head -10
```

Expected: all 7 non-default slugs appear.

- [ ] **Step 2: Confirm format dimensions are stored**

```bash
grep -n "format-w\|format-h\|format-ratio" .claude/skills/BusinessAgents/marketing.md | head -10
```

Expected: all three variable names appear in the Question 1 block.

- [ ] **Step 3: Confirm visual theme loading block is present**

```bash
grep -n "Visual Theme Loading\|has-visual-theme\|bg-category\|bg-svg" .claude/skills/BusinessAgents/marketing.md
```

Expected: all four terms appear.

- [ ] **Step 4: Confirm infographic layout trigger tables are present for all 4 templates**

```bash
grep -n "Template 1\|Template 2\|Template 3\|Template 4" .claude/skills/BusinessAgents/marketing.md | tail -8
```

Expected: four occurrences in the slide layout selection section (separate from the earlier four occurrences in the content generation section).

- [ ] **Step 5: Confirm CSS uses variable dimensions**

```bash
grep -n "card-w\|card-h\|card-bg" .claude/skills/BusinessAgents/marketing.md | head -5
```

Expected: `--card-w`, `--card-h`, and `.card-bg` all appear in the CSS template.

- [ ] **Step 6: Confirm background injection instruction is present in the HTML template**

```bash
grep -n "BACKGROUND INJECTION\|card-bg" .claude/skills/BusinessAgents/marketing.md
```

Expected: the injection comment and `.card-bg` class both appear.

- [ ] **Step 7: Final commit — bump skill version note**

No version number is tracked in these files. Just confirm git shows the expected changes:

```bash
git log --oneline -10
```

Expected: commits matching the ones made across Tasks 1–9, in order.

---

## Task 12: Marketing skill — update output path and filename example references

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md`

The `Save to:` line and example paths still reference `<platform-slug>`. These must be updated to `<format-slug>` to match the new Question 1 variable.

- [ ] **Step 1: Find the Save to line and example paths**

```bash
grep -n "platform-slug\|topic-slug\|Example paths" .claude/skills/BusinessAgents/marketing.md
```

Note all line numbers where `<platform-slug>` still appears.

- [ ] **Step 2: Replace the Save to line**

Using the Edit tool, replace:
```
Save to: `<carousel-output-path><platform-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>/carousel-<platform-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>.html`

Where:
- `<platform-slug>` = destination platform in lowercase (e.g., `linkedin`, `instagram`, `facebook`)
```
with:
```
Save to: `<carousel-output-path><format-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>/carousel-<format-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>.html`

Where:
- `<format-slug>` = the format chosen in Question 1 (e.g., `linkedin-carousel`, `stories`, `presentation`)
```

- [ ] **Step 3: Update the PDF save path**

Using the Edit tool, replace:
```
8. Save the PDF as: `<carousel-output-path><platform-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>/carousel-<platform-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>.pdf`
```
with:
```
8. Save the PDF as: `<carousel-output-path><format-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>/carousel-<format-slug>-<topic-slug>-<YYYY-MM-DD-HH-MM-SS>.pdf`
```

- [ ] **Step 4: Update the example paths**

Using the Edit tool, replace:
```markdown
Example paths:
- `outputs/marketing/linkedin-how-law-firms-can-use-ai-to-analyze-contracts-2026-05-02-14-35-22/carousel-linkedin-how-law-firms-can-use-ai-to-analyze-contracts-2026-05-02-14-35-22.html`
- `outputs/ideas/my-product-slug/marketing/linkedin-our-mission-and-values-2026-05-02-09-10-04/carousel-linkedin-our-mission-and-values-2026-05-02-09-10-04.html`
```
with:
```markdown
Example paths:
- `outputs/marketing/linkedin-carousel-how-law-firms-can-use-ai-2026-05-02-14-35-22/carousel-linkedin-carousel-how-law-firms-can-use-ai-2026-05-02-14-35-22.html`
- `outputs/ideas/my-product-slug/marketing/stories-our-mission-and-values-2026-05-02-09-10-04/carousel-stories-our-mission-and-values-2026-05-02-09-10-04.html`
- `outputs/marketing/presentation-why-firms-need-ai-2026-05-02-10-00-00/carousel-presentation-why-firms-need-ai-2026-05-02-10-00-00.html`
```

- [ ] **Step 5: Verify no `<platform-slug>` references remain (except in the Registry Update section where it refers to the old value)**

```bash
grep -n "platform-slug" .claude/skills/BusinessAgents/marketing.md
```

Expected: zero matches (or only inside a comment explaining the old naming, if any was left).

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "feat(marketing): rename platform-slug to format-slug in output paths and filename examples"
```
