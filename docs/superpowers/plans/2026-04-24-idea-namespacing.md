# Idea Namespacing (B+C) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-idea subfolders (`outputs/ideas/<slug>/`) and a shared registry (`memory/ideas.md`) so each agent scopes its files to the correct idea and founders can manage multiple product ideas without confusion.

**Architecture:** Two new constructs: (1) `memory/ideas.md` — an index of all registered ideas with status and stage dates, managed by the Founder Agent; (2) `outputs/ideas/<slug>/` — a folder per idea where all downstream agents write their outputs. All five downstream agents gain an "idea picker" step at startup that reads the registry and scopes all reads/writes to the selected idea's folder.

**Tech Stack:** Markdown only — all changes are to AI skill prompt files and documentation. No code.

---

## File Map

| File | Action | What changes |
|------|--------|--------------|
| `memory/ideas.md` | CREATE | New ideas registry file |
| `.claude/skills/BusinessAgents/founder.md` | MODIFY | Add Ideas mode (New / List / Archive) |
| `.claude/skills/BusinessAgents/discover.md` | MODIFY | Idea picker + new output path + registry update |
| `.claude/skills/BusinessAgents/validate.md` | MODIFY | Idea picker + new output path + registry update |
| `.claude/skills/BusinessAgents/simulate_user.md` | MODIFY | Idea picker + new output paths + registry update |
| `.claude/skills/BusinessAgents/docs.md` | MODIFY | Idea picker + new output paths (docs/ + slides/) + registry update |
| `CLAUDE.md` | MODIFY | Update file structure and key rules sections |
| `outputs/ideas/private-ai-montreal-legal/` | CREATE | Migrate all existing output files |

---

### Task 1: Create memory/ideas.md

**Files:**
- Create: `memory/ideas.md`

- [ ] **Step 1: Create the file with header and format documentation**

Create `memory/ideas.md` with this exact content (it will be populated with the real existing idea in Task 7):

```markdown
# Ideas Registry
Last updated: YYYY-MM-DD

<!-- Format for each idea entry:

## <slug>
**Description:** one sentence — what it does and who it helps
**Created:** YYYY-MM-DD
**Status:** new | discovered | validated-go | validated-nogo | simulated | documented | archived
**Folder:** outputs/ideas/<slug>/
**Stages:**
- Discovery:   YYYY-MM-DD | —
- Validation:  YYYY-MM-DD (Go) | YYYY-MM-DD (No-go) | —
- Simulation:  YYYY-MM-DD | —
- Docs:        YYYY-MM-DD | —
-->
```

- [ ] **Step 2: Commit**

```bash
git add memory/ideas.md
git commit -m "feat: add ideas registry file (idea namespacing B+C)"
```

---

### Task 2: Update founder.md — Add Ideas Mode

**Files:**
- Modify: `.claude/skills/BusinessAgents/founder.md`

- [ ] **Step 1: Expand the How to Start menu to add options 4–6**

Find this exact text:
```
> 1. **Initialize** — Set everything up for the first time (takes about 5 minutes)
> 2. **Update** — Change something that has evolved (your focus shifted, new constraint, etc.)
> 3. **Review** — Show me a plain-language summary of where things stand"
```

Replace with:
```
> 1. **Initialize** — Set everything up for the first time (takes about 5 minutes)
> 2. **Update** — Change something that has evolved (your focus shifted, new constraint, etc.)
> 3. **Review** — Show me a plain-language summary of where things stand
> 4. **New idea** — Register a new product or business idea to explore
> 5. **List ideas** — See all registered ideas and their current status
> 6. **Archive idea** — Mark an idea as no longer active so it stops appearing in agent menus"
```

- [ ] **Step 2: Add the Ideas Mode section**

After the `## Review Mode` section and before `## Memory File Formats`, insert this entire block:

