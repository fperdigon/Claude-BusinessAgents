# Persona Brand Guidelines — HTML Overlay Spec

This document defines what changes when adapting `BusinessAgents/templates/brand-guidelines-base.html` for a personal brand. Read the base template first; this overlay only describes the section deltas.

## Placeholder substitutions (delta from company use)

| Placeholder | Persona value |
|---|---|
| `{{company-name}}` | Persona's full name |
| `{{scope-label}}` | Literal string `Personal Brand` (do not append a slug) |
| `{{tagline}}` | The `Headline` field from `persona-context.md` |

All color, typography, and date placeholders behave identically to company use.

## Section overrides

### `<!-- LOGO_SHOWCASE -->`

Show the four persona variants (Monogram, Wordmark, Icon, Monochrome). Display each twice — once on a light surface, once on a dark surface — using the persona palette's surface colors.

If `<logo-concept>` = 4 (Photo-circle) and a portrait path was provided, also include a third row showing the photo-circle variant on a textured/photo-style background (use a CSS gradient to suggest a real-world photo backdrop).

### `<!-- COLOR_PALETTE -->`

Display the chosen palette as 5–6 swatches. Each swatch shows: hex code, role label, and one-sentence usage note. Pull usage notes from the chosen family in `references/persona-palettes.md`.

### `<!-- TYPOGRAPHY -->`

Same as company guidelines — heading samples (H1, H2, H3) and body text using `<font-stack>`. Use real persona content for the samples:
- H1 sample: persona's headline
- H2 sample: first Topic of Expertise
- Body sample: first sentence of `Bio (long)` from `persona-context.md`

### `<!-- BRAND_VOICE -->` (significantly expanded for persona)

Replace the company tone block with this structure:

```html
<section class="brand-voice">
  <h2>Voice & Tone</h2>

  <div class="voice-grid">
    <div class="voice-block">
      <h3>Tone</h3>
      <p class="voice-tags">[3–5 adjectives, comma separated]</p>
    </div>
    <div class="voice-block">
      <h3>Pronoun</h3>
      <p>[I / we / mixed]</p>
    </div>
    <div class="voice-block">
      <h3>Emoji</h3>
      <p>[policy phrasing — see persona-voice-cues.md]</p>
    </div>
    <div class="voice-block">
      <h3>Hashtags</h3>
      <p>[policy phrasing]</p>
    </div>
    <div class="voice-block">
      <h3>Sentence rhythm</h3>
      <p>[rhythm phrasing]</p>
    </div>
    <div class="voice-block">
      <h3>Avoid</h3>
      <p>[forbidden phrases or "no specific avoids"]</p>
    </div>
  </div>

  <div class="voice-examples">
    <div>
      <h3>Do</h3>
      <ul>
        <li>[do example 1]</li>
        <li>[do example 2]</li>
        <li>[do example 3]</li>
      </ul>
    </div>
    <div>
      <h3>Don't</h3>
      <ul>
        <li>[don't example 1]</li>
        <li>[don't example 2]</li>
        <li>[don't example 3]</li>
      </ul>
    </div>
  </div>
</section>
```

The `do` / `don't` examples are written by the brief Sonnet sub-agent invoked from `persona_brand.md` section 7, or inline on Haiku if the voice signals are clear.

### `<!-- USAGE_RULES -->` (replaced)

Replace the company UI/icon-system rules with persona-specific rules:

```html
<section class="usage-rules">
  <h2>Usage Rules</h2>

  <h3>Clear space</h3>
  <p>Always leave clear space around the monogram equal to the height of the initial letter. Around the wordmark, leave half the height of the lowercase x-height.</p>

  <h3>Headshot crops</h3>
  <p>Use square (1:1) for primary identity placements (LinkedIn, conference badges, About pages). Use circle for icon-scale uses (32–96 px) — apply the circular crop with a 4 px ring in your accent color.</p>

  <h3>Photo grading</h3>
  <p>Match portrait grading to the palette: [photographer-warm → warm grading; engineer-precise → neutral or cool grading; consultant-trust → classic studio neutral; academic-classic → muted desaturated; creative-bold → stylised editorial].</p>

  <h3>Don't</h3>
  <ul>
    <li>Stretch or distort the monogram or wordmark.</li>
    <li>Recolor the monogram outside the palette.</li>
    <li>Place the wordmark on a busy photo without a scrim or panel.</li>
    <li>Use the photo-circle variant on a background of a different person.</li>
  </ul>
</section>
```

### `<!-- ICON_LIBRARY -->`

Same as company guidelines — show the icon grid, library name, license, and browse URL. Persona icon selection is driven by `Topics of Expertise` from `persona-context.md`.

### `<!-- ASSET_INDEX -->`

Table of all generated files in `personal_label/persona_brand/`. Columns: filename, type, purpose, mode (main/dark/light/mono).

## Sections that stay identical to company use

- `<!-- COLOR_PALETTE -->` (structure; only the palette source differs)
- `<!-- TYPOGRAPHY -->` (structure; only the sample copy differs)
- `<!-- MODE_VARIANTS -->` (identical logic — show derived dark/light palettes and logo variants on mode backgrounds)
- `<!-- ICON_LIBRARY -->` (identical)

## Self-containment

Same as company guidelines: zero external URLs except inline-fetched icon SVGs. All fonts via system stack only. All images either inline SVG or absolute filesystem paths (acceptable for local viewing; flag in chat that sharing the HTML elsewhere will break local image refs).
