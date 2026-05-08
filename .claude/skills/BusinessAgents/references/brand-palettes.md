# Brand Palettes & Mode Derivation

## Default Palettes by Feeling

Use these when the founder selects "suggest a palette" in Question 4.

### Professional & Trustworthy
- `#1a2744` — deep navy (primary/background)
- `#c9a84c` — gold accent (highlights, CTAs)
- `#f8f6f1` — warm white (text on dark)
- `#6b7280` — neutral gray (muted text)
- `#ffffff` — white (surfaces)

### Modern & Tech-forward
- `#0f172a` — dark navy (primary/background)
- `#3b82f6` — electric blue (accent)
- `#f8fafc` — near white (text on dark)
- `#64748b` — slate (muted text)
- `#ffffff` — white (surfaces)

### Warm & Approachable
- `#1a3a2a` — deep green (primary/background)
- `#f59e0b` — amber (accent)
- `#fefce8` — warm cream (text/surfaces)
- `#6b7280` — gray (muted text)
- `#ffffff` — white (surfaces)

### Bold & Confident
- `#18181b` — near black (primary/background)
- `#ef4444` — bold red (accent)
- `#fafafa` — white (text on dark)
- `#71717a` — zinc (muted text)
- `#ffffff` — white (surfaces)

---

## Theme Mode Detection

### Brightness Formula

`brightness = 0.299 × R + 0.587 × G + 0.114 × B` (R, G, B are 0–255)

### Classification

| Brightness | Classification |
|-----------|---------------|
| Below 110 | **dark** — the brand uses a dark background |
| Above 145 | **light** — the brand uses a light background |
| 110–145 | **neutral** — mixed or ambiguous theme |

### Mode Variants to Generate

| Brand theme | Generate |
|-------------|----------|
| dark | light mode variant only |
| light | dark mode variant only |
| neutral | both dark and light |

---

## Dark Mode Palette Derivation

| Token | How to derive |
|-------|--------------|
| Background | Take the darkest brand color and push toward near-black. Target brightness < 30. Example: primary `#1a3a6b` → dark bg `#0d1b36`. If no dark color exists, derive from primary hue at 10–15% lightness. |
| Surface | Background + 8–12% brightness increase. |
| Text (primary) | `#f8fafc` or `#e2e8f0` |
| Text muted | `#94a3b8` |
| Accent | Keep brand accent. If contrast ratio against dark bg is below 3:1, increase brightness by ~10% and note. |
| Border/divider | `rgba(255,255,255,0.1)` |

## Light Mode Palette Derivation

| Token | How to derive |
|-------|--------------|
| Background | `#ffffff` or very slight tint from brand hue (target brightness > 245). Example: navy brand → `#f8f9fb` (cool tint). |
| Surface | `#f1f5f9` or slightly tinted off-white. |
| Text (primary) | Use darkest brand color, or derive near-black from it (target brightness < 30). |
| Text muted | `#64748b` |
| Accent | Keep brand accent. If contrast ratio against light bg is below 3:1, darken slightly and note. |
| Border/divider | `rgba(0,0,0,0.08)` |
