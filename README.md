# BusinessAgents

Nine AI agents that guide a founder from raw idea to validated business — with a brand identity, prospect list, and marketing materials along the way.

Each agent has one focused job. They share memory files and pass outputs to each other, so you never explain your context twice.

---

## What it does

| Step | Agent | What you get |
|------|-------|-------------|
| 1 | `/BusinessAgents:founder` | Startup context saved to memory — vision, constraints, ideal customer |
| 2 | `/BusinessAgents:discover` | Top 3 problems worth solving, ranked by evidence and market timing |
| 3 | `/BusinessAgents:simulate_user` | 1st simulation: hypothesis of what changes for your user |
| 4 | `/BusinessAgents:validate` | Go / No-go verdict + 3 cheap experiments to test before building |
| 5 | `/BusinessAgents:prospects` | Scraped lead list of real companies matching your ICP |
| 6 | `/BusinessAgents:interview` | Interview script, live coaching, insight synthesis |
| 7 | `/BusinessAgents:simulate_user` | 2nd simulation: refined, grounded in what real users told you |
| 8 | `/BusinessAgents:docs` | Business plan, pitch deck, value prop, canvas, and more |

**Optional — run at any point:**

| Agent | What you get |
|-------|-------------|
| `/BusinessAgents:brand` | SVG logo variants, color palette, brand guidelines HTML, Visual Theme Kit (10 backgrounds + 10 infographic layouts) |
| `/BusinessAgents:marketing` | Carousel post in 8 formats (LinkedIn, Instagram, Stories, Pinterest, presentation, and more), with brand backgrounds and infographics injected per slide |

---

## Requirements

