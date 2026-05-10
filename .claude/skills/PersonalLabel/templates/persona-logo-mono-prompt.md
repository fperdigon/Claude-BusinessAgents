# Persona Logo SVG Schema

Design rules for generating four logo SVG variants for a person. The hard SVG rules from `BusinessAgents/templates/logo-templates.md` apply (clipPath usage, no `clip-path` + `transform` on the same `<g>`, full self-containment, viewBox required, no external font refs).

## Variant 1 — Monogram

- viewBox: `0 0 200 200` (square)
- Mark: rounded square (`rx=24`), circle, hex, or rounded triangle — choose by personality:
  - `precise / technical` → rounded square
  - `bold / raw` → hexagon or pentagon
  - `warm / approachable` → circle
  - `classic / refined` → square with subtle inner border
- Fill: `<accent>` color from chosen palette.
- Initials: 1–3 characters from the persona's full name (`<initials>`).
  - 2 letters preferred (first + last name).
  - For 3-name persons, allow middle initial only if it improves balance.
- Initials font: `<font-stack>`; weight `700`; fill = `<text-on-accent>` (white for dark accents, dark for light accents).
- Initials sized to ~52% of mark height; centered both axes.
- Always include a `<clipPath>` matching the mark shape in `<defs>`. Wrap any inner content (initials, sub-marks) in an outer `<g clip-path>` to prevent bleeding outside rounded edges.

## Variant 2 — Wordmark only

- viewBox: `0 0 600 200` (wide; adjust width if name is long, in 100-unit increments)
- Content: full name only; no mark, no initials.
- Font: `<font-stack>`; weight `600`–`800` based on personality (bold = 800, classic = 600).
- Fill: `<accent>` for the surname (or both names if single-word brand); `<text>` for the first name.
- Letter-spacing: `-0.01em` for Geometric Sans / Mono; `0` for Humanist; `0.01em` for Classic Serif.
- Vertically centered. Horizontal padding ~48 units left and right.
- Optional underline accent: a 4-unit-tall rectangle at 88% height, fill = `<accent>`, length = 24% of the wordmark width, aligned to the start of the surname. Only include if personality contains `bold` or `confident`.

## Variant 3 — Icon

The icon variant changes by `<logo-concept>`:

### If `<logo-concept>` = 1 (Monogram primary):
- Same as Variant 1, but mark only — no initials. The geometry stands alone.

### If `<logo-concept>` = 2 (Wordmark primary):
- A square box (`0 0 200 200`) with a single-letter abstract treatment of the persona's first initial — large, edge-to-edge, fill = `<accent>`, set inside the brand-color background.

### If `<logo-concept>` = 3 (Silhouette / abstract):
- Square (`0 0 200 200`). Generate a simple abstract mark (3–6 paths, no fine detail) inspired by the persona's first Topic of Expertise. Examples:
  - "AI for legal" → a stylised scale + node
  - "Photography" → a geometric aperture
  - "Open-source" → an interlocking bracket pattern
- Fill: `<accent>`. Stroke: none, unless a stroke-only style fits the personality (`precise` may justify stroke-only).
- Keep the silhouette readable at 32×32 — favor strong shapes over fine lines.

### If `<logo-concept>` = 4 (Photo-circle):
- viewBox: `0 0 200 200`.
- A circle of radius 96 centered at (100, 100), fill = `<accent>` (acts as ring background).
- A `<clipPath id="photo-clip">` containing a circle of radius 92 centered at (100, 100).
- An `<image href="<photo-path-absolute>" x="8" y="8" width="184" height="184" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo-clip)" />`.
- Use absolute filesystem path in `href` (no `file://` prefix needed for SVG inside HTML; for standalone SVG viewing the prefix may help).
- Outside the clipped image, a 4-unit-thick `<accent>` ring.
- **Do not** apply `transform` and `clip-path` to the same `<g>` — keep the image element direct, not wrapped.

## Variant 4 — Monochrome

- viewBox: same as Variant 1 (square, `0 0 200 200`) for monogram brands; same as Variant 2 (`0 0 600 200`) for wordmark brands.
- All elements collapsed to a single fill color:
  - For dark-themed palettes: fill = `#0f172a` (or persona's `<text>` color).
  - For light-themed palettes: fill = `#fcfaf5` (or persona's `<text>` color on a dark sample background).
- Used for: stamps, watermarks, single-color print, embroidery files, embossing.
- No accent color, no gradients, no opacity.

## Self-containment checks

Before saving any variant:
1. Strip any `<style>` block referencing external URLs.
2. Confirm no `font-family` references a font that requires external loading — only system stacks from `<font-stack>`.
3. Confirm `viewBox` is present.
4. Confirm any `<clipPath>` is referenced via `clip-path="url(#id)"` and the `<defs>` block exists.
5. Confirm no `<g>` simultaneously has `clip-path` and `transform`.
6. For Photo-circle, confirm `<image href>` points to an absolute path that exists on disk.
