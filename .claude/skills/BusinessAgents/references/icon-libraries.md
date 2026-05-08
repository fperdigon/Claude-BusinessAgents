# Icon Libraries Reference

## Free Icon Library Catalog

All libraries below are free for commercial use, no attribution required.

| Library | Style | Icon count | Best for | Browse URL | License |
|---------|-------|-----------|----------|------------|---------|
| **Heroicons** | Clean outline, 24px | 300+ | Minimal tech/SaaS, AI | heroicons.com | MIT |
| **Lucide** | Rounded outline, consistent stroke | 1300+ | Friendly tech, B2B services | lucide.dev | ISC |
| **Phosphor** | 6 styles: thin / light / regular / bold / fill / duotone | 9000+ | Any feeling — extremely versatile | phosphoricons.com | MIT |
| **Tabler Icons** | Precise stroke outline | 5000+ | Technical, professional, engineering | tabler.io/icons | MIT |
| **Feather Icons** | Ultra-minimal line icons | 286 | Clean modern brands, developers | feathericons.com | MIT |
| **Bootstrap Icons** | Outline + fill, broad coverage | 2000+ | General B2B, any industry | icons.getbootstrap.com | MIT |
| **Remix Icon** | Line + fill, expressive | 2800+ | Bold, editorial, service brands | remixicon.com | Apache 2.0 |

## Selection Logic by Brand Feeling

| Feeling | Recommend |
|---------|-----------|
| Professional & Trustworthy | Heroicons, Lucide, Feather |
| Modern & Tech-forward | Heroicons, Tabler, Phosphor |
| Warm & Approachable | Lucide, Remix Icon, Bootstrap Icons |
| Bold & Confident | Phosphor (bold/fill style), Remix Icon, Tabler |

## Selection Logic by Industry

| Industry | Recommend |
|----------|-----------|
| AI / tech / SaaS | Heroicons, Tabler, Phosphor |
| Legal / compliance | Heroicons, Lucide, Tabler |
| Finance / accounting | Heroicons, Feather, Lucide |
| Healthcare / wellness | Bootstrap Icons, Remix Icon |
| Retail / consumer | Bootstrap Icons, Remix Icon, Phosphor |
| Consulting / services | Lucide, Remix Icon, Bootstrap Icons |

## Master Icon Concept Table

Use this to identify 8–12 icons relevant to what the company does, who it serves, and what problems it solves.

| Category | When to include | Concept names |
|----------|----------------|------------------------------------------------------|
| AI / machine learning | Company uses or sells AI | cpu/chip, lightning/bolt |
| Privacy / security | Data handling, legal, compliance | shield-check, lock/padlock |
| Documents / contracts | Law firms, document workflows | document-text, clipboard |
| Automation / workflows | Process automation, efficiency | cog/gear/settings, arrows-cycle |
| People / teams | HR, services, consulting | users/group, person |
| Analytics / growth | Data, reporting, performance | chart-bar, trending-up |
| Communication | Client services, consulting | chat/message-bubble, envelope/mail |
| Time / scheduling | Productivity, time-saving | clock, calendar |
| Ideas / innovation | Strategy, consulting, R&D | light-bulb, rocket |
| Buildings / offices | Local businesses, real estate | building/office, home |
| Search / discovery | Research, due diligence | magnifying-glass/search |
| Web / global | SaaS, international reach | globe |
| Learning / expertise | Training, consulting, education | academic-cap/graduation |
| Server / infrastructure | IT, hosting, local AI | server, database/stack |
| Finance / billing | Accounting, legal billing | banknotes/money, credit-card |

## Heroicons Reference Names

If Heroicons was chosen: `cpu-chip`, `bolt`, `shield-check`, `lock-closed`, `document-text`, `clipboard-document`, `cog-8-tooth`, `arrow-path`, `users`, `user-group`, `chart-bar`, `arrow-trending-up`, `chat-bubble-left-right`, `envelope`, `clock`, `calendar-days`, `light-bulb`, `rocket-launch`, `building-office-2`, `magnifying-glass`, `globe-alt`, `academic-cap`, `server-stack`, `circle-stack`, `banknotes`, `credit-card`

## Fetch URL Patterns per Library

| Library | Fetch URL pattern |
|---------|------------------|
| Heroicons | `https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/<name>.svg` |
| Lucide | `https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/<name>.svg` |
| Phosphor | `https://raw.githubusercontent.com/phosphor-icons/core/main/assets/regular/<name>.svg` |
| Tabler Icons | `https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/outline/<name>.svg` |
| Feather Icons | `https://raw.githubusercontent.com/feathericons/feather/master/icons/<name>.svg` |
| Bootstrap Icons | `https://raw.githubusercontent.com/twbs/icons/main/icons/<name>.svg` |
| Remix Icon | `https://raw.githubusercontent.com/Remix-Design/RemixIcon/master/icons/<Category>/<name>-line.svg` (category folders vary — browse remixicon.com for exact path) |

## SVG Cleanup Rules per Library

Strip these attributes before saving — icons must inherit CSS color via `currentColor`.

| Library | Attributes to remove |
|---------|---------------------|
| Heroicons | `aria-hidden="true"`, `data-slot="icon"` |
| Lucide | `class="..."` (if present), any `data-*` attributes |
| Phosphor | `class="..."` (if present) |
| Tabler | Usually clean — no stripping needed |
| Feather | Usually clean — no stripping needed |
| Bootstrap | `class="bi bi-..."` |
| Remix Icon | `class="..."` (if present) |

Always keep: `xmlns`, `viewBox`, `fill`, `stroke-width`, `stroke="currentColor"` (if present).
