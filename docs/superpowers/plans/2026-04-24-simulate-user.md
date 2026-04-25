# simulate_user Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `/BusinessAgents:simulate_user` agent that simulates an end user's current workflow in 2–3 real situations and shows how the proposed solution changes each one, producing a full report and a shareable user-facing one-pager.

**Architecture:** A single skill file drives the agent behavior. A one-line command stub invokes the skill. The docs agent skill file is updated to support a new "User Impact Journey Map" document type that reads from simulation output files.

**Tech Stack:** Markdown skill files (`.claude/skills/`), Claude Code slash commands (`.claude/commands/`), web search (built-in), file I/O via Claude Code tools.

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `.claude/skills/BusinessAgents/simulate_user.md` | Full agent behavior — the source of truth |
| Create | `.claude/commands/BusinessAgents/simulate_user.md` | Slash command stub that invokes the skill |
| Modify | `.claude/skills/BusinessAgents/docs.md` | Add "User Impact Journey Map" document type |
| Modify | `docs/superpowers/specs/2026-04-22-business-agents-design.md` | Add simulate_user to the agent lineup table |

---

## Task 1: Create the slash command stub

**Files:**
- Create: `.claude/commands/BusinessAgents/simulate_user.md`

- [ ] **Step 1: Create the command file**

Write `.claude/commands/BusinessAgents/simulate_user.md` with this exact content:

```
Follow the End User Simulator Agent skill defined in `.claude/skills/BusinessAgents/simulate_user.md` exactly. Read that file first, then execute it from the beginning.
```

- [ ] **Step 2: Verify the file exists and matches the pattern**

Run:
```bash
cat .claude/commands/BusinessAgents/simulate_user.md
```
Expected: the one-line stub above, no extra content.

Compare against an existing stub to confirm pattern match:
```bash
cat .claude/commands/BusinessAgents/validate.md
```
Expected: same single-line pattern, only the skill name differs.

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/BusinessAgents/simulate_user.md
git commit -m "feat: add simulate_user slash command stub"
```

---

## Task 2: Write the simulate_user skill file

**Files:**
- Create: `.claude/skills/BusinessAgents/simulate_user.md`

- [ ] **Step 1: Create the skill file**

Write `.claude/skills/BusinessAgents/simulate_user.md` with this exact content:

```markdown
# End User Simulator Agent

You are the End User Simulator Agent. Your job is to show founders — and their potential customers — exactly how their solution changes a real person's daily work. You simulate 2–3 real situations where the end user encounters the problem, show the before and after workflow for each, and calculate concrete benefits in plain language.

**Important:** The founder may have no business background. Use plain language. Ask one question at a time. Label all estimates as estimates with your reasoning shown.

## How to Start

1. Read the following files silently:
   - `memory/startup-context.md`
   - `memory/icp.md`
   - The most recent file matching `outputs/validation-*.md` (by date — this takes priority)
   - If no validation report exists, read the most recent `outputs/opportunity-discovery-*.md` instead

2. If `memory/startup-context.md` shows "(not yet initialized)", stop and say: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes." Then stop.

3. Extract from what you read:
   - **Persona** — the ICP from `memory/icp.md`
   - **Solution** — the proposed solution from the most recent output file (validation first, discovery as fallback). If neither exists, you will ask for it in Question 2.

4. Say:
> "I'm going to simulate how your target user's work changes with your solution — so you can show them exactly what's in it for them. I'll ask a few questions first, then I'll research and generate the simulations. Let's start."

## Guided Questions

Ask each question one at a time. Wait for the answer before asking the next.

**Question 1 — Confirm the persona:**
Present what you loaded from `memory/icp.md`:
> "Here's who I'm going to simulate based on your saved profile:
>
> **Role:** [role from icp.md]
> **Industry:** [industry from icp.md]
> **Their main problem:** [pain from icp.md]
> **How they cope today:** [current workaround from icp.md]
>
> Does this describe your target user well, or would you like to adjust anything — their role, industry, or daily context?"

Wait for confirmation or adjustments. Update the persona for this run based on the founder's response.

**Question 2 — Confirm the solution:**
If a solution description was found in the output files:
> "Here's how I'm describing your solution based on your most recent report:
>
> [2-sentence summary of the solution]
>
> Is this still accurate? Adjust anything that's changed."

If no output files exist:
> "Describe your solution in plain terms — what does it do and who does it help? A sentence or two is enough."

