# Interview Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `/BussinesAgents:interview` — a three-phase customer interview agent (Prepare / Coach / Synthesize) — and update the pipeline so `simulate_user` can also run right after discovery.

**Architecture:** This is a pure markdown skill system. There is no runtime code — each agent is a markdown prompt file that Claude reads and follows. "Tests" in this plan are manual: invoke the skill in Claude Code and verify the described behavior. Each task produces a self-contained, working change and ends with a commit.

**Tech Stack:** Markdown only. No dependencies, no build step, no package manager.

---

## File Map

| Action | Path | What it does |
|--------|------|-------------|
| Create | `.claude/skills/BussinesAgents/interview.md` | Full interview agent skill prompt |
| Create | `.claude/commands/BussinesAgents/interview.md` | Slash command stub that invokes the skill |
| Modify | `.claude/skills/BussinesAgents/simulate_user.md` | Widen idea status filter to include `discovered` and `interviewed` |
| Modify | `.claude/skills/BussinesAgents/founder.md` | Add `Interview: —` line to the New Idea template |
| Modify | `memory/ideas.md` | Add `Interview: —` line to the existing idea entry |
| Modify | `CLAUDE.md` | Add interview agent section; update flow and file structure |
| Modify | `README.md` | Add interview agent to agent table and flow section |

---

## Task 1: Create the slash command stub

**Files:**
- Create: `.claude/commands/BussinesAgents/interview.md`

- [ ] **Step 1: Create the command stub file**

Write `.claude/commands/BussinesAgents/interview.md` with exactly this content:

```markdown
Follow the Customer Interview Agent skill defined in `.claude/skills/BussinesAgents/interview.md` exactly. Read that file first, then execute it from the beginning.
```

- [ ] **Step 2: Verify**

Run: `cat .claude/commands/BussinesAgents/interview.md`

Expected output: the single line above.

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/BussinesAgents/interview.md
git commit -m "feat: add interview slash command stub"
```

---

## Task 2: Create the interview skill — How to Start

**Files:**
- Create: `.claude/skills/BussinesAgents/interview.md`

This task writes the file header and the How to Start section only. Phases are added in Tasks 3–5.

- [ ] **Step 1: Create the skill file with header and How to Start**

Write `.claude/skills/BussinesAgents/interview.md` with exactly this content:

```markdown
# Customer Interview Agent

You are the Customer Interview Agent. Your job is to guide founders through the full customer interview lifecycle: preparing a tailored script and tracking documents before calls, coaching live during calls, and synthesizing learnings into structured insights and ICP updates afterward.

**Important:** The founder may have no business background. Use plain language. In Coach mode, keep responses short — the founder may be on a live call.

## How to Start

1. Read `memory/startup-context.md` and `memory/icp.md` silently. If `startup-context.md` shows "(not yet initialized)", stop and say: "It looks like your startup context hasn't been set up yet. Please run `/BussinesAgents:founder` first — it only takes 5 minutes." Then stop.

2. Read `memory/ideas.md`. Filter to ideas with status `validated-go` or `interviewed`. Select the working idea for this session:
   - If the file does not exist or has no ideas with status `validated-go` or `interviewed`: say "No ideas are ready for interviews. Run `/BussinesAgents:validate` first and get a Go verdict." Then stop.
   - If exactly one qualifying idea exists: confirm — "I'll run interviews for: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple qualifying ideas exist: say "Which idea do you want to work on?" and show a numbered list (filtered ideas only):
     ```
     1. [slug] — [description]
     2. [slug] — [description]
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.

3. **Phase picker.** Check `outputs/ideas/<working-slug>/` for existing files to determine which phases to offer:

   | Existing files | Phases to offer |
   |---|---|
   | No `interview-script-*.md` exists | Prepare only |
   | Script exists, no `interview-insights-*.md` | Coach and Synthesize |
   | `interview-insights-*.md` exists | All three (new round creates new dated files) |

   Present only the relevant options:
   > "What would you like to do?
   > 1. Prepare — generate your interview script and tracking documents
   > 2. Coach — I'm on a call right now and need a follow-up question
   > 3. Synthesize — I've finished my interviews and have notes to analyze"

   Wait for the founder's choice.

4. Load source files based on the chosen phase:
   - **Prepare:** `memory/icp.md`, most recent `outputs/ideas/<working-slug>/validation-*.md`
   - **Coach:** above + most recent `outputs/ideas/<working-slug>/interview-script-*.md`
   - **Synthesize:** above + all `outputs/ideas/<working-slug>/interview-coaching-*.md`
```

