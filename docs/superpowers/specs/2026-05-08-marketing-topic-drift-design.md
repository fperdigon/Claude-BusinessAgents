# Design: Marketing Skill — Enforce Post Title as Carousel Thesis

**Date:** 2026-05-08
**Skill:** `.claude/skills/BusinessAgents/marketing.md`
**Problem:** The Sonnet sub-agent generates slide content related to the company's domain generally, ignoring the specific angle the founder typed as the post title in Q1.

---

## Root Cause

The Sonnet sub-agent prompt buries `<post-title>` as one line in a list of eight session choices. The startup context and ICP are pasted in full immediately after — much longer text that dominates the sub-agent's attention. The sub-agent writes to the company's domain rather than the specific angle in the title.

---

## Changes

### 1. Sub-agent prompt restructure (Approach B — title-first framing)

**Where:** The Sonnet sub-agent prompt block in `## Carousel Content Generation`.

**Change:** Add a `## CAROUSEL THESIS` section as the very first content in the sub-agent prompt, before the role description. Frame the post title as the primary directive. Relegate startup context and ICP to facts-only sources.

```
## CAROUSEL THESIS — your primary directive
**Post title (every slide must serve this exact angle):**
> [Q1 answer]

This is the argument, angle, and hook of the entire carousel. Every slide must directly
advance, illustrate, or support this specific statement.
The startup context and ICP below are facts-only sources — they do not set the direction
or topic. Use them to find evidence that supports the thesis above.

---
You are a LinkedIn content strategist and copywriter...
```

**New rule added to sub-agent rules block:**
> "Post title is the thesis — every slide headline and every bullet must directly relate to the angle stated in the post title above; never drift to the company domain generally."

---

### 2. Per-template title anchoring (Approach B continued)

**Where:** Each template description inside the sub-agent prompt.

**Change:** One anchor line at the top of each template:

- **Template 1 — Problem Awareness:** "All slides must address the specific problem framed in `<post-title>` — not a generic industry pain."
- **Template 2 — Before/After Journey:** "The journey must illustrate the transformation implied by `<post-title>` — not a generic before/after for the company."
- **Template 3 — Tips & Education:** "Every tip must be directly relevant to the specific angle in `<post-title>` — no generic advice about the company's domain."
- **Template 4 — Your Story:** "The story must center on the specific insight or struggle stated in `<post-title>` — not the founder's general origin story."

---

### 3. Post-generation validation step (Approach C)

**Where:** The Haiku resume block, immediately after `<carousel-content>` is received from Sonnet.

**Logic:**
1. For each slide, Haiku checks whether the headline directly addresses the angle in `<post-title>`. A slide drifts if its headline could apply to any carousel about the company's domain — nothing specific to the post title's angle.
2. If **2 or more slides** are flagged as drifted, Haiku dispatches a second minimal Sonnet sub-agent.
3. The correction sub-agent receives: the post title string, the subset of slide objects from `<carousel-content>.slides` that were flagged (same JSON schema as the original — `number`, `kicker`, `headline`, `content_type`, `bullets`, etc.), and one instruction: "Rewrite only these slides so each headline directly addresses the post title's specific angle. Return the same JSON array with only the corrected slides." Haiku merges by slide `number`.
4. Haiku merges corrections into `<carousel-content>` and proceeds with HTML assembly.
5. Fully silent — no user interruption. If correction sub-agent fails or is unclear, Haiku proceeds with original content.

**New Hard Rule:**
> "After receiving `<carousel-content>` from Sonnet, run a silent topic check against `<post-title>`. If 2+ slide headlines drift from the title's specific angle, dispatch a minimal correction sub-agent before HTML assembly."

---

## What Does NOT Change

- The 8-question flow is unchanged.
- The HTML assembly, infographic logic, PDF export, and registry update are unchanged.
- Startup context and ICP are still passed to the sub-agent — they are just reframed as supporting facts, not the primary direction.
- No user-facing changes to the Q&A experience.

---

## Success Criteria

- A specific post title like "Why law firms lose 3 hours a day to email" produces slides specifically about email inefficiency at law firms — not about AI for law firms generally.
- The hook slide headline reflects the post title's angle.
- All content slides advance the specific argument in the title.
