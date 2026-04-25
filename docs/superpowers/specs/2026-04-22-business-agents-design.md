# Business Agents — Design Spec
**Date:** 2026-04-22
**Status:** Approved

---

## Core Principle

Agents are organized around decisions a founder must make, not business departments. Every agent is fully guided — it asks you all the questions it needs, explains every concept it uses, and assumes no prior business knowledge.

---

## Agent Lineup

| Slash Command | Role |
|---|---|
| `/BusinessAgents:founder` | Startup memory manager + context keeper |
| `/BusinessAgents:discover` | Opportunity research + problem ranking |
| `/BusinessAgents:validate` | Idea validation + go/no-go recommendation |
| `/BusinessAgents:simulate_user` | End user workflow simulation + benefit quantification |
| `/BusinessAgents:docs` | Business document + slide generation |

---

## Project Structure

```
BusinessAgents/
├── .claude/
│   └── skills/
│       └── BusinessAgents/
│           ├── founder.md         # /BusinessAgents:founder
│           ├── discover.md        # /BusinessAgents:discover
│           ├── validate.md        # /BusinessAgents:validate
│           └── docs.md            # /BusinessAgents:docs
├── memory/
│   ├── startup-context.md         # vision, mission, constraints, priorities
│   ├── icp.md                     # ideal customer profile
│   └── decisions-log.md           # past decisions with date and reasoning
├── outputs/
│   ├── opportunity-discovery-<topic>-<date>.md
│   ├── validation-<idea-name>-<date>.md
│   ├── docs/
│   │   └── <document-name>-<date>.md
│   └── slides/
│       └── <presentation-name>-<date>.html
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-04-22-business-agents-design.md
```

---

## Memory & Data Flow

```
/BusinessAgents:founder
  writes → memory/startup-context.md
           memory/icp.md
           memory/decisions-log.md

/BusinessAgents:discover
  reads  → memory/startup-context.md
  writes → outputs/opportunity-discovery-<topic>-<date>.md

/BusinessAgents:validate
  reads  → memory/startup-context.md
           outputs/opportunity-discovery-*.md (user references a specific file)
  writes → outputs/validation-<idea-name>-<date>.md

/BusinessAgents:simulate_user
  reads  → memory/startup-context.md
           memory/icp.md
           outputs/validation-*.md (most recent by date — priority)
           outputs/opportunity-discovery-*.md (fallback if no validation report)
  writes → outputs/simulation-<persona>-<YYYY-MM-DD>.md
           outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md

/BusinessAgents:docs
  reads  → memory/ (all files)
           outputs/ (all reports)
  writes → outputs/docs/<document-name>-<date>.md
           outputs/slides/<presentation-name>-<date>.html
```

**Key rule:** Only `/BusinessAgents:founder` writes to `memory/`. All other agents write to `outputs/`. The user decides (via the Founder Agent) whether findings from outputs should be promoted into core memory. This keeps the source of truth clean and under the founder's control.

---

## Output Format (All Agents)

Every agent produces two things:

1. **Chat summary** — concise, in the Claude Code conversation. Key findings, top recommendations, and a clear next step.
2. **Full report file** — saved to `outputs/` with a descriptive filename. Contains all analysis, reasoning, raw data, and next steps.

---

## Agent 1: Founder Agent (`/BusinessAgents:founder`)

### Purpose
The startup's memory manager. Maintains the single source of truth about your company. Acts as your "executive brain" — not a researcher or advisor, just the keeper of what you've decided.

### Modes
The agent asks which mode you want at invocation:
- **Initialize** — first-time setup, walks through all memory files from scratch
- **Update** — change a specific piece of context (vision shifted, new constraint, ICP revised)
- **Review** — summarize current state of all memory files in plain language

