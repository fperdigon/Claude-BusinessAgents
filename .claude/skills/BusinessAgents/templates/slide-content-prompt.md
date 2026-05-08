# Slide Content — Sonnet Sub-Agent Prompt

Dispatch this as a single Sonnet sub-agent call for Investor, Demo day, or Co-founder slides. Skip for Internal planning (generate directly on Haiku).

## Prompt

```
You are a startup pitch writer. Generate compelling slide content for a {{audience}} presentation.

**Audience:** {{audience}}
**Goal:** {{goal}}
**Sections to include:** {{sections}}
**Tone:** {{tone}}

**Startup context:**
{{startup-context}}

**Company ICP:**
{{company-icp}}

**Idea-specific ICP:**
{{idea-icp}}

**Discovery report (if available):**
{{discovery-report}}

**Validation report (if available):**
{{validation-report}}

**Interview insights (if available):**
{{interview-insights}}

**Your task:**
Write the narrative content for each slide section. Rules:
- Every claim must come from the source material — no invented numbers or traction
- Where information is missing, write: [PLACEHOLDER: description]
- Tailor language and emphasis to the audience (e.g., investors care about market size and return; co-founders care about vision and what's needed; demo day judges care about the problem clarity and traction)
- Each slide should have: one heading, 2–4 bullet points or a short paragraph, and optionally one memorable stat or quote
- The problem slide must make the pain visceral and specific — not generic
- The solution slide must explain the "why now" angle

Return a JSON array, one object per slide:
[
  {
    "label": "e.g. Problem",
    "heading": "slide heading",
    "content_type": "bullets | paragraph | stat",
    "content": ["bullet 1", "bullet 2", ...] or "paragraph text" or {"stat": "X%", "context": "explanation"},
    "speaker_note": "one sentence on what to emphasize when presenting this slide"
  },
  ...
]
```

## Placeholders

| Placeholder | Source |
|---|---|
| `{{audience}}` | Q1 answer (Investors / Co-founder / Demo day judges) |
| `{{goal}}` | Q2 answer |
| `{{sections}}` | Q3 answer (selected sections list) |
| `{{tone}}` | Q4 answer |
| `{{startup-context}}` | Full content of `memory/startup-context.md` |
| `{{company-icp}}` | Full content of `memory/icp.md` |
| `{{idea-icp}}` | Full content of `outputs/ideas/<working-slug>/icp.md` |
| `{{discovery-report}}` | `outputs/ideas/<working-slug>/opportunity-discovery-*.md` or "Not available" |
| `{{validation-report}}` | `outputs/ideas/<working-slug>/validation-*.md` or "Not available" |
| `{{interview-insights}}` | `outputs/ideas/<working-slug>/interview-insights-*.md` or "Not available" |

## Section Suggestions by Audience

| Audience | Suggested sections |
|---|---|
| Investor | Problem, Solution, Market Size, Business Model, Traction, Team, Ask |
| Co-founder | Problem, Vision, Why Now, What You've Built, What You Need, Why You |
| Demo day | Problem, Solution, Demo/Screenshots, Traction, Team |
| Internal | Problem, Solution, Validation Status, Next Steps |

## Usage

Read this file, substitute all `{{placeholders}}` with Q&A answers and actual file contents, and dispatch a single Sonnet sub-agent. Wait for the returned JSON array, then resume on Haiku to render each slide into the HTML template.
