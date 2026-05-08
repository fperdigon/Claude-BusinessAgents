# Infographic Layout Triggers

## How to Inject an Infographic Layout Into a Slide

When a slide gets a non-plain layout key:
1. Look up the layout key in `<infographic-map>` → get the filename (e.g., `infographic-stats-grid.html`)
2. Read the HTML partial file from `<visual-theme-folder>/<filename>`
3. The file is an HTML partial — drop its full content into the `.card-body` div, replacing the default headline + bullets structure for that slide
4. Populate all template slots in the partial with the actual slide content derived from memory and outputs
5. **Suppress the background SVG on this slide** — on any card that has an infographic, omit the `<svg class="card-bg">` tag entirely. Keep the `<div class="card-scrim"></div>` so the card still has its base navy colour. The infographic is the visual; the SVG pattern would fight it.
6. If `<has-visual-theme>` = false: skip steps 1–4 and use plain text layout for all slides

## Layout Trigger Rules by Template

### Template 1 — Problem Awareness

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| "The real cost" | 2+ metrics available | `results` |
| "The real cost" | improvement % available | `improvements` |
| "The real cost" | neither | plain |
| "Why it keeps happening" | always | plain |
| "Old way vs right way" | always | `comparison` |
| "What changes when you fix it" | 3+ distinct outcomes | `use_cases` |
| "What changes when you fix it" | fewer outcomes | plain |
| Deeper evidence (slides 6–8) | pipeline or funnel data | `pipeline` |
| Deeper evidence (slides 6–8) | feature comparison | `versus` |
| Deeper evidence (slides 6–8) | neither | plain |
| CTA | always | plain |

### Template 2 — Before/After Journey

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| Setup | always | plain |
| Before journey phases | always | plain |
| Turning point | always | `comparison` |
| After journey phases | always | plain |
| Summary benefits | time/error/quality metrics present | `results` or `improvements` |
| Summary benefits | no metrics | plain |
| CTA | always | plain |

### Template 3 — Tips & Education

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| Tip slide | tip describes 3–5 ordered steps | `how_it_works` |
| Tip slide | tip compares two approaches | `versus` |
| Tip slide | tip contains 3+ statistics | `results` |
| Tip slide | tip lists 5–6 distinct capabilities | `capabilities` |
| Tip slide | tip has one central idea + 4–6 branches | `use_cases` |
| Tip slide | none of the above | plain |
| "Most important" tip | always | plain |
| CTA | always | plain |

### Template 4 — Your Story

| Slide | Trigger condition | Layout key |
|---|---|---|
| Hook | always | plain |
| Context | always | plain |
| Breaking point | always | plain |
| Journey sequence | 3+ dated or ordered events | `journey` |
| "What changed" | always | `comparison` |
| Lessons for reader | 4–6 distinct lessons | `capabilities` |
| Lessons for reader | fewer than 4 | plain |
| CTA | always | plain |

## Quote / Testimonial Layout

Only used when an actual quote exists in interview reports (`outputs/ideas/<working-slug>/interview-insights-*.md`) or the founder provides one explicitly during the session. Never fabricated. When triggered, replaces a content slide. Always uses style D (contained box + small SVG quote icon).

## Visual Density Rules

A slide has three fixed elements (kicker, headline, bottom bar) plus the infographic. The infographic must not crowd them.

- **Background off on infographic slides** — infographic + background SVG together is too much. Plain slides get the background; infographic slides get a clean navy card. The scrim stays for the base colour.
- **Keep the headline short** — when a slide uses an infographic, cap the headline at 6 words. The infographic carries the detail; the headline frames it.
- **Cap data points** — enforce these maximums regardless of how much data is available: stats grid ≤ 4 stats, progress bars ≤ 4 bars, process steps ≤ 4 steps, before/after ≤ 3 items per column, comparison table ≤ 5 rows, icon grid = exactly 6 cells, timeline ≤ 4 events, hub & spoke ≤ 6 nodes, funnel ≤ 5 stages. Pick the most impactful subset — do not squeeze in extras.
- **Labels stay short** — every label, stat description, or step label must be ≤ 4 words. No full sentences inside an infographic.
- **One number per stat box** — a stat box shows one number and one short descriptor. Never a sentence.
- **No kicker on infographic slides** — omit the `.kicker` element when the `.card-body` is occupied by an infographic that already has its own section label.
- **Breathing room test** — if more than 60% of the card body would be filled with infographic content, fall back to plain text for that slide.
- **Progress bars — positive values only** — when using `infographic-progress-bars.html` (layout key `improvements`), every `progress-val` must be a positive percentage. If a metric is naturally expressed as a reduction (e.g., "−90% less drafting time"), invert the framing: change the metric label to state the positive outcome ("Time saved on contracts") and drop the minus sign ("90%"). The bar width stays the same. Never show a minus sign in a `progress-val`.

## Critical CSS Rule — Comparison Table

**Never set `font-size` on `.comp-feature`** — `.comp-feature` elements always carry the class `.comp-cell` too. Setting `font-size` on `.comp-feature` would silently override `.comp-cell` with a smaller value. Set one `font-size` on `.comp-cell` only.

## Plain Text Fallback Conditions

Always use plain regardless of trigger rule:
- Content is primarily narrative with no structured data
- Fewer data points than the layout minimum (e.g., fewer than 3 steps for `how_it_works`)
- `<has-visual-theme>` = false
- The slide content doesn't fit the layout meaningfully
- The headline would need to exceed 6 words AND the infographic is data-heavy