### Guided Questions (Initialize mode)
The agent asks one question at a time, explains why it's asking:
- What problem are you trying to solve in the world? (Don't worry about getting it perfect)
- Who do you imagine using your solution? Describe them like a person.
- What resources do you have? (Time per week, budget, technical skills)
- Are there any industries or types of work you want to avoid?
- What does success look like for you personally in 1 year?

### Memory Files Updated
- `memory/startup-context.md` — vision, mission, constraints, priorities
- `memory/icp.md` — ideal customer profile
- `memory/decisions-log.md` — every update logged in the format: `[YYYY-MM-DD] What changed: <summary>. Why: <reason>.`

### What It Does NOT Do
Research, validation, document generation. It only reads and writes memory.

---

## Agent 2: Opportunity Discovery Agent (`/BusinessAgents:discover`)

### Purpose
Find viable problems worth solving. Prevents building products nobody wants. Produces a ranked list of opportunities with supporting market evidence.

### Guided Questions
The agent asks one question at a time, always explaining what it's asking and why:
- What problems have you personally experienced that frustrated you?
- What industry or type of person do you want to help? (No wrong answer)
- Have you noticed any tools, services, or products that feel broken, overpriced, or hard to use?
- Are there any trends or news topics you've been following lately?
- Is there anything you're already good at that could be useful to others?

The agent also reads `memory/startup-context.md` automatically to apply your existing constraints and focus.

### Data Sources
- Web search (Claude Code built-in) for market signals, trend analysis, competitor research
- User-pasted content (articles, notes, links) for additional context

### Outputs

**Chat summary:**
- Top 3 ranked problems with a one-line "Why now?" for each
- Recommended ICP for the top problem
- Suggested next step

**Full report** (`outputs/opportunity-discovery-<topic>-<date>.md`):
- Full ranked problem list with evidence for each
- Market trend analysis and signals
- "Why now?" rationale per problem
- ICP breakdown: who they are, what the pain is, how they currently solve it
- Recommended problem to validate first and why

---

## Agent 3: Validation Agent (`/BusinessAgents:validate`)

### Purpose
Kill bad ideas early before spending money or months building. Designs cheap experiments to test whether a problem is real and whether people will pay for a solution.

### Guided Questions
The agent asks one question at a time, explaining every concept it uses:
- Which idea or problem do you want to test? (Paste or describe it)
- Who exactly would use this? Describe them like a real person, not a category.
- How do people solve this problem today, even if it's a bad solution?
- Have you spoken to anyone who has this problem? What did they say?
- What would success look like in the next 30 days if you ran a small test?
- How much time and money can you spend on this experiment?

It reads `memory/startup-context.md` automatically. If a discovery report exists, the agent asks: "Do you have a discovery report to reference? If so, paste its filename or paste the relevant section." The user can paste the full path (e.g., `outputs/opportunity-discovery-saas-tools-2026-04-22.md`) or paste excerpt content directly into chat.

### Outputs

**Chat summary:**
- Go / No-go recommendation with one-line reasoning
- The single most important experiment to run next

**Full report** (`outputs/validation-<idea-name>-<date>.md`):
- Evidence summary: what you know vs. what you're assuming
- Designed experiments (landing page test, customer interview script, survey, cold outreach)
- Success and failure criteria for each experiment
- Go / No-go verdict with full reasoning
- Next steps if Go; lessons to carry forward if No-go

---

## Agent 4: Business Documentation Agent (`/BusinessAgents:docs`)

### Purpose
Generate formal business documents and presentations from everything captured in memory and output files. Produces polished, professional content without requiring business writing skills.

### Modes
The agent asks which type of output you want:

**Documents** (saved to `outputs/docs/`):
- Vision & mission statement
- Value proposition
- Business Model Canvas
- Lean Canvas
- SWOT analysis
- Go-to-market strategy outline
- MVP feature specification
- Customer journey map
- Financial projections template
- Competitive landscape summary
- TAM/SAM/SOM market size breakdown
- Investor one-pager
- Full business plan

**Slides** (saved to `outputs/slides/` as self-contained HTML):
- Pitch deck (investor)
- Demo day presentation
- Co-founder recruitment deck
- Internal planning presentation

### Slide Generation Flow
Before generating any slides, the agent asks:
1. Who is the audience? (investors, potential co-founder, demo day judges, internal)
2. What is the goal? (raise money, recruit, sell, plan)
3. What sections should be included?
4. What tone? (formal, conversational, bold)

Slides are fully self-contained HTML files — no dependencies, open in any browser, version-controlled in git.

### Data Sources
Reads all files in `memory/` and all files in `outputs/`. For early runs with limited data, generates drafts with clearly marked placeholders and flags what information is still needed.

### Outputs
- `outputs/docs/<document-name>-<date>.md` for written documents
- `outputs/slides/<presentation-name>-<date>.html` for slide decks

---

## Interaction Principles (All Agents)

1. **One question at a time** — never overwhelm with a form or list of questions
2. **Always explain why** — before asking a question, briefly explain what it's for
3. **Plain language in, business language out** — accept casual descriptions, produce professional output
4. **No assumed knowledge** — every business term is explained when first used
5. **Guided, not assumed** — the agent always asks for what it needs rather than expecting the user to know what to provide

---

## Recommended First-Use Flow

1. Run `/BusinessAgents:founder` in **Initialize** mode — sets up all memory files
2. Run `/BusinessAgents:discover` — research problems in your chosen space
3. Run `/BusinessAgents:simulate_user` (optional early run) — simulate the end user's workflow before validating to sharpen your understanding of the benefit
4. Run `/BusinessAgents:validate` — test the most promising problem from step 2
5. Run `/BusinessAgents:simulate_user` (post-validation run) — now with more evidence, produce the shareable user one-pager
6. Run `/BusinessAgents:docs` — generate a business plan, pitch deck, or User Impact Journey Map slide
7. Return to `/BusinessAgents:founder` **Update** mode whenever your thinking evolves

Steps 2–4 can be repeated as many times as needed. The system has no "done" state — it supports ongoing iteration.

---

## Non-Goals (Out of Scope)

- No automation between agents — you manually chain workflows
- No external integrations (CRM, email, analytics) in v1
- No multi-user support — single founder use only
- No persistent vector database — all memory is structured Markdown/JSON files