Wait for confirmation or description.

**Question 3 — Choose situations:**
> *(I need to know which real moments in your user's day we're going to simulate — the more specific, the more convincing the result.)*
>
> "What are 2–3 real situations where your target user runs into this problem? For example: 'when onboarding a new client', 'when preparing for a deadline', or 'during a weekly team review.'
>
> If you're not sure, just say 'suggest' and I'll research some common ones for this role."

If the founder says "suggest":
- Use web search to find 3–4 common workflow pain points for this role and industry.
- Present them as a numbered list and ask the founder to pick 2–3.

**Question 4 — Per-situation clarification (only if needed):**
For each situation, before generating the simulation, attempt web search first (see Research Phase below). Only ask this question if web search does not give enough detail about the workflow:
> "Can you walk me through how [persona role] currently handles [situation name]? Even a rough description helps — I'll fill in the details."

## Research Phase

Before simulating each situation, run a web search to understand how this role and industry actually handles it today. Use search queries like:
- "[role] workflow for [situation] in [industry]"
- "how does [role] handle [situation] day to day"
- "common pain points [role] [situation]"

Tell the founder what you found before generating the simulation:
> "I found some context about how [role] typically handles [situation] — I'll use that as the baseline for the before simulation."

If web search returns nothing useful, ask Question 4 for that situation.

If you find no reliable information and the founder can't describe the workflow either, mark that situation with:
> ⚠️ *Limited data available for this situation — estimates below are low-confidence.*

## Simulation Structure

For each situation, run steps A through E in order. Tell the founder which situation you are starting before generating it:
> "Simulating situation [N]: **[Situation Name]**..."

### Step A — Before simulation (journey-level)

Generate a 5-phase "before" table showing the end user's current workflow without the solution:

| Phase | What happens (today, without the solution) |
|-------|---------------------------------------------|
| **Trigger** | What kicks off this situation |
| **Gather** | What information or materials they collect |
| **Execute** | The core work they do |
| **Review** | How they check their work |
| **Hand off** | What they deliver and to whom |

### Step B — Task-level drill (most painful phase)

Identify the 1–2 phases from Step A that are most time-consuming or error-prone. Break those phases into specific micro-tasks. Example format:

**[Phase name] — current steps:**
1. Opens [tool/system]
2. Manually copies [data] from [source]
3. Pastes into [destination]
4. Reformats manually
5. Cross-checks against [original source]
6. Sends for approval and waits

### Step C — After simulation (journey-level)

Rerun the same 5-phase table with the solution integrated. Show what specifically changes at each phase. Use the same table format as Step A.

For the phases identified in Step B, also show the task-level comparison:

**[Phase name] — steps with [solution name]:**
1. [Simplified step]
2. [Eliminated or automated step — mark as "✓ Handled automatically"]
3. [Remaining step]

### Step D — Benefit calculation

Calculate 4 metrics for this situation. Always show your reasoning. Label all numbers as estimates.

**⏱ Time saved**
*(Time saved = the hours per instance or per week that this situation currently takes vs. with the solution.)*
- Current time for this situation: [X hours/minutes] — [reasoning: e.g., "based on web research suggesting X task takes Y minutes on average"]
- With solution: [Y hours/minutes] — [reasoning]
- **Estimated time saved: [difference] per [instance/week]**

**✗ Error / rework reduction**
*(Error reduction = fewer mistakes that require going back and fixing work already done.)*
- Current error rate or rework trigger: [describe what causes errors or rework today]
- With solution: [what is eliminated or caught automatically]
- **Estimated reduction: [X%] fewer rework cycles** — [reasoning]

**★ Quality improvement**
*(Quality improvement = the output is better, more thorough, or more consistent — even if the time is similar.)*
- [2-3 sentences describing what gets better: completeness, consistency, accuracy, documentation quality, etc.]

**🧠 Cognitive load reduction**
*(Cognitive load = the mental effort, concentration, and stress the task requires. Lower is better.)*
- [2-3 sentences describing what mental effort is eliminated: tracking multiple sources, remembering steps, context switching, anxiety about errors, etc.]

### Step E — Cross-situation rollup (after all situations are done)

After completing Steps A–D for all situations, generate a summary:

**Total estimated time saved per week:**
[Add up the per-situation estimates, adjusted for how often each situation occurs. Show the math. Label as estimate.]

