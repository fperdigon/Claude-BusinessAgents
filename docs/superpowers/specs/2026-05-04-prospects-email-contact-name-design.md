# Design: Automatic `email_contact_name` in Prospects Skill

**Date:** 2026-05-04
**Skill:** `BusinessAgents:prospects`
**Status:** Approved

---

## Problem

The prospects skill produces a `decision_maker` field (title-driven: who has buying authority) but no ready-to-use salutation name for email outreach. Users currently have to derive this manually by inspecting the email address and cross-referencing the website. The CSV export needed a separate `email_contact_name` column that answers: *"What name do I put in the greeting of my email?"*

---

## Goals

- Automatically populate `email_contact_name` for every prospect during the enrichment step.
- Reuse work already done (decision_maker extraction, website visits) — no extra user-facing questions.
- Provide the best available name: person name from the website > semantic email match > company name fallback.
- Add `email_contact_name` as the last column in both the `.csv` and `.md` outputs.

---

## Non-Goals

- Does not replace or change the `decision_maker` field.
- Does not run when the user declines enrichment (no website visits = no name extraction).
- Does not attempt AI-generated guesses — every name must come from a fetched page.

---

## Architecture

### Change 1 — Enrichment step (one-line addition)

At the end of the existing enrichment section, add:

> "After collecting enrichment data for all prospects, run the Contact Name Resolution step below for each prospect."

No other changes to the enrichment section.

### Change 2 — New `## Contact Name Resolution` sub-section

Placed immediately after the enrichment section. Executed once per prospect after enrichment completes.

### Change 3 — Output format

Add `email_contact_name` as the final column in:
- CSV headers: `name,phone,email,address,website,employees,source,decision_maker,email_contact_name`
- Markdown table: add `Email Contact Name` column at the end

---

## Contact Name Resolution Algorithm

```
For each prospect:

Step 1 — decision_maker shortcut
  If decision_maker is non-empty:
    email_contact_name = decision_maker
    → Done. Skip remaining steps.

Step 2 — Navigate to About/Team page (primary)
  Use the homepage content already fetched during enrichment (no re-fetch).
  Find a nav link whose anchor text contains any of:
    "about", "team", "our team", "attorneys", "lawyers", "people",
    "équipe", "avocats", "notre équipe"
  → Fetch that URL.

Step 3 — Fixed-list fallback
  If Step 2 finds no nav link, or the fetched page returns an error:
  Prepend the company base URL (e.g. https://firm.com) to each path and
  bulk_get in parallel — use the first that returns content:
    /about  /team  /our-team  /attorneys  /lawyers
    /equipe  /notre-equipe  /people
  If none return content → go to Step 6 (company name fallback).

Step 4 — Extract person names
  From the fetched page, extract all full person names.
  Prioritise names appearing near professional titles:
    Partner, Avocat, Avocate, Lawyer, Associate, Notaire,
    Counsel, Director, Associé, Associée
  If no names can be extracted → go to Step 6 (company name fallback).

Step 5 — Semantic email match (moderate)
  a. Strip the email local part (everything before @).
  b. Skip matching if local is a generic word:
       info, contact, reception, accueil, office, admin,
       attorney, avocats, administration, mail, questioncondo
  c. Test against each extracted name using these rules in order:
       i.  Dot-separated exact: "mehdi.tenouri" → "Mehdi Tenouri"
       ii. Initial + last name: "ms" → first char = first-name initial,
           remaining chars = start of last name → "Michel Savonitto"
      iii. Last name only: "fallali" → matches last name of any extracted
           name (case-insensitive, accent-insensitive)
  d. Use the first confident match found.
  e. email_contact_name = full extracted name from the page (not the
     email-derived form — always use the name as written on the page).

Step 6 — Fallback
  email_contact_name = company name
```

---

## Decision Log

| Decision | Choice | Reason |
|---|---|---|
| Where in the flow | Inside existing enrichment step | Agent is already visiting the website; no extra pass needed |
| Semantic matching level | Moderate (dot-separated + initial+last name + last name only) | Catches standard professional email naming patterns; avoids wrong guesses on opaque locals |
| Relationship to `decision_maker` | Draw from it first; only run email match if empty | Reuses work already done; decision_maker is already a reliable name when present |
| Sub-page discovery | Follow homepage nav to find actual URL | More accurate than a fixed list; finds pages at non-standard paths |
| Fallback when nav fails | Try fixed list (`/about`, `/team`, etc.) before giving up | Belt-and-suspenders; silent — no noise in output if both fail |
| Output format | Add `email_contact_name` as last column in CSV and MD | Additive change; no existing consumers broken |

---

## Files to Modify

| File | Change |
|---|---|
| `.claude/skills/BusinessAgents/prospects.md` | Add one sentence to enrichment step + new `## Contact Name Resolution` section + update CSV headers + update MD table headers |

No other files change.