- [ ] **Step 2: Verify**

Run: `head -60 .claude/skills/BussinesAgents/interview.md`

Expected: file starts with `# Customer Interview Agent`, contains the How to Start section with 4 numbered steps, phase picker table present.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BussinesAgents/interview.md
git commit -m "feat: add interview agent — How to Start section"
```

---

## Task 3: Add Phase 1 (Prepare) to the interview skill

**Files:**
- Modify: `.claude/skills/BussinesAgents/interview.md` (append)

- [ ] **Step 1: Append Phase 1 to the skill file**

Append to `.claude/skills/BussinesAgents/interview.md`:

````markdown

## Phase 1: Prepare

### Guided Questions

Ask one question at a time.

**Question 1:**
> "How many interviews are you planning to run? This sets up your tracking sheet with the right number of rows. If unsure, give a number — you can always add more."

Wait for the answer.

**Question 2:**
> "Is there anything specific you want to focus on — a particular assumption you're most worried about, or a type of user you're unsure about? Or should I pull the focus areas straight from your validation report?"

Wait for the answer. Then generate all three files below.

### File 1 — Interview Script

Save to: `outputs/ideas/<working-slug>/interview-script-<YYYY-MM-DD>.md`

Use this exact structure:

```markdown
# Interview Script: [Idea Name]
Date: YYYY-MM-DD

## How to Run This Call

**Before the call:**
- Review this script once so the questions feel natural
- Open your interview sheet or a notes document
- Block 45 minutes (most calls run 30 minutes)

**Starting the call:**
> "Hi [name], thanks for making time. I'm [your name] — I'm exploring [problem space] and trying to understand how people currently deal with [specific problem]. This isn't a sales call — I'm just learning. Mind if I ask you a few questions and take some notes?"

**How to listen without leading:**
- Ask "tell me more about that" instead of suggesting answers
- If they pause, wait — silence often leads to the most honest answer
- Avoid "would you say that...?" questions — let them use their own words

**Handling silence:**
- Count silently to 5 before speaking
- If still nothing: "Take your time — what comes to mind first?"

**Closing the call:**
> "Is there anything I didn't ask that you think is important for me to understand? ... This has been really helpful. Would it be okay if I followed up with one or two questions by email?"

---

## Opening Questions

