# BusinessAgents

Five AI agents that guide a founder from raw idea to validated business — with professional documents and pitch materials at the end.

Each agent has one focused job. They share memory files and pass outputs to each other, so you never explain your context twice.

---

## What it does

| Step | Agent | What you get |
|------|-------|-------------|
| 1 | `/BusinessAgents:founder` | Your startup context saved to memory — vision, constraints, ideal customer |
| 2 | `/BusinessAgents:discover` | Top 3 problems worth solving, ranked by evidence and market timing |
| 3 | `/BusinessAgents:simulate_user` | 1st simulation: hypothesis of what changes for your user, based on discovery |
| 4 | `/BusinessAgents:validate` | Go / No-go verdict + 3 cheap experiments to test before building anything |
| 5 | `/BusinessAgents:interview` | Interview script, tracker CSV, printable sheet + live coaching + insight synthesis |
| 6 | `/BusinessAgents:simulate_user` | 2nd simulation: refined — grounded in what real users told you |
| 7 | `/BusinessAgents:docs` | Business plan, pitch deck, value proposition, canvas, and more |

---

## Requirements

- [Claude Code](https://claude.ai/code) (the CLI or desktop app)

No other dependencies. No API keys to configure. No Python environment to set up.

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
/BusinessAgents:interview      →  Prepare → Coach → Synthesize
         ↓
/BusinessAgents:simulate_user  →  2nd run: refined simulation
         ↓
/BusinessAgents:docs           →  Generate documents and pitch materials
```

You can re-run any agent at any point — if your target customer changes, re-run `founder` in Update mode. If you get a No-go verdict, re-run `validate` on a new problem. If you want to explore a second product, use `founder` → "New idea".

---

## Agents

### `/BusinessAgents:founder` — Startup Memory Manager

Runs a short onboarding to capture your vision, constraints, and ideal customer. Stores everything in `memory/` so downstream agents never ask you to repeat yourself.

**Modes:** Initialize · Update · Review · New idea · List ideas · Archive idea

---

### `/BusinessAgents:discover` — Opportunity Discovery Agent

Asks 5 guided questions, then searches forums, reviews, and social signals to find real problems with real demand. Produces a ranked report with evidence and a "Why Now" analysis for each opportunity.

**Output:** `outputs/ideas/<slug>/opportunity-discovery-<date>.md`

---

### `/BusinessAgents:validate` — Validation Agent

Designs 3 cheap, fast experiments to test whether a problem is real and whether people will pay. Gives a clear Go / No-go verdict. A No-go is a good outcome — it saves months of building the wrong thing.

**Output:** `outputs/ideas/<slug>/validation-<date>.md`

---

### `/BusinessAgents:interview` — Customer Interview Agent

Guides founders through the full interview lifecycle. Generates a tailored question script, a CSV tracker to fill in across interviewees, and a printable HTML sheet for use on calls. Provides live coaching during calls — describe what the interviewee said, get one follow-up question back. After all calls, synthesizes findings: which assumptions held, which broke, what was unexpected. Proposes specific ICP updates for the founder to confirm before writing anything.

**Outputs:**
- `outputs/ideas/<slug>/interview-script-<date>.md` — full interview guide
- `outputs/ideas/<slug>/interview-tracker-<date>.csv` — open in Excel/Google Sheets
- `outputs/ideas/<slug>/interview-sheet-<date>.html` — open in browser to print
- `outputs/ideas/<slug>/interview-coaching-<date>-<N>.md` — per-session log
- `outputs/ideas/<slug>/interview-insights-<date>.md` — synthesis report

---

### `/BusinessAgents:simulate_user` — End User Simulator

Simulates 2–3 real situations where your target user runs into the problem. For each one: a before/after workflow table, task-level drill-down, and benefit calculations (time saved, error reduction, cognitive load). All estimates are labeled as estimates with reasoning shown.

**Outputs:**
- `outputs/ideas/<slug>/simulation-<persona>-<date>.md` — full report
- `outputs/ideas/<slug>/simulation-<persona>-onepager-<date>.md` — plain-language version to share with real users

---

### `/BusinessAgents:docs` — Business Documentation Agent

Generates polished business documents from everything captured so far. Choose from a menu. Missing information is marked `[PLACEHOLDER]` — never invented.

**Documents:** Vision & mission · Value proposition · Business Model Canvas · SWOT · Go-to-market strategy · MVP spec · Customer journey map · Financial projections · Competitive landscape · TAM/SAM/SOM · Investor one-pager · Full business plan · User Impact Journey Map

**Slides (self-contained HTML):** Pitch deck · Demo day · Co-founder recruitment · Internal planning

**Outputs:** `outputs/ideas/<slug>/docs/` and `outputs/ideas/<slug>/slides/`

---

## File structure

```
memory/                        ← your private startup context (gitignored)
  startup-context.md
  icp.md
  decisions-log.md
  ideas.md

outputs/ideas/<slug>/          ← your private research and reports (gitignored)
  opportunity-discovery-*.md
  validation-*.md
  simulation-<persona>-*.md
  simulation-<persona>-onepager-*.md
  docs/
  slides/

.claude/skills/BusinessAgents/ ← the agent prompts (shared, version-controlled)
.claude/commands/BusinessAgents/ ← slash command stubs
```

---

## Privacy

`memory/` and `outputs/ideas/` are gitignored. Your startup context, customer profile, research reports, and simulation outputs stay local — they are never committed to the repository.

If you fork or share this repo, only the agent skill files and project structure are included. Your data stays yours.

---

## Multiple ideas

Register each product idea separately:

```
/BusinessAgents:founder  →  choose "New idea"
```

Each downstream agent will show a numbered menu so you can pick which idea to work on. All files are scoped to `outputs/ideas/<slug>/` — ideas never mix.

---

## Built with

- [Claude Code](https://claude.ai/code) — the AI coding assistant from Anthropic
- [Superpowers plugin](https://github.com/untangled-ai/untangled-superpowers) — skill-based agent framework (optional, used during development)
