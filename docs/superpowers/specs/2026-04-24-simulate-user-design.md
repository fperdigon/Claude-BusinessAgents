# End User Simulator Agent — Design Spec
**Date:** 2026-04-24
**Status:** Approved

---

## Purpose

The End User Simulator helps founders show end users the concrete benefits of their solution by simulating how it changes real situations in their daily work. It answers: "What does this actually change for me?" — in terms the end user can feel (time, errors, quality, mental effort).

---

## Slash Command

`/BusinessAgents:simulate_user`

---

## Position in Workflow

```
founder → discover → [simulate_user] → validate → [simulate_user again] → docs
```

Can run after `/discover` (early, exploratory) or after `/validate` (refined, more detailed). Running it twice — once before and once after validation — produces increasingly credible output as more evidence accumulates. The `/docs` agent later renders the journey map slide from this agent's output.

---

## Data Flow

```
/BusinessAgents:simulate_user
  reads  → memory/startup-context.md
           memory/icp.md
           outputs/validation-*.md (most recent by date, if exists — takes priority)
           outputs/opportunity-discovery-*.md (most recent by date, used as fallback if no validation report)
  writes → outputs/simulation-<persona>-<YYYY-MM-DD>.md
           outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md
```

---

## Agent Flow

The agent always runs these steps in order:

### Step 1 — Load context silently
Read `memory/icp.md`, `memory/startup-context.md`, and the most recent discovery and validation reports in `outputs/` (if they exist). If `startup-context.md` is uninitialized, stop and redirect: "Please run `/BusinessAgents:founder` first."

### Step 2 — Confirm persona (Question 1)
Present the loaded ICP to the founder:
> "Here's who I'm going to simulate based on your saved profile: [ICP summary]. Does this describe your target user well, or would you like to adjust anything — their role, industry, or daily context?"

Wait for confirmation or adjustments before proceeding.

### Step 3 — Confirm solution (Question 2)
Present the solution description extracted from the most recent output file:
> "Here's how I'm describing your solution: [solution summary]. Is this still accurate? Adjust anything that's changed."

If no output files exist, ask:
> "Describe your solution in plain terms — what does it do and who does it help?"

### Step 4 — Choose situations (Question 3)
Ask the founder to name 2–3 real situations where the end user encounters the problem:
> "What are 2–3 real situations where your target user runs into this problem? For example: 'when onboarding a new client' or 'when preparing for a deadline.' I can suggest situations if you're not sure — just say 'suggest.'"

If the founder asks for suggestions, use web search to find common workflow pain points for this role/industry, then present 3–4 options.

### Step 5 — Simulate each situation
For each situation, run the following sub-steps:

#### 5a — Web search (if needed)
Before asking the founder anything, search for how this role/industry handles this situation today. Use the findings to fill the workflow phases. Tell the founder: "I found some context about how [role] typically handles [situation] — I'll use that as the baseline."

#### 5b — Before simulation (journey-level)
Generate the 5-phase "before" workflow showing how the end user currently handles this situation without the solution:

| Phase | What happens |
|-------|-------------|
| **Trigger** | What kicks off this situation |
| **Gather** | What information/materials they need to collect |
| **Execute** | The core work they do |
| **Review** | How they check their work |
| **Hand off** | What they deliver and to whom |

#### 5c — Task-level drill
Identify the 1–2 most time-consuming or error-prone phases from 5b. Break those phases into specific micro-tasks (e.g., "opens spreadsheet → copies data from email → pastes into tracker → reformats manually → cross-checks against original").

#### 5d — After simulation
Rerun the same 5 phases with the solution integrated. Show what specifically changes at each step. For the drilled phases, show the task-level comparison.

#### 5e — Benefit calculation
Calculate 4 metrics for this situation. Label estimates clearly as estimates:

- **⏱ Time saved** — estimated hours per instance or per week (show the math: e.g., "phase X currently takes 45 min, with the solution it takes 5 min → 40 min saved per instance")
- **✗ Error/rework reduction** — estimated % fewer mistakes or rework cycles, with reasoning
- **★ Quality improvement** — qualitative: what gets better (more thorough, more consistent, better documented)
- **🧠 Cognitive load reduction** — qualitative: what mental effort or stress is eliminated

#### 5f — Per-situation clarifying question (if needed)
If web search didn't cover the workflow sufficiently, ask one targeted question:
> "Can you walk me through how [persona] currently handles [situation]? Even a rough description helps."

### Step 6 — Cross-situation rollup
After all situations are simulated, summarize:
- Total estimated time saved per week (sum across situations, adjusted for frequency)
- Top 3 benefit messages across all situations
- "Key talking points" — 3–5 sentences the founder can use verbatim in conversations with end users

### Step 7 — Generate outputs
Produce both output files (see Outputs section below).