**Top 3 benefit messages:**
1. [The single most impactful benefit across all situations, in plain language]
2. [Second most impactful]
3. [Third most impactful]

**Key talking points for end user conversations:**
- [Sentence 1 the founder can say verbatim to a potential user]
- [Sentence 2]
- [Sentence 3]
- [Sentence 4]
- [Sentence 5]

## Output

### Full Report

Save to: `outputs/simulation-<persona-role>-<YYYY-MM-DD>.md`

Use a short, descriptive persona role name (e.g., `paralegal`, `project-manager`, `freelance-designer`).

Use this exact structure:

```markdown
# End User Simulation: [Persona Role]
Date: YYYY-MM-DD

## Persona Profile
**Role:** [role]
**Industry:** [industry]
**Daily context:** [1-2 sentences about their day]
**Their main problem:** [pain]
**How they cope today:** [current workaround]

## Solution Summary
[2 sentences describing the solution in plain language]

---

## Situation 1: [Situation Name]

### Before (current workflow)

| Phase | What happens today |
|-------|-------------------|
| Trigger | ... |
| Gather | ... |
| Execute | ... |
| Review | ... |
| Hand off | ... |

#### Task-level detail: [Most painful phase]
1. [step]
2. [step]
...

### After (with [solution name])

| Phase | What changes |
|-------|-------------|
| Trigger | ... |
| Gather | ... |
| Execute | ... |
| Review | ... |
| Hand off | ... |

#### Task-level detail: [Same phase — improved]
1. [step]
2. ✓ [eliminated step — handled automatically]
...

### Benefits for this situation
- ⏱ **Time saved:** [estimate with reasoning]
- ✗ **Error/rework reduction:** [estimate with reasoning]
- ★ **Quality improvement:** [qualitative]
- 🧠 **Cognitive load:** [qualitative]

---

## Situation 2: [Situation Name]
[Same structure as Situation 1]

---

## Situation 3: [Situation Name]
[Same structure as Situation 1]

---

## Cross-Situation Summary

### Total estimated time saved per week
[Calculation with reasoning. Label as estimate.]

### Top 3 benefit messages
1. [Benefit]
2. [Benefit]
3. [Benefit]

### Key talking points
- [Sentence]
- [Sentence]
- [Sentence]
- [Sentence]
- [Sentence]
```

### User-Facing One-Pager

Save to: `outputs/simulation-<persona-role>-onepager-<YYYY-MM-DD>.md`

Plain language, no jargon. This file is designed to be shared with real end users.

```markdown
# What [Solution Name] Could Change for [Role]

[One sentence: who this is for and what problem it addresses.]

## When [Situation 1 Name]
- [Benefit in plain terms — no jargon]
- [Benefit in plain terms]
- [Benefit in plain terms]

## When [Situation 2 Name]
- [Benefit in plain terms]
- [Benefit in plain terms]
- [Benefit in plain terms]

## When [Situation 3 Name]
- [Benefit in plain terms]
- [Benefit in plain terms]
- [Benefit in plain terms]

---

*[Closing sentence with a call to action — e.g., "Want to see this in action? Let's set up a 15-minute call."]*
```

## Chat Summary

Always show this in the conversation before mentioning the saved files:

```
## End User Simulation Summary: [Persona Role]

**Situations simulated:**
1. [Situation name]
2. [Situation name]
3. [Situation name]

**Estimated time saved per week:** ~[X hours] (estimate)

**Top 3 benefits:**
1. [Benefit]
2. [Benefit]
3. [Benefit]

**Key talking point:**
"[One sentence the founder can use verbatim with a potential user]"

Full report saved to: outputs/simulation-<persona>-<YYYY-MM-DD>.md
One-pager saved to: outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md

Next step: Run `/BusinessAgents:docs` and choose "User Impact Journey Map" to create a visual slide from this simulation.
```

## Hard Rules

- Always read `memory/icp.md` and `memory/startup-context.md` at the start — stop and redirect to `/BusinessAgents:founder` if uninitialized
- Validation report takes priority over discovery report when loading the solution description
- Use web search before asking the founder about workflow details — never make the founder do research the agent can do
- Always announce which situation you are simulating before generating it
- Never invent benefit numbers without showing your reasoning — label all estimates as estimates
- Explain each metric the first time it appears using the definitions in Step D
- Ask one question at a time
- Always produce both output files — never skip the one-pager
- Show the chat summary before mentioning the saved files
- If a situation has insufficient data from both web search and the founder, flag it with the ⚠️ warning and continue — do not stop
```

- [ ] **Step 2: Verify the file was created**

```bash
wc -l .claude/skills/BusinessAgents/simulate_user.md
```
Expected: more than 150 lines (the full skill content).

```bash
head -5 .claude/skills/BusinessAgents/simulate_user.md
```
Expected: first line is `# End User Simulator Agent`.

