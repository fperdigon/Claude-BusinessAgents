# BusinessAgents — System Overview

A system of AI agents that guide a founder from raw idea to validated business with professional documentation. Each agent has a focused job. They share memory files and pass outputs to each other so you never repeat yourself.

**Requires:** The `scrapling` MCP server is configured in `.mcp.json` and enabled in `.claude/settings.local.json`. The `/BusinessAgents:prospects` and `/BusinessAgents:brand` agents use it to scrape business directories and extract website branding.

---

## Agents

### 1. `/BusinessAgents:founder` — Startup Memory Manager

**Job:** Set up and maintain the founder's core memory files. All other agents read these files — so this must run first.

**Manages three files:**
- `memory/startup-context.md` — vision, mission, constraints, priorities
- `memory/icp.md` — Ideal Customer Profile (the specific type of person most likely to be your first customer)
- `memory/decisions-log.md` — a log of every change, with date and reason

**Modes:**
- **Initialize** — 5-question onboarding (~5 minutes). Ask once.
- **Update** — When your focus shifts, a new constraint appears, or you learn something about your customers.
- **Review** — Plain-language summary of where things stand.

---

### 2. `/BusinessAgents:discover` — Opportunity Discovery Agent

**Job:** Find real problems worth building a business around. Research market signals, rank opportunities, and recommend one to pursue.

**Reads:** `memory/startup-context.md`, `memory/icp.md`

**Asks:** 5 guided questions about personal frustrations, target audience, broken products, trends, and existing skills.

**Researches:** Forums, reviews, articles, and social signals to validate pain and timing.

**Outputs:**
- `outputs/opportunity-discovery-<topic>-<YYYY-MM-DD>.md` — full ranked report with evidence, Why Now analysis, and ICP recommendation.

**Hands off to:** `/BusinessAgents:validate` — run it with the top-ranked problem.

---

### 3. `/BusinessAgents:validate` — Validation Agent

**Job:** Kill bad ideas early. Design cheap, fast experiments to test whether a problem is real and whether people will pay for a solution.

**Reads:** `memory/startup-context.md`, `memory/icp.md` + optionally a discovery report

**Asks:** 6 questions: target person, current workarounds, existing conversations, willingness to pay, available budget/time, and success criteria.

**Produces:** A Go / No-go recommendation plus 3 concrete experiments (customer interviews, landing page test, surveys, cold outreach).

**Outputs:**
- `outputs/validation-<idea-name>-<YYYY-MM-DD>.md` — evidence audit, assumptions, 3 experiments with success/failure criteria, and Go/No-go verdict.

**Hands off to:** `/BusinessAgents:simulate_user` — run it for a first hypothesis simulation, then run `/BusinessAgents:interview`.

---

### 4. `/BusinessAgents:interview` — Customer Interview Agent

**Job:** Guide founders through the full interview lifecycle — generating a tailored script and tracking documents before calls, coaching live during calls, and synthesizing learnings into structured insights and ICP updates.

**Reads:** `memory/startup-context.md`, `memory/icp.md` + the validation report

**Three phases:**
- **Prepare** — generates a tailored interview script and an editable HTML interview sheet (fill in browser, export to CSV when done)
- **Coach** — live coaching during a call: founder describes what was said, agent responds with one follow-up question; saves a session log when the call ends
- **Synthesize** — after all interviews, audits assumptions (confirmed / busted / partial), surfaces new findings, proposes specific ICP updates for the founder to confirm

**Outputs:**
- `outputs/ideas/<slug>/interview-script-<YYYY-MM-DD>.md`
- `outputs/ideas/<slug>/interview-sheet-<YYYY-MM-DD>.html`
- `outputs/ideas/<slug>/interview-coaching-<YYYY-MM-DD>-<N>.md` (one per session)
- `outputs/ideas/<slug>/interview-insights-<YYYY-MM-DD>.md`

**Hands off to:** `/BusinessAgents:simulate_user` — run it again after interviews for a refined simulation.

---

### 5. `/BusinessAgents:simulate_user` — End User Simulator

**Job:** Show founders — and their potential customers — exactly how the solution changes a real person's daily work. Concrete, believable, shareable.

