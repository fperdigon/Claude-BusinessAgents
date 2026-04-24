# BussinesAgents — System Overview

A system of five AI agents that guide a founder from raw idea to validated business with professional documentation. Each agent has a focused job. They share memory files and pass outputs to each other so you never repeat yourself.

---

## Agents

### 1. `/BussinesAgents:founder` — Startup Memory Manager

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

### 2. `/BussinesAgents:discover` — Opportunity Discovery Agent

**Job:** Find real problems worth building a business around. Research market signals, rank opportunities, and recommend one to pursue.

**Reads:** `memory/startup-context.md`, `memory/icp.md`

**Asks:** 5 guided questions about personal frustrations, target audience, broken products, trends, and existing skills.

**Researches:** Forums, reviews, articles, and social signals to validate pain and timing.

**Outputs:**
- `outputs/opportunity-discovery-<topic>-<YYYY-MM-DD>.md` — full ranked report with evidence, Why Now analysis, and ICP recommendation.

**Hands off to:** `/BussinesAgents:validate` — run it with the top-ranked problem.

---

### 3. `/BussinesAgents:validate` — Validation Agent

**Job:** Kill bad ideas early. Design cheap, fast experiments to test whether a problem is real and whether people will pay for a solution.

**Reads:** `memory/startup-context.md`, `memory/icp.md` + optionally a discovery report

**Asks:** 6 questions: target person, current workarounds, existing conversations, willingness to pay, available budget/time, and success criteria.

**Produces:** A Go / No-go recommendation plus 3 concrete experiments (customer interviews, landing page test, surveys, cold outreach).

**Outputs:**
- `outputs/validation-<idea-name>-<YYYY-MM-DD>.md` — evidence audit, assumptions, 3 experiments with success/failure criteria, and Go/No-go verdict.

**Hands off to:** `/BussinesAgents:simulate_user` — run it after a Go verdict.

---

### 4. `/BussinesAgents:simulate_user` — End User Simulator

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

**Hands off to:** `/BussinesAgents:docs` — choose "User Impact Journey Map" to turn the simulation into a visual slide.

---

### 5. `/BussinesAgents:docs` — Business Documentation Agent

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
- **User Impact Journey Map** — before/after visual slides built from a simulation report (requires `/BussinesAgents:simulate_user` first)

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
1. /BussinesAgents:founder   →  Initialize memory (run once at the start)
         ↓
2. /BussinesAgents:discover  →  Find top 3 problems worth solving
         ↓
3. /BussinesAgents:validate  →  Test the top problem. Get a Go/No-go verdict.
         ↓ (Go)
4. /BussinesAgents:simulate_user  →  Show how the solution changes the user's day
         ↓
5. /BussinesAgents:docs      →  Generate documents and pitch materials
```

You can re-run any agent at any point:
- Re-run `/BussinesAgents:founder` (Update mode) whenever your constraints or target customer changes.
- Re-run `/BussinesAgents:founder` → "New idea" to register a second product idea and explore it in parallel.
- Re-run `/BussinesAgents:discover` to explore a different problem space for any registered idea.
- Re-run `/BussinesAgents:validate` on a new problem after a No-go verdict.
- Re-run `/BussinesAgents:docs` to update documents as new information comes in.

**Working on multiple ideas:** Register each product idea separately with `/BussinesAgents:founder` → "New idea". Each downstream agent will show a numbered menu so you can pick which idea to work on for that session. All files stay scoped to their idea's folder in `outputs/ideas/`.

---

## Memory & Output Structure

```
memory/
  startup-context.md     ← vision, mission, constraints, priorities
  icp.md                 ← ideal customer profile
  decisions-log.md       ← log of every memory change
  ideas.md               ← registry of all product ideas with status and stage dates

outputs/
  ideas/
    <slug>/              ← one folder per product idea (slug = short lowercase name)
      opportunity-discovery-*.md          ← discovery report
      validation-*.md                     ← validation plan with Go/No-go verdict
      simulation-<persona>-*.md           ← end user simulation report
      simulation-<persona>-onepager-*.md  ← plain-language user-facing summary
      docs/
        *.md             ← business documents
        *.html           ← user impact journey map slides
      slides/
        *.html           ← pitch decks and presentations
```

---

## Key Rules Across All Agents

- `/BussinesAgents:founder` must run first — all other agents stop and redirect if memory is uninitialized.
- Each agent reads memory and prior outputs before asking questions — you never explain your context twice.
- Register every new product idea with `/BussinesAgents:founder` → "New idea" before running any downstream agent — all agents require an entry in `memory/ideas.md`.
- Each downstream agent asks "which idea?" at startup and scopes all file reads and writes to `outputs/ideas/<slug>/` — files from different ideas are never mixed.
- All agents ask one question at a time and explain business terms before using them.
- All reports are saved to `outputs/` — never skipped.
- A No-go verdict from the Validation Agent is a success, not a failure — it saves months of building the wrong thing.
