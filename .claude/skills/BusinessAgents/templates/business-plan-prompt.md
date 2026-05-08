# Full Business Plan — Sonnet Sub-Agent Prompt

Dispatch this as a single Sonnet sub-agent call when the founder requests a full business plan.

## Prompt

```
You are a business plan writer. Generate a comprehensive business plan using all available source material below.

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

**Simulation report (if available):**
{{simulation-report}}

**Interview insights (if available):**
{{interview-insights}}

**Your task:**
Write a comprehensive business plan. Rules:
- Draw every fact from the source material above — never invent numbers or claims
- Where information is genuinely missing, insert: [PLACEHOLDER: brief description of what's needed]
- Write in clear, plain language — no jargon without explanation
- Each section should be substantive, not just headers with one line

Return the complete business plan as markdown using this exact structure:

# Business Plan: [Company Name]
Date: [today's date]

## Executive Summary
[3–5 sentences: what you do, who for, why it works, what you need]

## Problem & Opportunity
[Evidence from discovery report if available; otherwise from startup-context.md]

## Solution
[From validation report and startup-context.md]

## Target Market
[From icp.md and discovery reports]

## Business Model
[From validation report if defined; otherwise PLACEHOLDER]

## Go-to-Market Strategy
[Specific channels and actions based on ICP and validation findings]

## Competitive Landscape
[From discovery report if available; otherwise PLACEHOLDER]

## Financial Projections
[PLACEHOLDER: requires financial modeling session]

## Team
[PLACEHOLDER: team bios]

## What We Need
[PLACEHOLDER: funding ask and use of funds]
```

## Placeholders

| Placeholder | Source |
|---|---|
| `{{startup-context}}` | Full content of `memory/startup-context.md` |
| `{{company-icp}}` | Full content of `memory/icp.md` |
| `{{idea-icp}}` | Full content of `outputs/ideas/<working-slug>/icp.md` |
| `{{discovery-report}}` | `outputs/ideas/<working-slug>/opportunity-discovery-*.md` or "Not available" |
| `{{validation-report}}` | `outputs/ideas/<working-slug>/validation-*.md` or "Not available" |
| `{{simulation-report}}` | `outputs/ideas/<working-slug>/simulation-*.md` (not onepager) or "Not available" |
| `{{interview-insights}}` | `outputs/ideas/<working-slug>/interview-insights-*.md` or "Not available" |

## Usage

Read this file, substitute all `{{placeholders}}` with actual file contents (or "Not available"), and dispatch a single Sonnet sub-agent. Wait for the returned markdown, then resume on Haiku to save the file.