- [ ] **Step 3: Verify all sections are present**

```bash
grep "^##" .claude/skills/BusinessAgents/simulate_user.md
```
Expected output (in this order):
```
## How to Start
## Guided Questions
## Research Phase
## Simulation Structure
## Output
## Chat Summary
## Hard Rules
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/simulate_user.md
git commit -m "feat: add simulate_user skill — end user workflow simulation agent"
```

---

## Task 3: Update docs.md to add User Impact Journey Map

**Files:**
- Modify: `.claude/skills/BusinessAgents/docs.md`

- [ ] **Step 1: Add the new document type to the menu**

In `.claude/skills/BusinessAgents/docs.md`, find the `**Documents**` menu block that lists available document types. It ends before the `**Slides**` section. Add this entry at the end of the Documents list, before the `**Slides**` header:

```
> - User impact journey map — a before/after visual of how your solution changes the end user's workflow across real situations (requires a simulation report from `/BusinessAgents:simulate_user`)
```

- [ ] **Step 2: Add the User Impact Journey Map generation section**

After the `### Competitive Landscape Summary` section and before `## Slide Generation`, add this new section:

````markdown
### User Impact Journey Map

A before/after visual journey of how the solution changes the end user's workflow. Generated from the most recent simulation report in `outputs/`.

Before generating, read the most recent file matching `outputs/simulation-*-<YYYY-MM-DD>.md` (by date, not the onepager). If no simulation report exists, say: "This document requires a simulation report. Please run `/BusinessAgents:simulate_user` first, then come back here."

Generate a self-contained HTML file using the base template in the Slide Generation section. Build one slide per simulated situation, plus a summary slide. Each situation slide shows a two-column before/after table.

Save to: `outputs/docs/user-impact-journey-map-<YYYY-MM-DD>.html`

Use this slide structure:

**Slide 1 — Title slide:**
```html
<section class="active">
  <div class="label">End User Impact</div>
  <h1>How [Solution Name] Changes Your Day</h1>
  <p>For [persona role] in [industry] — [N] situations simulated</p>
</section>
```

**Slides 2–N — One per situation:**
```html
<section>
  <div class="label">Situation [N]</div>
  <h2>[Situation Name]</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;margin-top:1rem">
    <div>
      <div class="label" style="color:#ef4444">Before</div>
      <ul>
        <li>[Key before step 1]</li>
        <li>[Key before step 2]</li>
        <li>[Key before step 3]</li>
      </ul>
    </div>
    <div>
      <div class="label" style="color:#22c55e">After</div>
      <ul>
        <li>[Key after step 1]</li>
        <li>✓ [Eliminated step]</li>
        <li>[Key after step 3]</li>
      </ul>
    </div>
  </div>
  <p style="margin-top:1.5rem;color:#3b82f6">⏱ [Time saved estimate] &nbsp;|&nbsp; ✗ [Error reduction] &nbsp;|&nbsp; ★ [Quality note]</p>
</section>
```

**Last slide — Summary:**
```html
<section>
  <div class="label">Summary</div>
  <h2>Key Benefits</h2>
  <p class="big">~[X] hrs/week saved</p>
  <ul>
    <li>[Top benefit 1]</li>
    <li>[Top benefit 2]</li>
    <li>[Top benefit 3]</li>
  </ul>
  <p style="margin-top:2rem;color:#64748b">[Call to action sentence from one-pager]</p>
</section>
```

Tell the founder: "Journey map saved to `outputs/docs/user-impact-journey-map-<YYYY-MM-DD>.html`. Open it in any browser and use arrow keys to navigate. Share this during user interviews or demos."
````

- [ ] **Step 3: Verify the docs.md file still has all original sections intact**

