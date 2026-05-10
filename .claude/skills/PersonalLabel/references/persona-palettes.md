# Persona Palettes

Five palette families tuned for personal brands. Each assumes a portrait photo may sit alongside the palette, so contrast and skin-tone harmony are factored in. Distinct from the corporate palettes in `BusinessAgents/references/brand-palettes.md`.

## 1. Photographer-warm

For storytellers, travel writers, lifestyle creators, anyone whose work benefits from warmth and light.

| Role | Hex | Name |
|---|---|---|
| Primary (page bg) | `#1c1814` | Espresso |
| Surface | `#2a221b` | Walnut |
| Accent | `#e8a948` | Amber gold |
| Text | `#f5ecd9` | Cream |
| Text muted | `#b9a87f` | Warm sand |

- **Photography pairing:** documentary, golden-hour, warm grading, slight film grain.
- **Font pairing:** Humanist Sans-serif or Classic Serif.
- **Theme:** dark.

## 2. Engineer-precise

For technical experts, software engineers, ML researchers, analysts. Cool, exact, no warmth without purpose.

| Role | Hex | Name |
|---|---|---|
| Primary (page bg) | `#0f172a` | Slate-900 |
| Surface | `#1e293b` | Slate-800 |
| Accent | `#22d3ee` | Cyan-400 |
| Text | `#f1f5f9` | Slate-100 |
| Text muted | `#94a3b8` | Slate-400 |

- **Photography pairing:** high-key portrait, neutral or cool grading, sharp detail.
- **Font pairing:** Geometric Sans-serif or Minimal/Mono.
- **Theme:** dark.

## 3. Creative-bold

For designers, founders, makers, contrarians. High contrast, distinctive, memorable.

| Role | Hex | Name |
|---|---|---|
| Primary (page bg) | `#1a0b2e` | Deep purple |
| Surface | `#2e1849` | Plum |
| Accent | `#ff6b6b` | Coral |
| Text | `#fdf6e3` | Off-white |
| Text muted | `#c2a8d6` | Lavender |

- **Photography pairing:** stylised editorial, bold lighting, willing to push saturation.
- **Font pairing:** Geometric Sans-serif (with weight variation).
- **Theme:** dark.

## 4. Consultant-trust

For advisors, executives, consultants, coaches. Authoritative, classic, premium without being cold.

| Role | Hex | Name |
|---|---|---|
| Primary (page bg) | `#fcfaf5` | Parchment |
| Surface | `#ffffff` | White |
| Accent | `#0a2540` | Navy |
| Secondary accent | `#c79a3f` | Antique gold |
| Text | `#0a2540` | Navy |
| Text muted | `#5a6479` | Slate-blue |

- **Photography pairing:** classic studio portrait, neutral grading, soft fill.
- **Font pairing:** Classic Serif or Humanist Sans-serif.
- **Theme:** light.

## 5. Academic-classic

For researchers, educators, authors. Restrained, traditional, intellectually credible.

| Role | Hex | Name |
|---|---|---|
| Primary (page bg) | `#f5f1e8` | Parchment |
| Surface | `#ffffff` | White |
| Accent | `#1f3a2e` | Forest green |
| Secondary accent | `#7a4a2e` | Dark walnut |
| Text | `#1c1c1a` | Ink |
| Text muted | `#6b6354` | Sepia |

- **Photography pairing:** muted, slightly desaturated, soft natural light.
- **Font pairing:** Classic Serif (preferred) or Humanist Sans-serif.
- **Theme:** light.

## Custom (Q3 option 6)

If the user picks Custom, ask for:
- Primary (page background)
- Accent (one bright color for highlights/links)
- Text (high-contrast against primary)
- Text muted (~60% of text contrast)
- Surface (one step away from primary for cards)

Then derive whether `<persona-theme>` is dark or light from the primary color's brightness using the formula in `BusinessAgents/references/brand-palettes.md`.

## Selection guide by personality keywords

When the user provides personality keywords in Q1, use this mapping to suggest the most-likely palette before they pick in Q3:

| Keywords | Suggest |
|---|---|
| precise, technical, calm | Engineer-precise |
| warm, approachable, expressive | Photographer-warm |
| bold, raw, playful | Creative-bold |
| classic, refined, scholarly | Consultant-trust or Academic-classic |
| precise + bold | Engineer-precise (with Coral accent variant) |

This is a *suggestion*, not a default — always present all five families and let the user choose.