**Reads:** `memory/startup-context.md`, `memory/icp.md` + the most recent validation report (or discovery report as fallback).

**Simulates:** 2–3 real situations where the user encounters the problem. For each situation:
- **Before** table — 5-phase journey of how they handle it today
- **Task-level drill** — micro-steps in the most painful phase
- **After** table — the same journey with the solution
- **Benefit calculation** — time saved, error reduction, quality improvement, cognitive load (all labeled as estimates with reasoning shown)

**Outputs:**
- `outputs/simulation-<persona>-<YYYY-MM-DD>.md` — full simulation report
- `outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md` — plain-language version to share with real users

**Hands off to:** `/BusinessAgents:docs` — choose "User Impact Journey Map" to turn the simulation into a visual slide.

---

### 6. `/BusinessAgents:prospects` — Client Prospect Agent

**Job:** Find real potential clients — companies matching the ICP in the founder's target city — by scraping public business directories. Delivers a ready-to-use lead list with name, phone, email, address, employee count, and decision-maker name.

**Reads:** `memory/startup-context.md`, `memory/icp.md`

**Uses:** Scrapling MCP server (`scrapling mcp`) to fetch Yellow Pages, Yelp, and Google Maps pages

**Asks:** 4 questions — target city, industry focus (law firms / engineering / both), max company size, number of leads

**Enrichment (optional):** Visits each company's website to find email address, employee count, and decision-maker name

**Outputs:**
- `outputs/ideas/<slug>/prospects-<YYYY-MM-DD>.md` — formatted lead list
- `outputs/ideas/<slug>/prospects-<YYYY-MM-DD>.csv` — import-ready for any CRM or spreadsheet

**Hands off to:** `/BusinessAgents:interview` — use the prospect list to find people to contact

---

### 7. `/BusinessAgents:docs` — Business Documentation Agent


**Job:** Turn everything captured so far into polished business documents and presentations.

**Reads:** All memory files + all files in `outputs/` before generating anything.

**Documents it can generate:**
- Vision & mission statement
- Value proposition
- Business Model Canvas / Lean Canvas
- SWOT analysis
- Go-to-market strategy
- MVP feature specification
- Customer journey map
- Financial projections template
- Competitive landscape summary
- Market size breakdown (TAM/SAM/SOM)
- Investor one-pager
- Full business plan
- **User Impact Journey Map** — before/after visual slides built from a simulation report (requires `/BusinessAgents:simulate_user` first)

**Slides (HTML, open in any browser):**
- Pitch deck for investors
- Demo day presentation
- Co-founder recruitment deck
- Internal planning presentation

**Outputs:**
- `outputs/docs/<document-name>-<YYYY-MM-DD>.md` — documents
- `outputs/slides/<presentation-name>-<YYYY-MM-DD>.html` — slides (self-contained, no internet required)

Missing information is marked `[PLACEHOLDER: description]` — never invented.

---

## Intended Flow

```
1. /BusinessAgents:founder        →  Initialize memory (run once at the start)
         ↓
2. /BusinessAgents:discover       →  Find top 3 problems worth solving
         ↓
3. /BusinessAgents:simulate_user  →  1st run: hypothesis — what do we think changes for the user?
         ↓
4. /BusinessAgents:validate       →  Test the top problem. Get a Go/No-go verdict.
         ↓ (Go)
5. /BusinessAgents:prospects      →  Find real companies to contact (scraped lead list)
         ↓
6. /BusinessAgents:interview      →  Talk to real users. Refine the ICP.
         ↓
7. /BusinessAgents:simulate_user  →  2nd run: refined — what actually changes, based on real data
         ↓
8. /BusinessAgents:docs           →  Generate documents and pitch materials
```

**Optional helpers — run at any point:**
- `/BusinessAgents:brand` — build a complete brand identity: extracts colors and fonts from your existing website (if you have one), evaluates the current branding, makes suggestions, and generates SVG logo variants + a brand guidelines HTML document. Saves your colors to `memory/brand.md` so marketing and docs agents use them automatically.
- `/BusinessAgents:marketing` — create a LinkedIn carousel post from your idea. Use it whenever you want to build an audience, test messaging, or share your thinking publicly. It reads your memory and outputs automatically so you never need to re-explain your context. Run it once or many times — each carousel is saved separately.

