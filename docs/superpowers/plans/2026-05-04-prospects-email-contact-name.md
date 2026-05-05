# Prospects: Automatic `email_contact_name` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add automatic `email_contact_name` resolution to the prospects skill so every scraped lead has a ready-to-use salutation name derived from the company website, the email address, or the decision_maker — with company name as fallback.

**Architecture:** Single file change to `.claude/skills/BusinessAgents/prospects.md`. Three edits: (1) one sentence added to the enrichment step referencing a new sub-section, (2) a new `## Contact Name Resolution` section inserted after enrichment, (3) `email_contact_name` column added to both CSV headers and MD table. No code files change.

**Tech Stack:** Markdown skill file; scrapling MCP (`bulk_get`, `get`) for sub-page fetching.

---

## File Map

| File | Change |
|---|---|
| `.claude/skills/BusinessAgents/prospects.md` | Modify enrichment step (line 134), insert Contact Name Resolution section, update CSV headers (line 194), update MD table (line 181) |

---

### Task 1: Add Contact Name Resolution trigger to the enrichment step

**Files:**
- Modify: `.claude/skills/BusinessAgents/prospects.md:134`

- [ ] **Step 1: Open the file and locate the enrichment step closing line**

  Find this exact line (currently line 134):
  ```
  If enrichment is declined, leave email, employees, and decision_maker blank — do not guess.
  ```

- [ ] **Step 2: Append the trigger sentence immediately after that line**

  Replace that line with:
  ```
  If enrichment is declined, leave email, employees, and decision_maker blank — do not guess.

  After collecting enrichment data for all prospects, run the **Contact Name Resolution** step below for each prospect.
  ```

- [ ] **Step 3: Verify the change**

  Run:
  ```bash
  grep -n "Contact Name Resolution" .claude/skills/BusinessAgents/prospects.md
  ```
  Expected output: two matches — one in the enrichment step (around line 136) and one as a section heading (added in Task 2).

- [ ] **Step 4: Commit**

  ```bash
  git add .claude/skills/BusinessAgents/prospects.md
  git commit -m "feat(prospects): add Contact Name Resolution trigger in enrichment step"
  ```

---

### Task 2: Insert the Contact Name Resolution section

**Files:**
- Modify: `.claude/skills/BusinessAgents/prospects.md` — insert new section between enrichment step and `## Filtering by Size`

- [ ] **Step 1: Locate the insertion point**

  Find this exact line (the section that currently follows enrichment):
  ```
  ## Filtering by Size
  ```

- [ ] **Step 2: Insert the full Contact Name Resolution section immediately before it**

  The content to insert (place a blank line between this block and `## Filtering by Size`):

  ````markdown
  ## Contact Name Resolution

  Run this for each prospect after enrichment completes.

  **Step 1 — decision_maker shortcut**
  If `decision_maker` is non-empty: set `email_contact_name = decision_maker`. Done — skip the remaining steps for this prospect.

  **Step 2 — Find About/Team page via homepage nav (primary)**
  Use the homepage content already fetched during enrichment (do not re-fetch).
  Look for a nav link whose anchor text contains any of:
  `about`, `team`, `our team`, `attorneys`, `lawyers`, `people`, `équipe`, `avocats`, `notre équipe`
  → Fetch that URL.

  **Step 3 — Fixed-list fallback**
  If Step 2 finds no matching nav link, or the fetched page returns an error:
  Prepend the company base URL to each path and `bulk_get` in parallel:
  `/about` `/team` `/our-team` `/attorneys` `/lawyers` `/equipe` `/notre-equipe` `/people`
  Use the first path that returns content.
  If none return content → go to Step 6.

  **Step 4 — Extract person names**
  From the fetched page, extract all full person names.
  Prioritise names appearing near professional titles: Partner, Avocat, Avocate, Lawyer, Associate, Notaire, Counsel, Director, Associé, Associée.
  If no names can be extracted → go to Step 6.

  **Step 5 — Semantic email match (moderate)**
  a. Strip the local part of the email (everything before `@`).
  b. Skip matching if the local part is a generic word: `info`, `contact`, `reception`, `accueil`, `office`, `admin`, `attorney`, `avocats`, `administration`, `mail`, `questioncondo`.
  c. Test the local part against each extracted name in this order:
     - **Dot-separated exact:** `mehdi.tenouri` → matches "Mehdi Tenouri"
     - **Initial + last name:** `ms` → first character = first-name initial, remaining characters = start of last name → "Michel Savonitto"
     - **Last name only:** `fallali` → matches last name of any extracted name (case-insensitive, accent-insensitive)
  d. Use the first confident match found.
  e. Set `email_contact_name` = the full name as written on the page (not derived from the email string).

  **Step 6 — Fallback**
  `email_contact_name` = company name.

  ````

