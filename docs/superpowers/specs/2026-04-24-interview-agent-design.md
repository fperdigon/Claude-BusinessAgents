# Interview Agent Design

> **For agentic workers:** Use superpowers:writing-plans to implement this spec.

## Goal

Add `/BusinessAgents:interview` — a customer interview agent that guides founders through the full interview lifecycle: generating a tailored script and tracking documents before calls, coaching live during calls, and synthesizing learnings into structured insights and ICP updates afterward.

## Fit in the System

The interview agent slots between `validate` and the second run of `simulate_user`:

```
discover         → status: discovered
simulate_user    → 1st run: hypothesis simulation from discovery data
validate         → status: validated-go
interview        → status: interviewed
simulate_user    → 2nd run: refined simulation based on real interview data
```

This means `simulate_user` must also be runnable on `discovered` ideas (first run). Its status filter currently accepts only `validated-go` — this needs to be widened to also accept `discovered`.

## Status Lifecycle Change

```
new → discovered → validated-go → interviewed → simulated → documented → archived
```

`interviewed` is set after Synthesize completes. Running the interview agent is optional but strongly recommended before the second `simulate_user` run.

The `memory/ideas.md` stage block gains a new line:

```
- Interview:   —
```

Added between Validation and Simulation.

---

## Agent Architecture

### Source Files Read

| Phase | Files loaded |
|-------|-------------|
| Prepare | `memory/icp.md`, `validation-<date>.md` |
| Coach | `memory/icp.md`, `validation-<date>.md`, `interview-script-<date>.md` |
| Synthesize | `memory/icp.md`, `validation-<date>.md`, `interview-script-<date>.md`, all `interview-coaching-*.md` |

### Output Files Written

All saved to `outputs/ideas/<slug>/`:

| File | Phase | Description |
|------|-------|-------------|
| `interview-script-<date>.md` | Prepare | Question list + how-to guide |
| `interview-tracker-<date>.csv` | Prepare | One row per interviewee, one column per question |
| `interview-sheet-<date>.html` | Prepare | Printable HTML, one section per interviewee |
| `interview-coaching-<date>-<N>.md` | Coach | Log of one coaching session (N = sequential number 01, 02…) |
| `interview-insights-<date>.md` | Synthesize | Full synthesis: assumptions audit, new findings, ICP signals, top quotes |

---

## How to Start

1. Read `memory/startup-context.md` and `memory/icp.md` silently. If uninitialized, stop: *"Run `/BusinessAgents:founder` first."*

2. **Idea picker.** Read `memory/ideas.md`. Filter to ideas with status `validated-go` or `interviewed`.
   - None found → *"No ideas are ready for interviews. Run `/BusinessAgents:validate` first."* Stop.
   - One found → confirm with founder.
   - Multiple found → show numbered list, wait for choice.

3. **Phase picker.** Check `outputs/ideas/<slug>/` for existing files:

   | Existing files | Phases offered |
   |---|---|
   | No `interview-script-*.md` | Prepare only |
   | Script exists, no `interview-insights-*.md` | Coach and Synthesize |
   | Insights file exists | All three (second round creates new dated files) |

   Present only the relevant phases:
   > *"What would you like to do?*
   > *1. Prepare — generate your interview script and tracking documents*
   > *2. Coach — I'm on a call right now and need a follow-up question*
   > *3. Synthesize — I've finished my interviews and have notes to analyze"*

4. Load source files for the selected phase (see table above).

---

## Phase 1: Prepare

### Guided Questions

**Question 1:**
> "How many interviews are you planning to run? This sets up your tracking sheet with the right number of rows. If unsure, give a number — you can always add more."

**Question 2:**
> "Is there anything specific you want to focus on — a particular assumption you're most worried about, or a type of user you're unsure about? Or should I pull the focus areas straight from your validation report?"

### File 1 — Interview Script: `interview-script-<date>.md`

Structure:
- **How to run this call** — 1-page guide: how to introduce yourself, how to listen without leading, how to handle silence, how to close
- **Opening questions** — 2–3 warm-up questions (role, daily routine, context)
- **Core questions** — one question per assumption from the validation report, with 1–2 probing follow-ups each
- **Closing** — *"Is there anything I didn't ask that you think is important?"* + how to end gracefully

### File 2 — Interview Tracker: `interview-tracker-<date>.csv`

Columns:
```
ID | Date | Name | Role | Company Size | [one column per core question, summarized] | Key quote | Signal (Strong/Weak/Neutral) | Notes
```

Pre-populated with N rows (from Question 1). Question header text derived from the script.

### File 3 — Interview Sheet: `interview-sheet-<date>.html`

Self-contained HTML (no internet required). One section per interviewee with:
- Header fields: Name, Date, Role, Company
- Each question printed with blank space for notes
- Key quote field
- Signal checkbox: `[ ] Strong  [ ] Weak  [ ] Neutral`

Designed for printing or screen use on a tablet during the call.

### Closing Message

> *"Your interview kit is ready:*
> *— Script: `outputs/ideas/<slug>/interview-script-<date>.md`*
> *— Tracker: `outputs/ideas/<slug>/interview-tracker-<date>.csv` (open in Excel or Google Sheets)*
> *— Sheet: `outputs/ideas/<slug>/interview-sheet-<date>.html` (open in browser to print)*
>
> *When you're on a call and get stuck, run `/BusinessAgents:interview` → Coach.*
> *When all interviews are done, run `/BusinessAgents:interview` → Synthesize."*

---

## Phase 2: Coach

The founder is on a live call. All responses must be short and immediate — no preambles.

