# Format Specifications

## Format Menu

Present these options to the founder:

**Square (1:1)**
1. LinkedIn Carousel — 1080 × 1080 · PDF upload / document post *(Recommended)*
2. Instagram Feed Square — 1080 × 1080 · feed post, carousel

**Portrait**
3. Instagram Portrait — 1080 × 1350 · feed post (4:5, max portrait fill)
4. Stories — 1080 × 1920 · Instagram / LinkedIn / Facebook full-screen
5. Pinterest — 1000 × 1500 · standard pin (2:3)

**Landscape**
6. Presentation Slide — 1920 × 1080 · Google Slides / Keynote / PowerPoint
7. Link Preview — 1200 × 628 · LinkedIn / Twitter / Facebook shared-link thumbnail

**Document**
8. A4 / Letter — 794 × 1123 · PDF one-pager / print leave-behind

**Mobile-Optimized**
9. LinkedIn Mobile — 1080 × 1350 · mobile-first LinkedIn carousel (4:5) — very large fonts, 3 bullets max per slide

## Format Slug Mapping

| # | Slug | Width | Height | Ratio group |
|---|------|-------|--------|-------------|
| 1 | `linkedin-carousel` | 1080 | 1080 | square |
| 2 | `instagram-square` | 1080 | 1080 | square |
| 3 | `instagram-portrait` | 1080 | 1350 | portrait |
| 4 | `stories` | 1080 | 1920 | portrait |
| 5 | `pinterest` | 1000 | 1500 | portrait |
| 6 | `presentation` | 1920 | 1080 | landscape |
| 7 | `link-preview` | 1200 | 628 | landscape |
| 8 | `a4-letter` | 794 | 1123 | document |
| 9 | `linkedin-mobile` | 1080 | 1350 | portrait |

## Platform Labels

| Format # | Platform label (top-right brand bar) |
|----------|--------------------------------------|
| 1 | LinkedIn |
| 2 | Instagram |
| 3 | Instagram |
| 4 | Stories |
| 5 | Pinterest |
| 6 | Presentation |
| 7 | Link Preview |
| 8 | A4 / Letter |
| 9 | LinkedIn |

## Infographic Layout Adaptation by Format Ratio

- `portrait` and format = `stories` (1080×1920): prefer vertically-stacked layouts — `how_it_works`, `results`, `testimonial`. Avoid `versus` and `use_cases` which need horizontal space. Use icon grid 2 columns × 3 rows instead of 3×2.
- `landscape` (`presentation`, `link-preview`): prefer horizontally-arranged layouts — `comparison`, `versus`, `use_cases`, `capabilities` 3×2. `results` and `pipeline` adapt well. `how_it_works` should be arranged horizontally.
- All other ratios: use layouts as-is.