- [Claude Code](https://claude.ai/code) (CLI or desktop app)
- [Scrapling MCP server](https://github.com/D4Vinci/Scrapling) — required for `/BusinessAgents:prospects` (scrapes business directories) and `/BusinessAgents:brand` (extracts branding from your website)

Configure Scrapling in `.mcp.json` and enable it in `.claude/settings.local.json`. All other agents work without it.

---

## Getting started

```bash
git clone <this-repo>
cd BusinessAgents
claude  # open Claude Code in this directory
```

Then type:

```
/BusinessAgents:founder
```

This runs a 5-minute onboarding that saves your startup context. All other agents read from it — run this first.

---

## The flow

```
/BusinessAgents:founder        →  Set up memory (run once)
         ↓
/BusinessAgents:discover       →  Find real problems worth solving
         ↓
/BusinessAgents:simulate_user  →  1st run: hypothesis simulation
         ↓
/BusinessAgents:validate       →  Test the top problem. Get a Go/No-go.
         ↓  (Go)
/BusinessAgents:prospects      →  Scrape a lead list of real companies to contact
         ↓
/BusinessAgents:interview      →  Prepare → Coach → Synthesize
         ↓
/BusinessAgents:simulate_user  →  2nd run: refined simulation
         ↓
/BusinessAgents:docs           →  Generate documents and pitch materials
```

**Optional helpers — run at any point:**
- `/BusinessAgents:brand` — build a brand kit before or after any stage
- `/BusinessAgents:marketing` — create a LinkedIn carousel whenever you want to build an audience

You can re-run any agent at any point. If your target customer changes, re-run `founder` in Update mode. If you get a No-go verdict, re-run `validate` on a new problem. To explore a second product idea, use `founder` → "New idea".

---

## Agents

### `/BusinessAgents:founder` — Startup Memory Manager

Runs a short onboarding to capture your vision, constraints, and ideal customer. Stores everything in `memory/` so downstream agents never ask you to repeat yourself.

**Modes:** Initialize · Update · Review · New idea · List ideas · Archive idea

---

### `/BusinessAgents:discover` — Opportunity Discovery Agent

Asks 5 guided questions, then searches forums, reviews, and social signals to find real problems with real demand. Produces a ranked report with evidence and a "Why Now" analysis for each opportunity. Also writes an initial idea-specific ICP based on the research.

**Output:** `outputs/ideas/<slug>/opportunity-discovery-<date>.md`

---

### `/BusinessAgents:validate` — Validation Agent

Designs 3 cheap, fast experiments to test whether a problem is real and whether people will pay. Gives a clear Go / No-go verdict. A No-go is a good outcome — it saves months of building the wrong thing.

**Output:** `outputs/ideas/<slug>/validation-<date>.md`

---

### `/BusinessAgents:prospects` — Client Prospect Agent

Scrapes Yellow Pages, Yelp, and Google Maps to find real companies matching your ICP in a target city. Optional enrichment visits each company's website to find email, employee count, and decision-maker name.

**Requires:** Scrapling MCP server

**Outputs:**
- `outputs/ideas/<slug>/prospects-<date>.md` — formatted lead list
- `outputs/ideas/<slug>/prospects-<date>.csv` — import-ready for any CRM

---

### `/BusinessAgents:interview` — Customer Interview Agent

Guides founders through the full interview lifecycle. Generates a tailored question script and an editable HTML sheet to fill in during calls and export to CSV. Provides live coaching — describe what the interviewee said, get one follow-up question back. After all calls, synthesizes findings: which assumptions held, which broke, what was unexpected. Proposes ICP updates for the founder to confirm.

**Outputs:**
- `outputs/ideas/<slug>/interview-script-<date>.md`
- `outputs/ideas/<slug>/interview-sheet-<date>.html`
- `outputs/ideas/<slug>/interview-coaching-<date>-<N>.md` — per-session log
- `outputs/ideas/<slug>/interview-insights-<date>.md` — synthesis report

---

### `/BusinessAgents:simulate_user` — End User Simulator

Simulates 2–3 real situations where your target user encounters the problem. For each: a before/after workflow table, task-level drill-down, and benefit calculations (time saved, error reduction, cognitive load). All estimates are labeled with reasoning shown.

**Outputs:**
- `outputs/ideas/<slug>/simulation-<persona>-<date>.md` — full report
- `outputs/ideas/<slug>/simulation-<persona>-onepager-<date>.md` — shareable plain-language version

---

### `/BusinessAgents:docs` — Business Documentation Agent

Generates polished business documents from everything captured so far. Choose from a menu. Missing information is marked `[PLACEHOLDER]` — never invented.

**Documents:** Vision & mission · Value proposition · Business Model Canvas · SWOT · Go-to-market strategy · MVP spec · Customer journey map · Financial projections · Competitive landscape · TAM/SAM/SOM · Investor one-pager · Full business plan · User Impact Journey Map

**Slides (self-contained HTML, open in any browser):** Pitch deck · Demo day · Co-founder recruitment · Internal planning

**Outputs:** `outputs/ideas/<slug>/docs/` and `outputs/ideas/<slug>/slides/`

---

### `/BusinessAgents:brand` — Brand Identity Agent

Extracts your existing colors and fonts from your website (if you have one), evaluates the branding, makes suggestions, and generates a full brand kit: SVG logo variants, brand guidelines HTML, and AI image prompts for 8 platforms. Supports company-level brands and idea-specific sub-brands. When suggestions are accepted, generates both an Original kit (current branding preserved) and a Recommended kit (improvements applied) in separate subfolders for easy comparison.

Also generates a **Visual Theme Kit**: 10 branded SVG backgrounds (neural network, circuit board, private vault, server rack, legal scan, blueprint, and more) and 10 infographic layout partials (stats grid, before/after, process steps, timeline, icon grid, comparison table, funnel, progress bars, quote box, hub-and-spoke). The kit is saved to `outputs/brand/recommended/visual-theme/` with a `preview.html` you can open in any browser to review all assets at a glance. The marketing agent reads this kit automatically to inject the right background and infographic into each slide.

**Requires:** Scrapling MCP server (for website extraction)

**Outputs (company brand):**
- `outputs/brand/original/` — current branding preserved
- `outputs/brand/recommended/` — improved version
- `outputs/brand/recommended/visual-theme/` — backgrounds, infographics, preview

**Outputs (idea sub-brand):**
- `outputs/ideas/<slug>/brand/original/`
- `outputs/ideas/<slug>/brand/recommended/`
- `outputs/ideas/<slug>/brand/recommended/visual-theme/`

---

### `/BusinessAgents:marketing` — Carousel Agent

Creates a professional carousel post from your idea in 8 formats: LinkedIn square (1080×1080), Instagram square, Instagram portrait (1080×1350), Stories (1080×1920), Pinterest (1000×1500), presentation (1920×1080), link preview (1200×628), and A4/letter (794×1123).

Choose a topic (problem awareness, before/after journey, tips, or founder story), tone, format, and slide count. Automatically loads your saved brand kit and Visual Theme Kit. Each carousel gets a branded background SVG matched to its topic — and per-slide infographic layouts (stats grid, before/after, progress bars, etc.) injected where content warrants them. On infographic slides the background is suppressed so the layout is the visual, never both at once. Brand selection drives ICP selection: company brand uses your broad audience profile; product brand uses the idea-specific ICP.

**Output:** `outputs/marketing/<format>-<topic>-<date>/carousel-*.html` (company brand) or `outputs/ideas/<slug>/marketing/<format>-<topic>-<date>/carousel-*.html` (idea brand) — open in browser to preview, print to PDF to upload

---

## Memory structure

Memory is split into two levels so you can run multiple product ideas in parallel without mixing contexts.

```
memory/                        ← company-level (gitignored)
  startup-context.md           ← vision, mission, founder constraints
  icp.md                       ← broad market filter — who you serve across all products
  decisions-log.md             ← company-level decisions
  ideas.md                     ← registry of all product ideas
  brand.md                     ← company brand colors and logo paths

outputs/marketing/             ← company-level carousels (gitignored)
  <format>-<topic>-<date>/
    carousel-*.html            ← generated when company brand is used

outputs/ideas/<slug>/          ← idea-specific (gitignored)
  icp.md                       ← detailed ICP for this product (role, size, pain, decision authority)
  decisions-log.md             ← decisions specific to this idea
  opportunity-discovery-*.md
  validation-*.md
  simulation-<persona>-*.md
  prospects-*.md / *.csv
  interview-script-*.md
  interview-sheet-*.html
  interview-insights-*.md
  brand/                       ← idea sub-brand (optional)
    original/
    recommended/
      visual-theme/
  marketing/
    <format>-<topic>-<date>/
      carousel-*.html
  docs/
  slides/

outputs/brand/                 ← company brand assets (gitignored)
  original/                    ← current branding preserved
  recommended/                 ← improved version (active)
    visual-theme/              ← 10 SVG backgrounds + 10 infographic partials + preview.html
```

The company ICP (`memory/icp.md`) is broad — "small-to-mid law firms and engineering companies." Each idea's ICP (`outputs/ideas/<slug>/icp.md`) is specific — "managing partner at a 2–15 lawyer Montreal boutique law firm." Downstream agents use whichever level is appropriate.

---

## Privacy

`memory/` and `outputs/` are gitignored. Your startup context, customer profiles, research reports, simulation outputs, brand assets, and marketing materials stay local — they are never committed to the repository.

Only the agent skill files and project structure are version-controlled. Your data stays yours.

---

## Multiple ideas

Register each product idea separately:

```
/BusinessAgents:founder  →  choose "New idea"
```

Each downstream agent shows a numbered menu so you can pick which idea to work on. All files are scoped to `outputs/ideas/<slug>/` — ideas never mix.

---

## Built with

- [Claude Code](https://claude.ai/code) — the AI coding assistant from Anthropic
- [Scrapling](https://github.com/D4Vinci/Scrapling) — MCP server for web scraping (used by prospects and brand agents)