### Opening

> *"Coach mode — tell me who you're talking to (role, company size) and what they just said. I'll respond with one question to ask next."*

### The Loop

Founder types a short description of what the interviewee just said. Agent responds with:
- One follow-up question in plain language (readable verbatim)
- One optional note in parentheses explaining why — only if non-obvious

Example:
> **Founder:** "She said contract review happens weekly but isn't that painful"
>
> **Agent:** Ask: *"What IS the most painful part of your week?"*
> *(Pivoting — if this problem isn't severe enough, find what is.)*

The agent tracks which validation assumptions have been addressed and prompts when untested ones remain:
> *"We haven't tested the pricing assumption yet — ask: 'If a tool could cut that in half, what would that be worth to you?'"*

### Ending

When the founder types `done` or `call ended`, save:

**`interview-coaching-<date>-<N>.md`** where N is a sequential number (01, 02, 03…) incremented per session within this slug.

Contents:
- Interviewee: role, company size
- Topics covered
- Assumptions touched (which ones, what was said)
- Notable quotes captured during the session

Then:
> *"Saved. Run `/BusinessAgents:interview` → Synthesize when you've finished all your interviews."*

---

## Phase 3: Synthesize

### Opening

Agent loads all coaching logs and asks:
> *"I can see [N] coaching session log(s). Do you have additional notes to add — from interviews where you didn't use Coach mode, or anything else? Paste them here, or say 'no' to proceed."*

### Analysis

Produces a structured cross-interview analysis:

**Assumptions audit** — for each assumption from the validation report:
- `✓ Confirmed` — supporting interviewees and what they said
- `✗ Busted` — contradicting evidence
- `~ Partial` — mixed signals with explanation

**New findings** — patterns that emerged outside the original assumptions

**ICP refinement signals** — role, pain, workaround, or willingness-to-pay signals that suggest ICP changes

**Top 3 quotes** — most useful verbatim quotes across all interviews

### ICP Update Step

For each ICP refinement signal, propose a specific edit:

> *"Based on your interviews, here's what I think should change in your ICP:*
>
> *— Role: 'paralegal' → 'junior associate' (3 of 4 interviewees were associates)*
> *— Pain: refine to 'deadline-driven contract review under partner supervision'*
>
> *Confirm and I'll update `memory/icp.md` and log the changes — same way `/BusinessAgents:founder` would. Or say 'skip' to leave the ICP as-is."*

If confirmed: write updates to `memory/icp.md`. Add entry to `memory/decisions-log.md`:
```
[YYYY-MM-DD] What changed: ICP updated after customer interviews (<slug>). Why: [summary of interview findings].
```

### Output File: `interview-insights-<date>.md`

Structure:
```markdown
# Interview Insights: [Idea Name]
Date: YYYY-MM-DD
Interviews conducted: N

## Assumptions Audit
### ✓ Confirmed
...
### ✗ Busted
...
### ~ Partial
...

## New Findings
...

## ICP Refinement Signals
...

## Top Quotes
1. "[quote]" — [role], [company size]
2. ...
3. ...

## Summary
[3 sentences: what was learned, what changed, what to do next]
```

### Closing Message

> *"Insights saved. Your ICP has been updated.*
>
> *Next step: run `/BusinessAgents:simulate_user` for a refined simulation — this time grounded in what you heard from real users."*

---

## Registry Update

After saving `interview-insights-<date>.md`:

1. Find the entry for `<working-slug>` in `memory/ideas.md`.
2. Set `**Status:**` to `interviewed`.
3. Set the `Interview:` stage line to today's date.
4. Update `Last updated:` at the top of the file.

---

## simulate_user Filter Change

The existing `simulate_user` skill must be updated to accept ideas with status `discovered` in addition to `validated-go`. This enables the first simulation run (hypothesis) immediately after discovery.

Change the idea picker filter from:
```
Filter to ideas with status `validated-go`
```
To:
```
Filter to ideas with status `validated-go`, `interviewed`, or `discovered`
```

The existing fallback logic (validation report → discovery report) already handles loading the right source file per status.

---

## New Files

| File | Purpose |
|------|---------|
| `.claude/skills/BusinessAgents/interview.md` | Agent skill prompt |
| `.claude/commands/BusinessAgents/interview.md` | Slash command stub |

## Modified Files

| File | Change |
|------|--------|
| `.claude/skills/BusinessAgents/simulate_user.md` | Widen idea picker filter to include `discovered` and `interviewed` |
| `memory/ideas.md` format (in `founder.md`) | Add `Interview: —` stage line to the New Idea template |
| `CLAUDE.md` | Add interview agent description; update flow diagram; update file structure |
| `README.md` | Add interview agent to the agent table and flow section |

---

## Hard Rules

- Always read `memory/icp.md` and `memory/startup-context.md` at the start — stop and redirect if uninitialized
- Only accept `validated-go` or `interviewed` ideas — never run on `discovered` or earlier
- Phase picker must detect existing files before offering phases — never offer Coach or Synthesize if no script exists
- Coach mode responses must be one question maximum — never multiple questions at once
- In Synthesize, propose ICP changes before writing them — never update `memory/icp.md` without explicit founder confirmation
- Always log ICP changes to `memory/decisions-log.md` using the founder agent's format
- Always produce `interview-insights-<date>.md` — never skip synthesis output
- Always update `memory/ideas.md` after saving insights — set status to `interviewed` and record the date
- Save all output files to `outputs/ideas/<working-slug>/` — never to the flat `outputs/` folder
- Ask one question at a time in Prepare phase
