# Directory Sources Reference

## Extraction Type Rules

| Page type | `extraction_type` | Reason |
|---|---|---|
| Directory listing (Yellow Pages, Google Maps) | `"markdown"` | Needed to extract website URLs from redirect `<a>` tags |
| Enrichment (company homepages, contact/team pages) | `"text"` | 50–70% smaller; sufficient for emails, names, counts |
| Cloudflare decode re-fetch | `"markdown"` | Needed to expose hex-encoded `mailto:` links |

## Source Priority

Both industries use the same order: **yellowpages.ca → Google Maps**. Yelp.ca is CAPTCHA-blocked — skip it. Run each industry separately, then combine and deduplicate by company name. Move to the next source if a source returns no listings.

## Yellow Pages

**URL pattern:**
```
https://www.yellowpages.ca/search/si/{PAGE}/{QUERY}/{CITY+PROVINCE}
```

Example: `https://www.yellowpages.ca/search/si/1/law+firms/Montreal+QC`

**CSS selector:** `div.listing.listing--bottomcta:not(.placementText)` — targets business listing cards, excludes banner ads (~75% size reduction).

**Fallback:** If the CSS selector returns 0 results (site redesigned), re-fetch without `css_selector` and parse the full page markdown.

**Website URL decoding:** Yellow Pages wraps company websites in redirect links: `/gourl/...?redirect=<encoded-url>`. Decode the `redirect=` query parameter value to get the real URL.

**Pagination:** Fetch pages 1–5 via `bulk_get`. Stop when a page returns fewer than 5 listings or no new companies.

## Google Maps (fallback)

**URL pattern:**
```
https://www.google.com/maps/search/{QUERY}+{CITY+PROVINCE}
```

Use `stealthy_fetch` with `extraction_type: "markdown"` and `network_idle: true`.

## Website Recovery (for prospects with no website)

Work through no-website companies **sequentially** (Google rate-limits parallel requests).

**City selection:**
- If the company has an address: extract the city name from it
- If no address: use the city from Question 1

Always include the city in search URLs for disambiguation.

**Step 1 — Google Maps:**
```
https://www.google.com/maps/search/{name}+{city}+{province}
```
Use `stealthy_fetch` with `extraction_type: "markdown"` and `network_idle: true`. Look for: `[Website](url)`, `[Visiter le site Web](url)`, or `[Site Web](url)`. Record the first non-google.com URL.

**Step 2 — Google Search fallback:**
```
https://www.google.com/search?q="{name}"+{city}+{province}
```
Use `stealthy_fetch` with `extraction_type: "markdown"`. Take the first organic result URL that is **not** google.com, yellowpages.ca, yelp.ca, or a known directory domain.

## Fields to Extract Per Listing

| Field | Where to look |
|---|---|
| Company name | Heading or bold text for each listing |
| Phone | Any phone number near the company name |
| Email | Any `@` address or `mailto:` link |
| Address | Street address under or near the listing |
| Website | Any URL or "website" link |
| Employee count | "X employees", "staff of X", "X-person firm", ranges like "1–10" |
| Source | Which directory this came from |