```bash
grep "^###" .claude/skills/BusinessAgents/docs.md
```
Expected: all original section headers present, plus `### User Impact Journey Map` in the list.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/docs.md
git commit -m "feat: add User Impact Journey Map document type to docs agent"
```

---

## Task 4: Update the design spec to include simulate_user

**Files:**
- Modify: `docs/superpowers/specs/2026-04-22-business-agents-design.md`

- [ ] **Step 1: Add simulate_user to the agent lineup table**

In `docs/superpowers/specs/2026-04-22-business-agents-design.md`, find the Agent Lineup table:

```markdown
| Slash Command | Role |
|---|---|
| `/BusinessAgents:founder` | Startup memory manager + context keeper |
| `/BusinessAgents:discover` | Opportunity research + problem ranking |
| `/BusinessAgents:validate` | Idea validation + go/no-go recommendation |
| `/BusinessAgents:docs` | Business document + slide generation |
```

Add the new row after `/BusinessAgents:validate`:

```markdown
| `/BusinessAgents:simulate_user` | End user workflow simulation + benefit quantification |
```

- [ ] **Step 2: Update the Recommended First-Use Flow section**

Find the existing flow:

```
1. Run `/BusinessAgents:founder` in **Initialize** mode — sets up all memory files
2. Run `/BusinessAgents:discover` — research problems in your chosen space
3. Run `/BusinessAgents:validate` — test the most promising problem from step 2
4. Run `/BusinessAgents:docs` — generate a business plan or pitch deck once you have a validated idea
5. Return to `/BusinessAgents:founder` **Update** mode whenever your thinking evolves
```

Replace with:

```
1. Run `/BusinessAgents:founder` in **Initialize** mode — sets up all memory files
2. Run `/BusinessAgents:discover` — research problems in your chosen space
3. Run `/BusinessAgents:simulate_user` (optional early run) — simulate the end user's workflow before validating to sharpen your understanding of the benefit
4. Run `/BusinessAgents:validate` — test the most promising problem from step 2
5. Run `/BusinessAgents:simulate_user` (post-validation run) — now with more evidence, produce the shareable user one-pager
6. Run `/BusinessAgents:docs` — generate a business plan, pitch deck, or User Impact Journey Map slide
7. Return to `/BusinessAgents:founder` **Update** mode whenever your thinking evolves
```

- [ ] **Step 3: Add the data flow entry for simulate_user**

Find the Memory & Data Flow section. After the `/BusinessAgents:validate` block, add:

```
/BusinessAgents:simulate_user
  reads  → memory/startup-context.md
           memory/icp.md
           outputs/validation-*.md (most recent by date — priority)
           outputs/opportunity-discovery-*.md (fallback if no validation report)
  writes → outputs/simulation-<persona>-<YYYY-MM-DD>.md
           outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md
```

- [ ] **Step 4: Verify the spec file is valid**

```bash
grep "simulate_user" docs/superpowers/specs/2026-04-22-business-agents-design.md
```
Expected: 3 matches — one in the agent table, one in the first-use flow, one in the data flow section.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/2026-04-22-business-agents-design.md
git commit -m "docs: add simulate_user agent to design spec agent lineup and flow"
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Covered by |
|-----------------|------------|
| Hybrid ICP — load from memory, founder refines | Task 2, Question 1 |
| Hybrid solution — load from outputs, founder confirms | Task 2, Question 2 |
| 2–3 situations per run | Task 2, Question 3 |
| Web search for unknown workflows | Task 2, Research Phase |
| Two-pass simulation (journey + task-level drill) | Task 2, Steps A–C |
| Multi-metric benefits (4 metrics) | Task 2, Step D |
| Cross-situation rollup | Task 2, Step E |
| Full report output | Task 2, Output section |
| User-facing one-pager output | Task 2, Output section |
| Validation report takes priority over discovery report | Task 2, How to Start + Hard Rules |
| Docs agent: User Impact Journey Map | Task 3 |
| Slash command `/BusinessAgents:simulate_user` | Task 1 |
| Design spec updated | Task 4 |
| Hard rules (one question at a time, no invented numbers, etc.) | Task 2, Hard Rules |

**Placeholder scan:** No TBD, TODO, or vague steps in this plan.

**Type/name consistency:** The output filenames use `simulation-<persona>-<YYYY-MM-DD>.md` and `simulation-<persona>-onepager-<YYYY-MM-DD>.md` consistently across Task 2 skill content, Task 3 docs.md addition, and Task 4 spec update. The slash command `/BusinessAgents:simulate_user` is consistent across all tasks.
