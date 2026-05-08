# Icon Mapping

## Heroicon Source

Fetch icons from: `https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/<icon-name>.svg`

Strip `aria-hidden` and `data-slot` attributes. Set `stroke="currentColor"`. Wrap in `<span class="icon">`.

## Topic-Based Hook Icon

After `<post-title>` is confirmed, match it against this table (case-insensitive). Store result as `<hook-icon>`. Use on the hook slide — override the sub-agent's `suggested_icon` for slide 1 if it differs.

Match the first row whose keywords appear in `<post-title>`. If multiple match, pick the one whose keywords best describe the main theme.

| Topic keywords in `<post-title>` | Hook icon |
|---|---|
| AI, agent, agents, model, neural, LLM, GPT, machine learning | `sparkles` |
| automation, workflow, repetitive, manual, process | `bolt` |
| privacy, security, data protection, compliance, safe | `shield-check` |
| cost, ROI, savings, money, revenue, budget, price | `banknotes` |
| time, speed, efficiency, faster, productivity, hours | `clock` |
| team, people, staff, adoption, hiring, HR, culture | `users` |
| document, contract, report, file, paperwork, template | `document-text` |
| server, local, on-premise, infrastructure, hardware, GPU | `server-stack` |
| idea, insight, innovation, strategy, vision, future | `light-bulb` |
| data, analytics, metrics, dashboard, numbers, stats | `chart-bar` |
| code, engineering, technical, developer, software, API | `cpu-chip` |
| legal, law, firm, lawyer, regulation, clause | `briefcase` |
| growth, scale, startup, business, market, launch | `arrow-trending-up` |
| education, learning, tips, guide, how-to, explained, what is | `academic-cap` |
| story, founder, journey, personal, origin | `identification` |
| communication, outreach, email, message, contact | `chat-bubble-left-right` |
| no match | `sparkles` |

## Slide-Type Icon Recommendations

| Slide type | Recommended icon(s) |
|------------|-------------------|
| Automation / repetitive tasks | `bolt`, `arrow-trending-up` |
| Privacy / data security | `shield-check`, `lock-closed` |
| AI complexity / tech | `cpu-chip`, `command-line` |
| Documents / reports | `document-text` |
| People / teams / adoption | `users` |
| Time savings | `clock` |
| Ideas / insight | `light-bulb` |
| Server / local AI | `server-stack` |
| Hook slide | determined by topic — see hook icon table above |
| CTA slide | `arrow-top-right-on-square` or `globe-alt` |

## Icon Placement

| Location | Size | Color |
|----------|------|-------|
| Hook slide | 48×48px (`.icon-lg`) | accent |
| Content slides | 28×28px (`.icon`) | accent |
| CTA slide | 36×36px (`.icon-md`) | accent |

## Icon CSS

```css
.icon { display: inline-flex; align-items: center; flex-shrink: 0; }
.icon svg { width: 28px; height: 28px; color: var(--accent); }
.icon-lg svg { width: 48px; height: 48px; }
.icon-md svg { width: 36px; height: 36px; }
.slide-header { display: flex; align-items: center; gap: 12px; margin-bottom: 1.25rem; }
```

## Fallback

If a Heroicon fetch fails, fall back to a Unicode character inline in the headline text: ⚡ 🔒 📄 👥 ⏱ 💡. Never leave a broken `<img>` or empty element.
