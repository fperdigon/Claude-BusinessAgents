# Contact & Email Discovery Reference

## Enrichment: What to Look For

**Email addresses** (highest priority):
- Any `@` email address visible on the page
- `mailto:` links (most reliable)
- Prefer named person's email over generic (e.g., `jsmith@firm.com` > `info@firm.com`), but record both

**Employee count:**
- "Our team of X", "X lawyers", "X engineers", "X professionals", "X staff"
- Size indicators on About or Our Firm pages

**Decision-maker name and title:**
- Managing Partner, Senior Partner, Founding Partner, CTO, CEO, President, Director of Technology
- Check About, Team, Our People, and Leadership pages

## Deep Email Search Paths

Prepend the company's base URL to each. Fetch **all paths at once** via `bulk_get` with `extraction_type: "text"` — do not stop early.

```
/contact
/contact-us
/nous-joindre
/contactez-nous
/coordonnees
/coordonnees.html
/joindre
/about
/about-us
/equipe
/notre-equipe
/team
/our-team
/attorneys
/lawyers
/people
```

Scan every returned page for a real email address (contains `@`, is not the `[email protected]` placeholder).

If any page returns the `[email protected]` placeholder: re-fetch that URL with `extraction_type: "markdown"` to expose the Cloudflare hex string, then decode with `scripts/decode_cf_email.py`.

If no path yields an email, mark the company as "contact form only."

## Cloudflare Email Obfuscation

Many websites (especially Quebec law firms) use Cloudflare's email obfuscation. In page Markdown you'll see:

```
[[email protected]](/cdn-cgi/l/email-protection#d1bcbbff...)
```

The hex string after `#` encodes the real email. Decode with `scripts/decode_cf_email.py` or `mcp__ide__executeCode`.

If `mcp__ide__executeCode` is unavailable, mark affected emails as `"CF-obfuscated — decode manually"` and continue.

## Contact Name Resolution: Nav Link Detection

Look for nav links whose anchor text contains any of:
```
about, team, our team, attorneys, lawyers, people, équipe, avocats, notre équipe
```

Fetch the matching URL with `extraction_type: "text"`.

## Contact Name Resolution: Title Keywords

Prioritize names appearing near these professional titles:
```
Partner, Avocat, Avocate, Lawyer, Associate, Notaire, Counsel, Director, Associé, Associée
```
