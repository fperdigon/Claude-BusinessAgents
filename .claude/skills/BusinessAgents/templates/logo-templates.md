# Logo SVG Templates

All SVGs must be fully self-contained (no external refs, no linked fonts — use generic font-family stacks), scalable at any size (use `viewBox`, not fixed `width`/`height`), and production-ready.

## Variant 1 — Primary (icon + wordmark, horizontal)

Structure: Icon mark on the left, full company name on the right.

```svg
<svg viewBox="0 0 320 80" xmlns="http://www.w3.org/2000/svg">
  <!-- Icon mark -->
  [icon shape — rect/circle/path with brand accent color]
  [initials or abstract shape inside]
  <!-- Wordmark -->
  <text x="[icon-width + 16]" y="50" font-family="[chosen font stack]"
        font-size="28" font-weight="700" fill="[text color]"
        letter-spacing="-0.5">[Company Name]</text>
  <!-- Optional tagline -->
  <text x="[icon-width + 16]" y="68" font-family="[chosen font stack]"
        font-size="11" font-weight="400" fill="[muted color]"
        letter-spacing="0.08em" text-transform="uppercase">[Short tagline if applicable]</text>
</svg>
```

## Variant 2 — Icon only

The icon mark from the primary logo, isolated. Square viewBox (e.g., `0 0 80 80`). Use as favicon, app icon, or social media profile picture.

**Critical clipPath rule:** Always add a `<clipPath>` in `<defs>` matching the background rect shape, and wrap all graphic elements in `<g clip-path="url(#...)">`. This prevents the icon mark from bleeding outside the rounded container.

**Never place `clip-path` and `transform` on the same `<g>`.** SVG applies `clip-path` in the element's local (already-transformed) coordinate space, so the clip region moves with the transform and the overflow is not clipped. Always use two nested groups: the outer one carries `clip-path`, the inner one carries `transform`.

```svg
<defs>
  <clipPath id="iconBounds">
    <rect x="[x]" y="[y]" width="[w]" height="[h]" rx="[rx]"/>
  </clipPath>
</defs>
<rect x="[x]" y="[y]" width="[w]" height="[h]" rx="[rx]" fill="[bg]"/>
<g clip-path="url(#iconBounds)">          <!-- clip applied in parent space -->
  <g transform="[translate/scale if needed]">  <!-- transform on inner group -->
    <!-- icon mark elements here -->
  </g>
</g>
```

If no transform is needed, the inner `<g transform>` can be omitted — just place elements directly inside `<g clip-path>`.

## Variant 3 — Wordmark only

Company name only, no icon. Wide viewBox sized to text. Use in contexts where the icon would be too small to read.

## Variant 4 — Monochrome (dark)

Primary logo with all colors replaced by a single dark color (`#1a1a1a` or the darkest brand color). For use on light backgrounds, printed materials, or embossing.

---

## Icon Mark Designs by Style

Choose the style that best matches the brand feeling and product positioning from `memory/startup-context.md`.

### Lettermark in rounded square

```svg
<rect x="0" y="0" width="80" height="80" rx="12" fill="[accent]"/>
<text x="40" y="55" font-family="system-ui" font-size="36" font-weight="800"
      fill="white" text-anchor="middle" dominant-baseline="auto">[XX]</text>
```

### Abstract mark — "AI document" (for AI/legal positioning)

```svg
<!-- Document shape -->
<rect x="8" y="4" width="44" height="56" rx="4" fill="[accent]" opacity="0.15"/>
<rect x="8" y="4" width="44" height="56" rx="4" fill="none" stroke="[accent]" stroke-width="2.5"/>
<!-- Corner fold -->
<path d="M 40 4 L 52 16 L 40 16 Z" fill="[bg]" stroke="[accent]" stroke-width="2"/>
<!-- AI dots pattern (3x2 grid suggesting neural network) -->
<circle cx="20" cy="30" r="2.5" fill="[accent]"/>
<circle cx="30" cy="30" r="2.5" fill="[accent]"/>
<circle cx="40" cy="30" r="2.5" fill="[accent]"/>
<circle cx="20" cy="42" r="2.5" fill="[accent]"/>
<circle cx="30" cy="42" r="2.5" fill="[accent]"/>
<circle cx="40" cy="42" r="2.5" fill="[accent]"/>
```

### Abstract mark — "Shield" (for privacy/security positioning)

```svg
<path d="M 40 8 L 68 20 L 68 44 Q 68 62 40 72 Q 12 62 12 44 L 12 20 Z"
      fill="[accent]" opacity="0.9"/>
<path d="M 28 40 L 36 48 L 52 32" stroke="white" stroke-width="3.5"
      fill="none" stroke-linecap="round" stroke-linejoin="round"/>
```