- [ ] **Step 3: Verify the section appears correctly**

  Run:
  ```bash
  grep -n "## Contact Name Resolution\|## Filtering by Size\|## Enrichment" .claude/skills/BusinessAgents/prospects.md
  ```
  Expected output (line numbers will shift):
  ```
  114:## Enrichment Step (find emails, employee counts, decision-makers)
  138:## Contact Name Resolution
  178:## Filtering by Size
  ```
  Confirm Contact Name Resolution appears between Enrichment and Filtering.

- [ ] **Step 4: Commit**

  ```bash
  git add .claude/skills/BusinessAgents/prospects.md
  git commit -m "feat(prospects): add Contact Name Resolution section with nav-follow + semantic email match"
  ```

---

### Task 3: Update output format — CSV headers and MD table

**Files:**
- Modify: `.claude/skills/BusinessAgents/prospects.md` — two locations in the Output section

- [ ] **Step 1: Update the CSV headers line**

  Find this exact line:
  ```
  Headers: `name,phone,email,address,website,employees,source,decision_maker`
  ```

  Replace with:
  ```
  Headers: `name,phone,email,address,website,employees,source,decision_maker,email_contact_name`
  ```

- [ ] **Step 2: Update the markdown table header**

  Find this exact block:
  ```
  | # | Company | Phone | Email | Address | Website | Employees | Decision Maker |
  |---|---------|-------|-------|---------|---------|-----------|----------------|
  | 1 | ...     | ...   | ...   | ...     | ...     | ...       | ...            |
  ```

  Replace with:
  ```
  | # | Company | Phone | Email | Address | Website | Employees | Decision Maker | Email Contact Name |
  |---|---------|-------|-------|---------|---------|-----------|----------------|--------------------|
  | 1 | ...     | ...   | ...   | ...     | ...     | ...       | ...            | ...                |
  ```

- [ ] **Step 3: Verify both changes**

  Run:
  ```bash
  grep -n "email_contact_name\|Email Contact Name" .claude/skills/BusinessAgents/prospects.md
  ```
  Expected: two matches — one in the CSV headers line, one in the MD table header.

- [ ] **Step 4: Commit**

  ```bash
  git add .claude/skills/BusinessAgents/prospects.md
  git commit -m "feat(prospects): add email_contact_name column to CSV and MD output format"
  ```

---

### Task 4: Final verification

- [ ] **Step 1: Confirm overall structure of the modified skill**

  Run:
  ```bash
  grep -n "^## " .claude/skills/BusinessAgents/prospects.md
  ```
  Expected output:
  ```
  ## How to Start
  ## Questions to Ask
  ## How to Fetch and Extract
  ## Enrichment Step (find emails, employee counts, decision-makers)
  ## Contact Name Resolution
  ## Filtering by Size
  ## Output
  ## Hard Rules
  ```

- [ ] **Step 2: Confirm the Hard Rules section is untouched**

  Run:
  ```bash
  grep -n "Hard Rules" .claude/skills/BusinessAgents/prospects.md
  ```
  Expected: exactly one match on the `## Hard Rules` heading line.

- [ ] **Step 3: Read the full file and do a final visual check**

  Read `.claude/skills/BusinessAgents/prospects.md` from top to bottom. Confirm:
  - Enrichment step ends with the trigger sentence referencing Contact Name Resolution
  - Contact Name Resolution section has all 6 steps (shortcut, nav, fallback, extract, match, default)
  - CSV headers include `email_contact_name` as the last field
  - MD table includes `Email Contact Name` as the last column
  - No other content was accidentally modified