---

## Guided Questions Summary

At most 4 questions per run (plus up to 1 per situation if web search doesn't cover it):

1. "Does this describe your target user well?" — persona confirmation
2. "Is this still an accurate description of your solution?" — solution confirmation
3. "What are 2–3 real situations where your target user runs into this problem?" — situation selection
4. *(Per situation, only if needed)* "Can you walk me through how [persona] currently handles [situation]?"

---

## Outputs

### Full Report
**Path:** `outputs/simulation-<persona>-<YYYY-MM-DD>.md`

**Structure:**
```markdown
# End User Simulation: [Persona Name/Role]
Date: YYYY-MM-DD

## Persona Profile
[Refined ICP for this run — role, industry, daily context]

## Solution Summary
[What the solution does, in plain language]

## Situation 1: [Situation Name]

### Before (current workflow)
[Journey-level phases table]

#### Task-level detail: [Most painful phase]
[Step-by-step micro-tasks]

### After (with solution)
[Journey-level phases table showing changes]

#### Task-level detail: [Same phase with solution]
[Step-by-step micro-tasks showing what's eliminated or transformed]

### Benefits
- ⏱ Time saved: [estimate with reasoning]
- ✗ Error/rework reduction: [estimate with reasoning]
- ★ Quality improvement: [qualitative description]
- 🧠 Cognitive load: [qualitative description]

---

## Situation 2: [Situation Name]
[Same structure]

---

## Situation 3: [Situation Name]
[Same structure]

---

## Cross-Situation Summary

### Total estimated time saved per week
[Calculation across all situations, adjusted for frequency]

### Top 3 benefit messages
1. [Benefit message 1]
2. [Benefit message 2]
3. [Benefit message 3]

### Key talking points for end user conversations
- [Sentence 1]
- [Sentence 2]
- [Sentence 3]
- [Sentence 4]
- [Sentence 5]
```

### User-Facing One-Pager
**Path:** `outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md`

Plain language, no jargon. Framed as "here's what this could change for you."

**Structure:**
```markdown
# What [Solution Name] Could Change for [Role]

[One sentence: who this is for and what problem it addresses]

## [Situation 1 Name]
- [Benefit bullet 1 — plain language]
- [Benefit bullet 2 — plain language]
- [Benefit bullet 3 — plain language]

## [Situation 2 Name]
- [Benefit bullet 1]
- [Benefit bullet 2]
- [Benefit bullet 3]

## [Situation 3 Name]
- [Benefit bullet 1]
- [Benefit bullet 2]
- [Benefit bullet 3]

---

[Closing line with call to action — e.g., "Want to see this in action? Let's talk."]
```

---

## Docs Agent Addition

When `/BusinessAgents:docs` is run, a new document type is available:

**"User Impact Journey Map"** — an HTML slide showing the before/after workflow for each simulated situation. Uses the same visual style as existing slides (dark navy background, white text, blue accent). Reads from the most recent simulation report in `outputs/`.

Add to the `/BusinessAgents:docs` menu:
> - User impact journey map — a before/after visual of how your solution changes the end user's workflow (requires a simulation report from `/BusinessAgents:simulate_user`)

---

## Hard Rules

- Always read `memory/icp.md` and `memory/startup-context.md` at the start — stop and redirect to `/BusinessAgents:founder` if uninitialized
- Use web search before asking the founder about workflow details — never make the founder do research the agent can do
- Always tell the founder which situation is being simulated before generating it
- Never invent benefit numbers without a source or clear estimate basis — label all estimates as estimates with the reasoning shown
- Always produce both output files — never skip the one-pager
- Explain each metric the first time it appears: ⏱ time saved, ✗ error/rework reduction, ★ quality improvement, 🧠 cognitive load reduction
- Ask one question at a time
- A No-data situation (no outputs, no founder knowledge, no web results) should be flagged explicitly: "I couldn't find reliable information about how [role] handles [situation] — I'll mark this section as needing your input."
- Show the chat summary before mentioning the saved files

---

## Chat Summary Format

Always show this at the end of the run:

```
## End User Simulation Summary: [Persona]

**Situations simulated:** [list]

**Estimated time saved per week:** [X hours]

**Top 3 benefits:**
1. [Benefit]
2. [Benefit]
3. [Benefit]

**Key talking point:**
"[One sentence the founder can use verbatim]"

Full report saved to: outputs/simulation-<persona>-<YYYY-MM-DD>.md
One-pager saved to: outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md
```

---

## Non-Goals (Out of Scope for v1)

- No multi-persona simulation in a single run (one persona per run)
- No automated chaining with other agents — founder manually decides when to run this
- No real user data or interviews — simulation is based on web research + founder input only
- No quantitative ROI or revenue projections — that belongs in `/BusinessAgents:docs`