You can re-run any agent at any point:
- Re-run `/BusinessAgents:founder` (Update mode) whenever your constraints or target customer changes.
- Re-run `/BusinessAgents:founder` → "New idea" to register a second product idea and explore it in parallel.
- Re-run `/BusinessAgents:discover` to explore a different problem space for any registered idea.
- Re-run `/BusinessAgents:validate` on a new problem after a No-go verdict.
- Re-run `/BusinessAgents:docs` to update documents as new information comes in.

**Working on multiple ideas:** Register each product idea separately with `/BusinessAgents:founder` → "New idea". Each downstream agent will show a numbered menu so you can pick which idea to work on for that session. All files stay scoped to their idea's folder in `outputs/ideas/`.

---

## Memory & Output Structure

```
memory/
  startup-context.md     ← company: vision, mission, constraints, priorities
  icp.md                 ← company-level ICP (broad market filter — who you serve across all products)
  decisions-log.md       ← company-level decisions only
  ideas.md               ← registry of all product ideas with status and stage dates
  brand.md               ← brand colors, typography, logo paths (written by /BusinessAgents:brand)

outputs/
  brand/                 ← company-level brand (applies to the whole business)
    logo-primary-*.svg       ← single-kit: all brand files directly here
    logo-icon-*.svg
    logo-wordmark-*.svg
    logo-mono-*.svg
    brand-guidelines-*.html
    ai-image-prompts-*.md
    original/            ← dual-kit only: exact current branding preserved for comparison
      logo-primary-*.svg
      logo-icon-*.svg
      logo-wordmark-*.svg
      logo-mono-*.svg
      brand-guidelines-*.html
      ai-image-prompts-*.md
    recommended/         ← dual-kit only: improved version (active brand)
      logo-primary-*.svg
      logo-icon-*.svg
      logo-wordmark-*.svg
      logo-mono-*.svg
      brand-guidelines-*.html
      ai-image-prompts-*.md
  ideas/
    <slug>/              ← one folder per product idea (slug = short lowercase name)
      icp.md                              ← detailed ICP for THIS product (job title, company size, decision authority, etc.)
      decisions-log.md                    ← decisions specific to this product idea
      opportunity-discovery-*.md          ← discovery report
      validation-*.md                     ← validation plan with Go/No-go verdict
      interview-script-*.md               ← tailored interview question guide
      interview-sheet-*.html              ← editable interview sheet (fill in browser, export to CSV)
      interview-coaching-*-*.md           ← per-session coaching log
      interview-insights-*.md             ← synthesis: assumptions audit + ICP updates
      prospects-*.md                      ← scraped lead list (formatted)
      prospects-*.csv                     ← scraped lead list (CRM import)
      simulation-<persona>-*.md           ← end user simulation report
      simulation-<persona>-onepager-*.md  ← plain-language user-facing summary
      brand/                   ← idea/product-specific sub-brand (optional, same structure as outputs/brand/)
        logo-primary-*.svg
        ...
        original/        ← dual-kit only
        recommended/     ← dual-kit only
      marketing/
        carousel-*.html  ← LinkedIn carousel (browser preview + PDF export for upload)
      docs/
        *.md             ← business documents
        *.html           ← user impact journey map slides
      slides/
        *.html           ← pitch decks and presentations
```

---

## Key Rules Across All Agents

- `/BusinessAgents:founder` must run first — all other agents stop and redirect if memory is uninitialized.
- Each agent reads memory and prior outputs before asking questions — you never explain your context twice.
- Register every new product idea with `/BusinessAgents:founder` → "New idea" before running any downstream agent — all agents require an entry in `memory/ideas.md`.
- Each downstream agent asks "which idea?" at startup and scopes all file reads and writes to `outputs/ideas/<slug>/` — files from different ideas are never mixed.
- All agents ask one question at a time and explain business terms before using them.
- All reports are saved to `outputs/` — never skipped.
- A No-go verdict from the Validation Agent is a success, not a failure — it saves months of building the wrong thing.
