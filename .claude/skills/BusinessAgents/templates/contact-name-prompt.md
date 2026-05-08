# Contact Name Resolution — Sonnet Sub-Agent Prompt

Dispatch this as a single Sonnet sub-agent call after completing Contact Name Resolution Steps 1–4 for all prospects.

## Prompt

```
For each prospect below, determine `email_contact_name` by semantic email matching.

Rules:
a. Strip the local part of the email (everything before `@`).
b. Skip matching if the local part is a generic word: info, contact, reception, accueil, office, admin, attorney, avocats, administration, mail, questioncondo → return null.
c. Test the local part against extracted_names in this order:
   1. Dot-separated exact: "mehdi.tenouri" → matches "Mehdi Tenouri"
   2. Initial + last name: "ms" → first char = first-name initial, rest = start of last name → "Michel Savonitto"
   3. Last name only: "fallali" → case-insensitive, accent-insensitive match against last name of any extracted name
d. Return the full name exactly as written in extracted_names. If no confident match: return null.

Prospects:
{{prospects-json}}

Return ONLY a JSON array: [{"prospect": "...", "email_contact_name": "matched name or null"}, ...]
```

## Input Format

`{{prospects-json}}` is a JSON array:
```json
[
  {"prospect": "Company Name", "email": "jsmith@firm.com", "extracted_names": ["John Smith", "Jane Doe"]},
  ...
]
```

## Usage

Collect every prospect that has both an email address and extracted names from Step 4. Dispatch one Sonnet sub-agent with all prospects in a single call. Apply returned values: if `email_contact_name` is non-null, use it; if null, fall through to Step 6 (fallback = company name).