```markdown
## Ideas Mode

### New Idea

Ask: "What's a short name for this idea? Use lowercase with hyphens — for example: `ai-legal-assistant` or `invoice-tool`. This becomes the folder name for all its files."

Wait for the slug. Then ask: "Describe it in one sentence — what does it do and who does it help?"

Then:

1. Add an entry to `memory/ideas.md` using this exact format:

```markdown
## <slug>
**Description:** [founder's one-sentence description]
**Created:** [today's date]
**Status:** new
**Folder:** outputs/ideas/<slug>/
**Stages:**
- Discovery:   —
- Validation:  —
- Simulation:  —
- Docs:        —
```

2. Update the `Last updated:` line at the top of `memory/ideas.md` to today's date.

3. Add an entry to `memory/decisions-log.md`:
```
[YYYY-MM-DD] What changed: New idea registered — <slug>. Why: Founder wants to explore this opportunity.
```

4. Confirm: "Idea **<slug>** is registered. Your next step: run `/BusinessAgents:discover` to find and rank the real problems this idea could solve."

### List Ideas

Read `memory/ideas.md`. If it does not exist or contains no idea entries, say: "No ideas registered yet. Choose 'New idea' to register your first one."

Otherwise, display all ideas in this table format:

```
| # | Idea | Description | Status | Discovery | Validation | Simulation | Docs |
|---|------|-------------|--------|-----------|------------|------------|------|
| 1 | [slug] | [description] | [status] | [date or —] | [verdict + date or —] | [date or —] | [date or —] |
```

Then ask: "Would you like to do anything else — update memory, archive an idea, or register a new one?"

### Archive Idea

Read `memory/ideas.md`. Show only non-archived ideas by number, slug, and description. Ask: "Which idea would you like to archive?"

After the founder confirms:

1. Update that idea's `**Status:**` to `archived` in `memory/ideas.md`.
2. Update the `Last updated:` line at the top of `memory/ideas.md` to today's date.
3. Add to `memory/decisions-log.md`:
```
[YYYY-MM-DD] What changed: Idea <slug> archived. Why: [reason the founder gave].
```
4. Confirm: "Idea **<slug>** is archived. It will no longer appear in agent menus, but its files remain in `outputs/ideas/<slug>/`."
```

- [ ] **Step 3: Add two rules to Hard Rules**

In the `## Hard Rules` section at the bottom of founder.md, add after the last rule:

```
- Never create output folders directly — downstream agents create their files when they first run for an idea
- Always update the `Last updated:` date in `memory/ideas.md` whenever you modify it
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/founder.md
git commit -m "feat: add Ideas mode to Founder Agent (new/list/archive)"
```

---

### Task 3: Update discover.md — Idea picker + new output path + registry update

**Files:**
- Modify: `.claude/skills/BusinessAgents/discover.md`

- [ ] **Step 1: Add idea selection into How to Start**

Find in `## How to Start`:
```
1. Read `memory/startup-context.md` and `memory/icp.md` silently. Use the vision, constraints, and ICP to inform all your questions and research. If `startup-context.md` shows "(not yet initialized)", tell the founder: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes and will make this research much more focused." Then stop.
2. Tell the founder:
```

Replace with:
```
1. Read `memory/startup-context.md` and `memory/icp.md` silently. Use the vision, constraints, and ICP to inform all your questions and research. If `startup-context.md` shows "(not yet initialized)", tell the founder: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes and will make this research much more focused." Then stop.

2. Read `memory/ideas.md`. Select the working idea for this session:
   - If the file does not exist or has no non-archived ideas: say "No ideas registered yet. Please run `/BusinessAgents:founder` and choose 'New idea' to register one first." Then stop.
   - If exactly one non-archived idea exists: confirm — "I'll run discovery for: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple non-archived ideas exist: say "Which idea are you running discovery for?" and show a numbered list:
     ```
     1. [slug] — [description] ([status])
     2. [slug] — [description] ([status])
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.

   All output files this session will be saved to `outputs/ideas/<working-slug>/`.

3. Tell the founder:
```

(The old steps 2 and 3 become steps 3 and 4 — renumber them.)

- [ ] **Step 2: Update output path in Chat Summary**

Find in `## Output` → `### Chat Summary`:
```
Full report saved to: outputs/opportunity-discovery-[topic]-[YYYY-MM-DD].md
```

Replace with:
```
Full report saved to: outputs/ideas/[working-slug]/opportunity-discovery-[YYYY-MM-DD].md
```

- [ ] **Step 3: Update output path and remove topic name in Full Report File section**

Find:
```
### Full Report File

Save to: `outputs/opportunity-discovery-<topic>-<YYYY-MM-DD>.md`

Use a descriptive topic name (e.g., `freelance-tools`, `healthcare-admin`, `ai-education`).
```

Replace with:
```
### Full Report File

Save to: `outputs/ideas/<working-slug>/opportunity-discovery-<YYYY-MM-DD>.md`
```

- [ ] **Step 4: Add Registry Update section before Hard Rules**

Insert this entire block immediately before `## Hard Rules`:

```markdown
## Registry Update

After saving the full report file, update `memory/ideas.md`:
1. Find the entry for `<working-slug>`.
2. Set `**Status:**` to `discovered`.
3. Set the `Discovery:` stage line to today's date.
4. Update the `Last updated:` line at the top of the file to today's date.
```

- [ ] **Step 5: Add two rules to Hard Rules**

After the last rule in `## Hard Rules`, add:
```
- Always update `memory/ideas.md` after saving the report — set status to `discovered` and record the date
- Save all reports to `outputs/ideas/<working-slug>/` — never to the flat `outputs/` folder
```

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/BusinessAgents/discover.md
git commit -m "feat: add idea picker and namespaced output path to discover agent"
```

---

### Task 4: Update validate.md — Idea picker + new output path + registry update

**Files:**
- Modify: `.claude/skills/BusinessAgents/validate.md`

- [ ] **Step 1: Add idea selection into How to Start**

Find in `## How to Start`:
```
1. Read `memory/startup-context.md` and `memory/icp.md` silently. If `startup-context.md` shows "(not yet initialized)", tell the founder: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first." Then stop.
2. Ask:
```

Replace with:
```
1. Read `memory/startup-context.md` and `memory/icp.md` silently. If `startup-context.md` shows "(not yet initialized)", tell the founder: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first." Then stop.

2. Read `memory/ideas.md`. Filter to ideas with status `discovered`. Select the working idea for this session:
   - If the file does not exist or has no ideas with status `discovered`: say "No ideas are ready for validation. Run `/BusinessAgents:discover` first to generate a discovery report for an idea." Then stop.
   - If exactly one `discovered` idea exists: confirm — "I'll validate: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple `discovered` ideas exist: say "Which idea do you want to validate?" and show a numbered list (discovered ideas only):
     ```
     1. [slug] — [description]
     2. [slug] — [description]
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.

   Load the discovery report from `outputs/ideas/<working-slug>/opportunity-discovery-*.md` (most recent by date if multiple exist). All output files this session will be saved to `outputs/ideas/<working-slug>/`.

3. Ask:
```

(The old step 2 becomes step 3, step 3 becomes step 4 — renumber.)

- [ ] **Step 2: Update output path in Chat Summary**

Find in `## Output` → `### Chat Summary`:
```
Full validation plan saved to: outputs/validation-[idea-name]-[YYYY-MM-DD].md
```

Replace with:
```
Full validation plan saved to: outputs/ideas/[working-slug]/validation-[YYYY-MM-DD].md
```

- [ ] **Step 3: Update output path in Full Validation Plan File section**

Find:
```
Save to: `outputs/validation-<idea-name>-<YYYY-MM-DD>.md`

Use a descriptive idea name (e.g., `freelance-invoicing-tool`, `ai-study-assistant`).
```

Replace with:
```
Save to: `outputs/ideas/<working-slug>/validation-<YYYY-MM-DD>.md`
```

- [ ] **Step 4: Add Registry Update section before Experiment Templates**

Insert this entire block immediately before `## Experiment Templates`:

```markdown
## Registry Update

After saving the validation plan file, update `memory/ideas.md`:
1. Find the entry for `<working-slug>`.
2. If the verdict is Go: set `**Status:**` to `validated-go` and set the `Validation:` stage line to `[today's date] (Go)`.
3. If the verdict is No-go: set `**Status:**` to `validated-nogo` and set the `Validation:` stage line to `[today's date] (No-go)`.
4. Update the `Last updated:` line at the top of the file to today's date.
```

- [ ] **Step 5: Add two rules to Hard Rules**

After the last rule in `## Hard Rules`, add:
```
- Always update `memory/ideas.md` after saving the report — set status to `validated-go` or `validated-nogo` and record the date
- Save all reports to `outputs/ideas/<working-slug>/` — never to the flat `outputs/` folder
```

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/BusinessAgents/validate.md
git commit -m "feat: add idea picker and namespaced output path to validate agent"
```

---

### Task 5: Update simulate_user.md — Idea picker + new output paths + registry update

**Files:**
- Modify: `.claude/skills/BusinessAgents/simulate_user.md`

- [ ] **Step 1: Replace How to Start steps 1–3 with idea-aware version**

Find this block in `## How to Start`:
```
1. Read the following files silently:
   - `memory/startup-context.md`
   - `memory/icp.md`
   - The most recent file matching `outputs/validation-*.md` (by date — this takes priority)
   - If no validation report exists, read the most recent `outputs/opportunity-discovery-*.md` instead

2. If `memory/startup-context.md` shows "(not yet initialized)", stop and say: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes." Then stop.

3. Extract from what you read:
```

Replace with:
```
1. Read `memory/startup-context.md` and `memory/icp.md` silently. If `startup-context.md` shows "(not yet initialized)", stop and say: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes." Then stop.

2. Read `memory/ideas.md`. Filter to ideas with status `validated-go`. Select the working idea for this session:
   - If the file does not exist or has no ideas with status `validated-go`: say "No ideas are ready for simulation. Run `/BusinessAgents:validate` first and get a Go verdict." Then stop.
   - If exactly one `validated-go` idea exists: confirm — "I'll simulate end users for: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple `validated-go` ideas exist: say "Which idea do you want to simulate?" and show a numbered list (`validated-go` ideas only):
     ```
     1. [slug] — [description]
     2. [slug] — [description]
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.

   Load files from `outputs/ideas/<working-slug>/`: the most recent `validation-*.md` (takes priority as solution source); if none exists, the most recent `opportunity-discovery-*.md` instead. All output files this session will be saved to `outputs/ideas/<working-slug>/`.

3. Extract from what you read:
```

- [ ] **Step 2: Update full report output path**

Find in `## Output` → `### Full Report`:
```
Save to: `outputs/simulation-<persona-role>-<YYYY-MM-DD>.md`
```

Replace with:
```
Save to: `outputs/ideas/<working-slug>/simulation-<persona-role>-<YYYY-MM-DD>.md`
```

- [ ] **Step 3: Update one-pager output path**

Find in `### User-Facing One-Pager`:
```
Save to: `outputs/simulation-<persona-role>-onepager-<YYYY-MM-DD>.md`
```

Replace with:
```
Save to: `outputs/ideas/<working-slug>/simulation-<persona-role>-onepager-<YYYY-MM-DD>.md`
```

- [ ] **Step 4: Update Chat Summary file references**

Find in `## Chat Summary`:
```
Full report saved to: outputs/simulation-<persona>-<YYYY-MM-DD>.md
One-pager saved to: outputs/simulation-<persona>-onepager-<YYYY-MM-DD>.md
```

Replace with:
```
Full report saved to: outputs/ideas/<working-slug>/simulation-<persona>-<YYYY-MM-DD>.md
One-pager saved to: outputs/ideas/<working-slug>/simulation-<persona>-onepager-<YYYY-MM-DD>.md
```

- [ ] **Step 5: Add Registry Update section before Hard Rules**

Insert this entire block immediately before `## Hard Rules`:

```markdown
## Registry Update

After saving both output files, update `memory/ideas.md`:
1. Find the entry for `<working-slug>`.
2. Set `**Status:**` to `simulated`.
3. Set the `Simulation:` stage line to today's date.
4. Update the `Last updated:` line at the top of the file to today's date.
```

- [ ] **Step 6: Add two rules to Hard Rules**

After the last rule in `## Hard Rules`, add:
```
- Always update `memory/ideas.md` after saving both output files — set status to `simulated` and record the date
- Save all output files to `outputs/ideas/<working-slug>/` — never to the flat `outputs/` folder
```

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/BusinessAgents/simulate_user.md
git commit -m "feat: add idea picker and namespaced output paths to simulate_user agent"
```

---

### Task 6: Update docs.md — Idea picker + new output paths + registry update

**Files:**
- Modify: `.claude/skills/BusinessAgents/docs.md`

- [ ] **Step 1: Replace How to Start steps 1–4 with idea-aware version**

Find this block in `## How to Start`:
```
1. Read all files in `memory/` silently: `startup-context.md`, `icp.md`, `decisions-log.md`.
2. Read all `.md` files in `outputs/` silently (discovery and validation reports if they exist).
3. If `memory/startup-context.md` shows "(not yet initialized)", tell the founder: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes." Then stop.
4. Ask:
```

Replace with:
```
1. Read all files in `memory/` silently: `startup-context.md`, `icp.md`, `decisions-log.md`.
2. If `memory/startup-context.md` shows "(not yet initialized)", tell the founder: "It looks like your startup context hasn't been set up yet. Please run `/BusinessAgents:founder` first — it only takes 5 minutes." Then stop.
3. Read `memory/ideas.md`. Select the working idea for this session:
   - If the file does not exist or has no non-archived ideas: say "No ideas registered yet. Please run `/BusinessAgents:founder` and choose 'New idea' first." Then stop.
   - If exactly one non-archived idea exists: confirm — "I'll generate documents for: **[slug]** — [description]. Is that right?" Wait for confirmation.
   - If multiple non-archived ideas exist: say "Which idea do you want to generate documents for?" and show a numbered list:
     ```
     1. [slug] — [description] ([status])
     2. [slug] — [description] ([status])
     ```
     Wait for the founder's choice. Store the selected slug as `<working-slug>` for this session.

   Read all `.md` files in `outputs/ideas/<working-slug>/` silently (discovery, validation, and simulation reports if they exist). All output files this session will be saved to `outputs/ideas/<working-slug>/docs/` (documents) and `outputs/ideas/<working-slug>/slides/` (presentations).

4. Ask:
```

- [ ] **Step 2: Update the document save path in Document Generation section**

Find in `## Document Generation`:
```
Show the document in chat first, then save it to `outputs/docs/<document-name>-<YYYY-MM-DD>.md`.
```

Replace with:
```
Show the document in chat first, then save it to `outputs/ideas/<working-slug>/docs/<document-name>-<YYYY-MM-DD>.md`.
```

- [ ] **Step 3: Update the User Impact Journey Map paths**

Find the simulation report loading instruction in `### User Impact Journey Map`:
```
Before generating, read the most recent file matching `outputs/simulation-*-<YYYY-MM-DD>.md` (by date — do NOT read the onepager file, which contains `-onepager-` in the name).
```

Replace with:
```
Before generating, read the most recent file matching `outputs/ideas/<working-slug>/simulation-*-<YYYY-MM-DD>.md` (by date — do NOT read the onepager file, which contains `-onepager-` in the name).
```

Find the save path in User Impact Journey Map:
```
Save to: `outputs/docs/user-impact-journey-map-<YYYY-MM-DD>.html`
```

Replace with:
```
Save to: `outputs/ideas/<working-slug>/docs/user-impact-journey-map-<YYYY-MM-DD>.html`
```

Find the confirmation message in User Impact Journey Map:
```
Tell the founder: "Journey map saved to `outputs/docs/user-impact-journey-map-<YYYY-MM-DD>.html`. Open it in any browser and use arrow keys to navigate. Share this during user interviews or demos."
```

Replace with:
```
Tell the founder: "Journey map saved to `outputs/ideas/<working-slug>/docs/user-impact-journey-map-<YYYY-MM-DD>.html`. Open it in any browser and use arrow keys to navigate. Share this during user interviews or demos."
```

- [ ] **Step 4: Update the slides save path and confirmation message**

Find in `## Slide Generation` (after the 4 questions):
```
Save to: `outputs/slides/<presentation-name>-<YYYY-MM-DD>.html`
```

Replace with:
```
Save to: `outputs/ideas/<working-slug>/slides/<presentation-name>-<YYYY-MM-DD>.html`
```

Find the slides confirmation message:
```
Tell the founder: "Slides saved to `outputs/slides/[filename].html`. Open that file in any browser to present. Use arrow keys or the on-screen buttons to navigate. When you have more information, run `/BusinessAgents:docs` again to update it."
```

Replace with:
```
Tell the founder: "Slides saved to `outputs/ideas/<working-slug>/slides/[filename].html`. Open that file in any browser to present. Use arrow keys or the on-screen buttons to navigate. When you have more information, run `/BusinessAgents:docs` again to update it."
```

- [ ] **Step 5: Add Registry Update section before Hard Rules**

Insert this entire block immediately before `## Hard Rules`:

```markdown
## Registry Update

After saving any output file, update `memory/ideas.md`:
1. Find the entry for `<working-slug>`.
2. Set `**Status:**` to `documented` (only if not already `documented` — do not downgrade a later status).
3. Set the `Docs:` stage line to today's date (only if currently `—`).
4. Update the `Last updated:` line at the top of the file to today's date.
```

- [ ] **Step 6: Add two rules to Hard Rules**

After the last rule in `## Hard Rules`, add:
```
- Always update `memory/ideas.md` after saving any output file — set status to `documented` and record the date
- Save documents to `outputs/ideas/<working-slug>/docs/` and slides to `outputs/ideas/<working-slug>/slides/` — never to flat `outputs/` paths
```

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/BusinessAgents/docs.md
git commit -m "feat: add idea picker and namespaced output paths to docs agent"
```

---

### Task 7: Migrate existing files and populate memory/ideas.md

**Files:**
- Create: `outputs/ideas/private-ai-montreal-legal/` (folder + moved files)
- Modify: `memory/ideas.md`

- [ ] **Step 1: Create the idea folder and move all existing output files**

```bash
mkdir -p outputs/ideas/private-ai-montreal-legal
mv outputs/opportunity-discovery-private-ai-montreal-legal-engineering-2026-04-23.md \
   outputs/ideas/private-ai-montreal-legal/opportunity-discovery-2026-04-23.md
mv outputs/validation-private-ai-montreal-law-firms-2026-04-24.md \
   outputs/ideas/private-ai-montreal-legal/validation-2026-04-24.md
mv outputs/simulation-paralegal-lawyer-2026-04-24.md \
   outputs/ideas/private-ai-montreal-legal/simulation-paralegal-lawyer-2026-04-24.md
mv outputs/simulation-paralegal-lawyer-onepager-2026-04-24.md \
   outputs/ideas/private-ai-montreal-legal/simulation-paralegal-lawyer-onepager-2026-04-24.md
```

- [ ] **Step 2: Populate memory/ideas.md with the existing idea**

Replace the full contents of `memory/ideas.md` with:

```markdown
# Ideas Registry
Last updated: 2026-04-24

## private-ai-montreal-legal
**Description:** Private AI assistant for Montreal law firms handling document review and compliance
**Created:** 2026-04-23
**Status:** simulated
**Folder:** outputs/ideas/private-ai-montreal-legal/
**Stages:**
- Discovery:   2026-04-23
- Validation:  2026-04-24 (Go)
- Simulation:  2026-04-24
- Docs:        —
```

- [ ] **Step 3: Verify the folder structure looks correct**

```bash
find outputs/ideas -type f | sort
```

Expected output:
```
outputs/ideas/private-ai-montreal-legal/opportunity-discovery-2026-04-23.md
outputs/ideas/private-ai-montreal-legal/simulation-paralegal-lawyer-2026-04-24.md
outputs/ideas/private-ai-montreal-legal/simulation-paralegal-lawyer-onepager-2026-04-24.md
outputs/ideas/private-ai-montreal-legal/validation-2026-04-24.md
```

- [ ] **Step 4: Commit**

```bash
git add memory/ideas.md outputs/ideas/
git commit -m "feat: migrate existing outputs to ideas subfolder; populate ideas registry"
```

---

### Task 8: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Replace the Memory & Output Structure section**

Find:
```
## Memory & Output Structure

```
outputs/
  opportunity-discovery-*.md   ← discovery reports
  validation-*.md              ← validation plans with Go/No-go verdicts
  simulation-*.md              ← end user simulation reports
  simulation-*-onepager-*.md   ← plain-language user-facing summaries
  docs/
    *.md                       ← business documents
    *.html                     ← user impact journey map slides
  slides/
    *.html                     ← pitch decks and presentations
```
```

Replace the outputs block with:
```
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
```

- [ ] **Step 2: Add two rules to the Key Rules section**

Find in `## Key Rules Across All Agents`:
```
- `/BusinessAgents:founder` must run first — all other agents stop and redirect if memory is uninitialized.
- Each agent reads memory and prior outputs before asking questions — you never explain your context twice.
```

Add after these two lines:
```
- Register every new product idea with `/BusinessAgents:founder` → "New idea" before running any downstream agent — all agents require an entry in `memory/ideas.md`.
- Each downstream agent asks "which idea?" at startup and scopes all file reads and writes to `outputs/ideas/<slug>/` — files from different ideas are never mixed.
```

- [ ] **Step 3: Update the re-run guidance paragraph**

Find:
```
You can re-run any agent at any point:
- Re-run `/BusinessAgents:founder` (Update mode) whenever your constraints or target customer changes.
- Re-run `/BusinessAgents:discover` to explore a different problem space.
- Re-run `/BusinessAgents:validate` on a new problem after a No-go verdict.
- Re-run `/BusinessAgents:docs` to update documents as new information comes in.
```

Replace with:
```
You can re-run any agent at any point:
- Re-run `/BusinessAgents:founder` (Update mode) whenever your constraints or target customer changes.
- Re-run `/BusinessAgents:founder` → "New idea" to register a second product idea and explore it in parallel.
- Re-run `/BusinessAgents:discover` to explore a different problem space for any registered idea.
- Re-run `/BusinessAgents:validate` on a new problem after a No-go verdict.
- Re-run `/BusinessAgents:docs` to update documents as new information comes in.

**Working on multiple ideas:** Register each product idea separately with `/BusinessAgents:founder` → "New idea". Each downstream agent will show a numbered menu so you can pick which idea to work on for that session. All files stay scoped to their idea's folder in `outputs/ideas/`.
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for idea namespacing (B+C)"
```

---

## Self-Review

**Spec coverage:**
- ✅ B (idea subfolders) — Tasks 3, 4, 5, 6, 7
- ✅ C (idea registry) — Tasks 1, 2
- ✅ Filtered menus per agent: discover (all non-archived), validate (discovered only), simulate (validated-go only), docs (all non-archived) — Tasks 3, 4, 5, 6
- ✅ Each agent updates registry after saving output — Tasks 3, 4, 5, 6
- ✅ Founder Agent manages New / List / Archive — Task 2
- ✅ Migration of existing files — Task 7
- ✅ CLAUDE.md updated — Task 8

**Status values used consistently across all files:** `new | discovered | validated-go | validated-nogo | simulated | documented | archived`

**`<working-slug>` used consistently** as the session variable name in all four downstream agents.