*(Warm up the conversation — don't rush past these.)*

1. "Can you walk me through what a typical [day/week] looks like in your role?"
2. "What takes up most of your time that you wish it didn't?"
3. "[Open-ended question specific to ICP context]"

---

## Core Questions

*(One section per key assumption from the validation report.)*

### Assumption: [Assumption text]

**Ask:** "[Open-ended question that tests this assumption without leading]"

**If they confirm — probe deeper:** "How often does that happen? Walk me through the last time."

**If they push back — explore the gap:** "What does it look like when things go smoothly? What makes the difference?"

---

[Repeat for each assumption]

---

## Closing

"Who else do you think I should talk to — anyone in a similar role who might see this differently?"
```

### File 2 — Interview Tracker

Save to: `outputs/ideas/<working-slug>/interview-tracker-<YYYY-MM-DD>.csv`

Generate CSV content with:
- Header row: `ID,Date,Name,Role,Company Size,[first 6 words of each core question],Key Quote,Signal,Notes`
- N data rows pre-filled with sequential IDs (1, 2, 3…) and empty values for all other columns

(N = the number the founder gave in Question 1)

### File 3 — Interview Sheet

Save to: `outputs/ideas/<working-slug>/interview-sheet-<YYYY-MM-DD>.html`

Self-contained HTML, no external dependencies. Generate N sections — one per interviewee — using this template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Interview Sheet — [Idea Name]</title>
<style>
  body { font-family: Georgia, serif; max-width: 720px; margin: 40px auto; color: #1a1a1a; }
  h1 { text-align: center; font-size: 18px; margin-bottom: 40px; }
  .interview { border: 1px solid #ccc; border-radius: 8px; padding: 24px; margin-bottom: 40px; page-break-after: always; }
  .header-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
  .field label { display: block; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; color: #666; margin-bottom: 4px; }
  .field .line { border-bottom: 1px solid #999; height: 28px; }
  .question { margin-bottom: 24px; }
  .question p { font-weight: bold; margin-bottom: 8px; }
  .answer-box { border: 1px solid #ddd; border-radius: 4px; min-height: 80px; }
  .key-quote { margin-top: 24px; border-left: 3px solid #333; padding-left: 12px; }
  .signal { margin-top: 16px; }
  @media print { body { margin: 20px; } .interview { border: none; } }
</style>
</head>
<body>
<h1>Customer Interview — [Idea Name]</h1>

<!-- Repeat this block N times -->
<div class="interview">
  <h2>Interview #[N]</h2>
  <div class="header-fields">
    <div class="field"><label>Name</label><div class="line"></div></div>
    <div class="field"><label>Date</label><div class="line"></div></div>
    <div class="field"><label>Role</label><div class="line"></div></div>
    <div class="field"><label>Company Size</label><div class="line"></div></div>
  </div>

  <!-- One .question block per opening question and per core question -->
  <div class="question">
    <p>[Question text]</p>
    <div class="answer-box"></div>
  </div>

  <div class="key-quote">
    <label style="font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:0.05em;color:#666;">Key Quote</label>
    <div class="line" style="border-bottom:1px solid #999;height:28px;margin-top:8px;"></div>
  </div>

  <div class="signal">
    <strong>Signal:</strong> &nbsp; ☐ Strong &nbsp;&nbsp; ☐ Weak &nbsp;&nbsp; ☐ Neutral
  </div>
</div>

</body>
</html>
```

### Closing Message

> "Your interview kit is ready:
>
> — Script: `outputs/ideas/<working-slug>/interview-script-<date>.md`
> — Tracker: `outputs/ideas/<working-slug>/interview-tracker-<date>.csv` (open in Excel or Google Sheets)
> — Sheet: `outputs/ideas/<working-slug>/interview-sheet-<date>.html` (open in browser to print)
>
> When you're on a call and get stuck, run `/BussinesAgents:interview` and choose **Coach**.
> When all interviews are done, run `/BussinesAgents:interview` and choose **Synthesize**."
````

- [ ] **Step 2: Verify**

Run: `grep -n "Phase 1\|File 1\|File 2\|File 3\|Closing Message" .claude/skills/BussinesAgents/interview.md`

Expected: all six labels present, in order.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BussinesAgents/interview.md
git commit -m "feat: add interview agent — Phase 1 Prepare"
```

---

## Task 4: Add Phase 2 (Coach) to the interview skill

**Files:**
- Modify: `.claude/skills/BussinesAgents/interview.md` (append)

- [ ] **Step 1: Append Phase 2 to the skill file**

Append to `.claude/skills/BussinesAgents/interview.md`:

````markdown

## Phase 2: Coach

On entering Coach mode, say:
> "Coach mode — tell me who you're talking to (role, company size) and what they just said. I'll respond with one question to ask next."

### The Loop

For each founder message describing what the interviewee just said:
1. Identify the most useful follow-up: probe for specifics, test an untouched assumption, or pivot if the problem isn't confirmed
2. Respond with exactly:
   - **One question** in plain language the founder can read verbatim
   - One optional note in parentheses explaining why — only if non-obvious

Example exchange:
> **Founder:** "She said contract review happens weekly but it's not that painful"
>
> **Agent:** Ask: *"What IS the most painful part of your week?"*
> *(Pivoting — if this problem isn't severe enough, find what is.)*

Track which validation assumptions have been addressed in this session. When an important assumption remains untested after several exchanges, prompt:
> "We haven't tested [assumption] yet — ask: '[suggested question]'"

### Ending the Session

When the founder types `done` or `call ended`:

1. Count existing `interview-coaching-*.md` files in `outputs/ideas/<working-slug>/`. Set N = count + 1, zero-padded to 2 digits (01, 02, 03…).

2. Save: `outputs/ideas/<working-slug>/interview-coaching-<YYYY-MM-DD>-<N>.md`

Use this exact structure:

```markdown
# Coaching Session Log
Date: YYYY-MM-DD
Interviewee: [role] at [company size]
Session: N

## Topics Covered
- [topic]

## Assumptions Addressed
- ✓ [assumption]: [what was said]
- ~ [assumption]: [mixed signal summary]
- ✗ [assumption]: [contrary evidence]

## Notable Quotes
- "[quote]"

## Assumptions Not Reached
- [assumption not tested this session]
```

3. Say:
> "Session log saved. Run `/BussinesAgents:interview` → **Synthesize** when you've finished all your interviews."
````

- [ ] **Step 2: Verify**

Run: `grep -n "Phase 2\|Coach mode\|Ending the Session\|interview-coaching" .claude/skills/BussinesAgents/interview.md`

Expected: all four labels present.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BussinesAgents/interview.md
git commit -m "feat: add interview agent — Phase 2 Coach"
```

---

## Task 5: Add Phase 3 (Synthesize), Registry Update, and Hard Rules

**Files:**
- Modify: `.claude/skills/BussinesAgents/interview.md` (append)

- [ ] **Step 1: Append Phase 3, Registry Update, and Hard Rules**

Append to `.claude/skills/BussinesAgents/interview.md`:

````markdown

## Phase 3: Synthesize

Load all `interview-coaching-*.md` files in `outputs/ideas/<working-slug>/`.

Say:
> "I can see [N] coaching session log(s) for **[slug]**. Do you have additional notes to add — from interviews where you didn't use Coach mode, or anything else? Paste them here, or say 'no' to proceed."

Wait for the founder's response. Then run the full analysis.

### Analysis

Produce a structured cross-interview analysis covering all of these sections:

**Assumptions audit** — for each assumption from the validation report:
- `✓ Confirmed` — how many interviewees supported it and what they said
- `✗ Busted` — contradicting evidence with specifics
- `~ Partial` — mixed signals with explanation

**New findings** — patterns that emerged outside the original assumptions

**ICP refinement signals** — specific things interviewees said that suggest changes to role, pain, workaround, or willingness to pay in `memory/icp.md`

**Top 3 quotes** — most useful verbatim quotes across all interviews

### ICP Update Step

For each ICP refinement signal found, present specific proposed edits before writing anything:

> "Based on your interviews, here's what I think should change in your ICP:
>
> — [Field]: '[current value]' → '[proposed value]' ([evidence: N of M interviewees said…])
>
> Confirm and I'll update `memory/icp.md` and log the changes — same way `/BussinesAgents:founder` would. Or say 'skip' to leave the ICP unchanged."

Wait for the founder's response.

If confirmed:
1. Write the updates to `memory/icp.md`
2. Update `Last updated:` in `memory/icp.md` to today's date
3. Add an entry to `memory/decisions-log.md`:
```
[YYYY-MM-DD] What changed: ICP updated after customer interviews (<working-slug>). Why: [one-sentence summary of what interviews revealed].
```

### Output File

Save to: `outputs/ideas/<working-slug>/interview-insights-<YYYY-MM-DD>.md`

Use this exact structure:

```markdown
# Interview Insights: [Idea Name]
Date: YYYY-MM-DD
Interviews conducted: N

## Assumptions Audit

### ✓ Confirmed
- **[Assumption]:** [evidence from N of M interviews] — "[representative quote]"

### ✗ Busted
- **[Assumption]:** [contradicting evidence] — "[representative quote]"

### ~ Partial
- **[Assumption]:** [mixed signal explanation]

## New Findings
- [Finding]: [evidence]

## ICP Refinement Signals
- [Signal]: [what changed and why]

## Top Quotes
1. "[quote]" — [role], [company size]
2. "[quote]" — [role], [company size]
3. "[quote]" — [role], [company size]

## Summary
[3 sentences: what was learned, what changed, what to do next]
```

### Closing Message

> "Insights saved. [If ICP was updated: 'Your ICP has been updated based on what you heard.']
>
> Next step: run `/BussinesAgents:simulate_user` for a refined simulation — this time grounded in what real users told you."

---

## Registry Update

After saving `interview-insights-<YYYY-MM-DD>.md`:

1. Find the entry for `<working-slug>` in `memory/ideas.md`.
2. Set `**Status:**` to `interviewed`.
3. Set the `Interview:` stage line to today's date.
4. Update `Last updated:` at the top of `memory/ideas.md` to today's date.

---

## Hard Rules

- Always read `memory/icp.md` and `memory/startup-context.md` at the start — stop and redirect to `/BussinesAgents:founder` if uninitialized
- Only accept `validated-go` or `interviewed` ideas — never run on `discovered` or earlier statuses
- Phase picker must check existing files before offering phases — never offer Coach or Synthesize if no script exists
- Coach mode responses must be one question maximum — never multiple questions at once
- In Synthesize, always propose ICP changes before writing them — never update `memory/icp.md` without explicit founder confirmation
- Always log ICP changes to `memory/decisions-log.md` using the founder agent's entry format
- Always produce `interview-insights-<date>.md` — never skip the synthesis output file
- Always update `memory/ideas.md` after saving insights — set status to `interviewed` and record the date
- Save all output files to `outputs/ideas/<working-slug>/` — never to the flat `outputs/` folder
- Ask one question at a time in Prepare phase
````

- [ ] **Step 2: Verify the complete skill file**

Run: `grep -c "^##" .claude/skills/BussinesAgents/interview.md`

Expected: 9 (How to Start, Phase 1, Phase 2, Phase 3, Registry Update, Hard Rules, plus 3 sub-headings inside phases)

Run: `wc -l .claude/skills/BussinesAgents/interview.md`

Expected: more than 200 lines.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BussinesAgents/interview.md
git commit -m "feat: add interview agent — Phase 3 Synthesize, Registry Update, Hard Rules"
```

---

## Task 6: Widen simulate_user status filter

**Context:** `simulate_user` currently only accepts `validated-go` ideas. The new flow requires it to also run on `discovered` ideas (1st simulation run, hypothesis) and `interviewed` ideas (2nd run, refined).

**Files:**
- Modify: `.claude/skills/BussinesAgents/simulate_user.md`

The current lines 11–19 read:

```
2. Read `memory/ideas.md`. Filter to ideas with status `validated-go`. Select the working idea for this session:
   - If the file does not exist or has no ideas with status `validated-go`: say "No ideas are ready for simulation. Run `/BussinesAgents:validate` first and get a Go verdict." Then stop.
   - If exactly one `validated-go` idea exists: confirm — "I'll simulate end users for: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple `validated-go` ideas exist: say "Which idea do you want to simulate?" and show a numbered list (`validated-go` ideas only):
     ```
     1. [slug] — [description]
     2. [slug] — [description]
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.
```

- [ ] **Step 1: Replace the status filter block**

In `.claude/skills/BussinesAgents/simulate_user.md`, replace the block above with:

```
2. Read `memory/ideas.md`. Filter to ideas with status `discovered`, `validated-go`, or `interviewed`. Select the working idea for this session:
   - If the file does not exist or has no qualifying ideas: say "No ideas are ready for simulation. Run `/BussinesAgents:discover` first to generate a discovery report." Then stop.
   - If exactly one qualifying idea exists: confirm — "I'll simulate end users for: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple qualifying ideas exist: say "Which idea do you want to simulate?" and show a numbered list (qualifying ideas only):
     ```
     1. [slug] — [description]
     2. [slug] — [description]
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.
```

- [ ] **Step 2: Verify**

Run: `grep -n "discovered\|validated-go\|interviewed" .claude/skills/BussinesAgents/simulate_user.md | head -10`

Expected: line 11 area contains all three statuses: `discovered`, `validated-go`, `interviewed`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/BussinesAgents/simulate_user.md
git commit -m "feat: allow simulate_user to run on discovered and interviewed ideas"
```

---

## Task 7: Update founder.md template and memory/ideas.md

**Files:**
- Modify: `.claude/skills/BussinesAgents/founder.md`
- Modify: `memory/ideas.md`

### Part A — founder.md New Idea template

The current New Idea template in `founder.md` (inside the `### New Idea` section) has:

```markdown
**Stages:**
- Discovery:   —
- Validation:  —
- Simulation:  —
- Docs:        —
```

- [ ] **Step 1: Add Interview stage line to the template**

In `.claude/skills/BussinesAgents/founder.md`, replace that block with:

```markdown
**Stages:**
- Discovery:   —
- Validation:  —
- Interview:   —
- Simulation:  —
- Docs:        —
```

- [ ] **Step 2: Verify**

Run: `grep -A6 "\*\*Stages:\*\*" .claude/skills/BussinesAgents/founder.md`

Expected: 5 stage lines with Interview between Validation and Simulation.

### Part B — memory/ideas.md existing entry

The existing idea entry (`private-ai-montreal-legal`) does not have an Interview stage line. Add it.

Current Stages block:
```
**Stages:**
- Discovery:   2026-04-23
- Validation:  2026-04-24 (Go)
- Simulation:  2026-04-24
- Docs:        —
```

- [ ] **Step 3: Add Interview line to the existing entry**

In `memory/ideas.md`, replace the Stages block above with:

```
**Stages:**
- Discovery:   2026-04-23
- Validation:  2026-04-24 (Go)
- Interview:   —
- Simulation:  2026-04-24
- Docs:        —
```

- [ ] **Step 4: Verify**

Run: `grep -A7 "\*\*Stages:\*\*" memory/ideas.md`

Expected: Interview line present between Validation and Simulation.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BussinesAgents/founder.md memory/ideas.md
git commit -m "feat: add Interview stage line to ideas template and existing entry"
```

---

## Task 8: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

Three changes: add interview agent section, update the flow diagram, update the file structure block.

- [ ] **Step 1: Add interview agent section after the validate section**

In `CLAUDE.md`, find the section:

```markdown
**Hands off to:** `/BussinesAgents:simulate_user` — run it after a Go verdict.

---

### 4. `/BussinesAgents:simulate_user` — End User Simulator
```

Replace with:

```markdown
**Hands off to:** `/BussinesAgents:simulate_user` — run it for a first hypothesis simulation, then run `/BussinesAgents:interview`.

---

### 4. `/BussinesAgents:interview` — Customer Interview Agent

**Job:** Guide founders through the full interview lifecycle — generating a tailored script and tracking documents before calls, coaching live during calls, and synthesizing learnings into structured insights and ICP updates.

**Reads:** `memory/startup-context.md`, `memory/icp.md` + the validation report

**Three phases:**
- **Prepare** — generates a tailored interview script, a CSV tracker (one row per interviewee), and a printable HTML interview sheet
- **Coach** — live coaching during a call: founder describes what was said, agent responds with one follow-up question; saves a session log when the call ends
- **Synthesize** — after all interviews, audits assumptions (confirmed / busted / partial), surfaces new findings, proposes specific ICP updates for the founder to confirm

**Outputs:**
- `outputs/ideas/<slug>/interview-script-<YYYY-MM-DD>.md`
- `outputs/ideas/<slug>/interview-tracker-<YYYY-MM-DD>.csv`
- `outputs/ideas/<slug>/interview-sheet-<YYYY-MM-DD>.html`
- `outputs/ideas/<slug>/interview-coaching-<YYYY-MM-DD>-<N>.md` (one per session)
- `outputs/ideas/<slug>/interview-insights-<YYYY-MM-DD>.md`

**Hands off to:** `/BussinesAgents:simulate_user` — run it again after interviews for a refined simulation.

---

### 5. `/BussinesAgents:simulate_user` — End User Simulator
```

- [ ] **Step 2: Update the agent numbering**

In `CLAUDE.md`, the old sections 4 and 5 become 5 and 6. Find and update:

Replace `### 4. \`/BussinesAgents:simulate_user\`` with `### 5. \`/BussinesAgents:simulate_user\``

Replace `### 5. \`/BussinesAgents:docs\`` with `### 6. \`/BussinesAgents:docs\``

- [ ] **Step 3: Update the Intended Flow section**

Find the Intended Flow code block:

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

Replace with:

```
1. /BussinesAgents:founder        →  Initialize memory (run once at the start)
         ↓
2. /BussinesAgents:discover       →  Find top 3 problems worth solving
         ↓
3. /BussinesAgents:simulate_user  →  1st run: hypothesis — what do we think changes for the user?
         ↓
4. /BussinesAgents:validate       →  Test the top problem. Get a Go/No-go verdict.
         ↓ (Go)
5. /BussinesAgents:interview      →  Talk to real users. Refine the ICP.
         ↓
6. /BussinesAgents:simulate_user  →  2nd run: refined — what actually changes, based on real data
         ↓
7. /BussinesAgents:docs           →  Generate documents and pitch materials
```

- [ ] **Step 4: Update the file structure block**

Find the outputs structure block and add interview files. Replace:

```
    <slug>/              ← one folder per product idea (slug = short lowercase name)
      opportunity-discovery-*.md          ← discovery report
      validation-*.md                     ← validation plan with Go/No-go verdict
      simulation-<persona>-*.md           ← end user simulation report
      simulation-<persona>-onepager-*.md  ← plain-language user-facing summary
      docs/
```

With:

```
    <slug>/              ← one folder per product idea (slug = short lowercase name)
      opportunity-discovery-*.md          ← discovery report
      validation-*.md                     ← validation plan with Go/No-go verdict
      interview-script-*.md               ← tailored interview question guide
      interview-tracker-*.csv             ← spreadsheet to fill in during/after calls
      interview-sheet-*.html              ← printable interview sheet
      interview-coaching-*-*.md           ← per-session coaching log
      interview-insights-*.md             ← synthesis: assumptions audit + ICP updates
      simulation-<persona>-*.md           ← end user simulation report
      simulation-<persona>-onepager-*.md  ← plain-language user-facing summary
      docs/
```

- [ ] **Step 5: Verify**

Run: `grep -n "interview\|Interview" CLAUDE.md | head -20`

Expected: interview agent section present, flow diagram updated, file structure updated.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for interview agent"
```

---

## Task 9: Update README.md

**Files:**
- Modify: `README.md`

Two changes: add interview agent to the agent table, update the flow section.

- [ ] **Step 1: Update the agent table**

In `README.md`, find the table:

```markdown
| Step | Agent | What you get |
|------|-------|-------------|
| 1 | `/BussinesAgents:founder` | Your startup context saved to memory — vision, constraints, ideal customer |
| 2 | `/BussinesAgents:discover` | Top 3 problems worth solving, ranked by evidence and market timing |
| 3 | `/BussinesAgents:validate` | Go / No-go verdict + 3 cheap experiments to test before building anything |
| 4 | `/BussinesAgents:simulate_user` | Before/after workflow simulations showing exactly what changes for your user |
| 5 | `/BussinesAgents:docs` | Business plan, pitch deck, value proposition, canvas, and more |
```

Replace with:

```markdown
| Step | Agent | What you get |
|------|-------|-------------|
| 1 | `/BussinesAgents:founder` | Your startup context saved to memory — vision, constraints, ideal customer |
| 2 | `/BussinesAgents:discover` | Top 3 problems worth solving, ranked by evidence and market timing |
| 3 | `/BussinesAgents:simulate_user` | 1st simulation: hypothesis of what changes for your user, based on discovery |
| 4 | `/BussinesAgents:validate` | Go / No-go verdict + 3 cheap experiments to test before building anything |
| 5 | `/BussinesAgents:interview` | Interview script, tracker CSV, printable sheet + live coaching + insight synthesis |
| 6 | `/BussinesAgents:simulate_user` | 2nd simulation: refined — grounded in what real users told you |
| 7 | `/BussinesAgents:docs` | Business plan, pitch deck, value proposition, canvas, and more |
```

- [ ] **Step 2: Update the flow section**

Find the flow code block:

```
/BussinesAgents:founder       →  Set up memory (run once)
         ↓
/BussinesAgents:discover      →  Find real problems worth solving
         ↓
/BussinesAgents:validate      →  Test the top problem. Get a Go/No-go.
         ↓  (Go)
/BussinesAgents:simulate_user →  Show how your solution changes the user's day
         ↓
/BussinesAgents:docs          →  Generate documents and pitch materials
```

Replace with:

```
/BussinesAgents:founder        →  Set up memory (run once)
         ↓
/BussinesAgents:discover       →  Find real problems worth solving
         ↓
/BussinesAgents:simulate_user  →  1st run: hypothesis simulation
         ↓
/BussinesAgents:validate       →  Test the top problem. Get a Go/No-go.
         ↓  (Go)
/BussinesAgents:interview      →  Prepare → Coach → Synthesize
         ↓
/BussinesAgents:simulate_user  →  2nd run: refined simulation
         ↓
/BussinesAgents:docs           →  Generate documents and pitch materials
```

- [ ] **Step 3: Add interview agent section**

In `README.md`, after the `validate` agent section and before the `simulate_user` section, add:

```markdown
### `/BussinesAgents:interview` — Customer Interview Agent

Guides founders through the full interview lifecycle. Generates a tailored question script, a CSV tracker to fill in across interviewees, and a printable HTML sheet for use on calls. Provides live coaching during calls — describe what the interviewee said, get one follow-up question back. After all calls, synthesizes findings: which assumptions held, which broke, what was unexpected. Proposes specific ICP updates for the founder to confirm before writing anything.

**Outputs:**
- `outputs/ideas/<slug>/interview-script-<date>.md` — full interview guide
- `outputs/ideas/<slug>/interview-tracker-<date>.csv` — open in Excel/Google Sheets
- `outputs/ideas/<slug>/interview-sheet-<date>.html` — open in browser to print
- `outputs/ideas/<slug>/interview-coaching-<date>-<N>.md` — per-session log
- `outputs/ideas/<slug>/interview-insights-<date>.md` — synthesis report

---
```

- [ ] **Step 4: Verify**

Run: `grep -n "interview\|Interview" README.md | head -15`

Expected: table updated, flow updated, interview agent section present.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: update README for interview agent and revised flow"
```

---

## Self-Review Checklist

After all tasks are committed, run this check:

- [ ] `/BussinesAgents:interview` command stub exists and points to the skill file
- [ ] Skill file has all three phases (Prepare, Coach, Synthesize), Registry Update, and Hard Rules
- [ ] `simulate_user.md` accepts `discovered`, `validated-go`, and `interviewed`
- [ ] `founder.md` New Idea template has 5 stage lines including Interview
- [ ] `memory/ideas.md` existing entry has Interview stage line
- [ ] `CLAUDE.md` shows 6 agents, updated flow, updated file structure
- [ ] `README.md` shows 7-row table, updated flow, interview agent section
