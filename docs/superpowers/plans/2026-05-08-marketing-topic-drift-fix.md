# Marketing Skill — Topic Drift Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure the Sonnet sub-agent always writes carousel content to the founder's specific post title, not to the company's domain generally.

**Architecture:** Three targeted edits to `.claude/skills/BusinessAgents/marketing.md` — (1) promote the post title to a top-level thesis directive in the sub-agent prompt, (2) add per-template anchor lines, (3) insert a silent Haiku validation + correction step after the Sonnet response. No structural changes to the Q&A flow or HTML assembly.

**Tech Stack:** Markdown skill file — no code files, no dependencies.

---

### Task 1: Promote post title to CAROUSEL THESIS in sub-agent prompt

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md` — the Sonnet sub-agent prompt block (around line 483)

The sub-agent prompt currently opens with the role description followed by a flat list of session choices. The post title is buried as one line. This task inserts a `## CAROUSEL THESIS` block as the very first content in the prompt, before the role description.

- [ ] **Step 1: Locate the exact opening of the sub-agent prompt block**

The block starts with the backtick-fenced prompt string. Search for this line:

```
You are a LinkedIn content strategist and copywriter. Write a complete carousel post for a founder's brand.
```

It appears inside a fenced code block under `## Carousel Content Generation`.

- [ ] **Step 2: Insert the CAROUSEL THESIS block before the role description**

Replace:
```
You are a LinkedIn content strategist and copywriter. Write a complete carousel post for a founder's brand.

**Session choices:**
- Post title: [Q1 answer]
- Audience: [Q2 answer — general or icp]
- Format: [Q3 answer — e.g., LinkedIn Carousel 1080×1080]
- Topic template: [Q4 answer — Problem Awareness / Before/After Journey / Tips & Education / Your Story]
- Tone: [Q5 answer]
- Slide count: [Q6 answer]
- CTA: [Q8 answer]
```

With:
```
## CAROUSEL THESIS — your primary directive
**Post title (every slide must serve this exact angle):**
> [Q1 answer]

This is the argument, angle, and hook of the entire carousel. Every slide must directly advance, illustrate, or support this specific statement.
The startup context and ICP below are facts-only sources — they do not set the direction or topic. Use them to find evidence that supports the thesis above.

---

You are a LinkedIn content strategist and copywriter. Write a complete carousel post for a founder's brand.

**Session choices:**
- Post title: [Q1 answer]
- Audience: [Q2 answer — general or icp]
- Format: [Q3 answer — e.g., LinkedIn Carousel 1080×1080]
- Topic template: [Q4 answer — Problem Awareness / Before/After Journey / Tips & Education / Your Story]
- Tone: [Q5 answer]
- Slide count: [Q6 answer]
- CTA: [Q8 answer]
```

- [ ] **Step 3: Add thesis rule to the sub-agent Rules block**

Locate the Rules block inside the sub-agent prompt (the block that starts with `Rules:`). It contains lines like `- Every fact must come from the source material`. Add one line at the top of the list:

Replace:
```
Rules:
- Every fact must come from the source material — no invented stats
```

With:
```
Rules:
- Post title is the thesis — every slide headline and every bullet must directly relate to the angle stated in the post title above; never drift to the company domain generally
- Every fact must come from the source material — no invented stats
```

- [ ] **Step 4: Manual verification — confirm the block is in the right position**

Read `.claude/skills/BusinessAgents/marketing.md` lines 480–510. Verify:
- `## CAROUSEL THESIS` appears before `You are a LinkedIn content strategist`
- The `> [Q1 answer]` thesis quote is present
- The "facts-only sources" sentence is present
- Session choices list is unchanged and follows the role description

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "fix(marketing): elevate post title to CAROUSEL THESIS in sub-agent prompt"
```

---

### Task 2: Add per-template title anchor lines

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md` — the four template descriptions inside the sub-agent prompt

Each template currently lists slide structure without referencing `<post-title>`. This task adds one anchor line at the top of each template that binds the content to the title.

- [ ] **Step 1: Add anchor to Template 1 — Problem Awareness**

Locate:
```
Template 1 — Problem Awareness:
- Slide 1 (Hook): shocking statement or bold question; lead with a striking number or claim that makes the reader think "wait, that's me"
```

Replace with:
```
Template 1 — Problem Awareness:
*(All slides must address the specific problem framed in `<post-title>` — not a generic industry pain.)*
- Slide 1 (Hook): shocking statement or bold question; lead with a striking number or claim that makes the reader think "wait, that's me"
```

- [ ] **Step 2: Add anchor to Template 2 — Before/After Journey**

Locate:
```
Template 2 — Before/After Journey (use simulation report):
- Slide 1 (Hook): "Here's how [ICP job title] handles [painful task] today. (Keep swiping →)"
```

Replace with:
```
Template 2 — Before/After Journey (use simulation report):
*(The journey must illustrate the transformation implied by `<post-title>` — not a generic before/after for the company.)*
- Slide 1 (Hook): "Here's how [ICP job title] handles [painful task] today. (Keep swiping →)"
```

- [ ] **Step 3: Add anchor to Template 3 — Tips & Education**

Locate:
```
Template 3 — Tips & Education:
- Slide 1 (Hook): "[N] things every [ICP job title] should know about [topic]"
```

Replace with:
```
Template 3 — Tips & Education:
*(Every tip must be directly relevant to the specific angle in `<post-title>` — no generic advice about the company's domain.)*
- Slide 1 (Hook): "[N] things every [ICP job title] should know about [topic]"
```

- [ ] **Step 4: Add anchor to Template 4 — Your Story**

Locate:
```
Template 4 — Your Story:
- Slide 1 (Hook): "I used to [painful situation] every [time period]." — first person, immediate
```

Replace with:
```
Template 4 — Your Story:
*(The story must center on the specific insight or struggle stated in `<post-title>` — not the founder's general origin story.)*
- Slide 1 (Hook): "I used to [painful situation] every [time period]." — first person, immediate
```

- [ ] **Step 5: Manual verification**

Read the template section. Confirm each of the four templates has one italicised anchor line immediately after its name, and the existing slide structure is unchanged.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "fix(marketing): add per-template title anchor lines in sub-agent prompt"
```

---

### Task 3: Add silent topic validation + correction step

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md` — immediately after the Haiku resume marker that follows the Sonnet sub-agent dispatch

This inserts a new `### Topic Validation Check` section between the Haiku resume marker and the existing `### Template reference (for Haiku post-processing)` section.

- [ ] **Step 1: Locate the Haiku resume marker**

Find this exact line:

```
> 🤖 **Model: Haiku** — resume here after sub-agent returns `<carousel-content>` JSON
```

The line immediately following is:
```
Use `<carousel-content>.slides` to populate every card...
```

- [ ] **Step 2: Insert the Topic Validation Check block**

After the line:
```
> 🤖 **Model: Haiku** — resume here after sub-agent returns `<carousel-content>` JSON
```

And before the line:
```
Use `<carousel-content>.slides` to populate every card, `<carousel-content>.document_title` for the title block
```

Insert:

```
### Topic Validation Check (silent — runs before HTML assembly)
> 🤖 **Model: Haiku**

Before assembling any HTML, check each slide in `<carousel-content>.slides` for topic drift:

For each slide, evaluate: does the `headline` field directly address the specific angle in `<post-title>`? A headline **drifts** if it could apply to any carousel about the company's domain generally — nothing unique to the post title's argument.

Collect drifted slide objects into `<drifted-slides>`.

**If `<drifted-slides>` has 2 or more slides:** dispatch a correction Sonnet sub-agent via the Agent tool with `model: "sonnet"` and this prompt:

```
The post title is: "[post-title]"

The following slides drifted from this topic. Rewrite only these slides so each headline directly addresses the post title's specific angle. Return a JSON array containing only the corrected slides — same schema as the input (number, kicker, headline, content_type, bullets, stat, stat_context, swipe_hint, cta_action, cta_sentence, cta_contact, suggested_icon, layout_hint).

Drifted slides:
[paste <drifted-slides> as JSON array]
```

Wait for the correction sub-agent's response. For each corrected slide in the returned array, replace the matching object in `<carousel-content>.slides` by matching `number`. Proceed with HTML assembly using the merged `<carousel-content>`.

**If `<drifted-slides>` has 0 or 1 slides:** skip the correction step entirely — proceed directly to HTML assembly.

**If the correction sub-agent fails or returns invalid JSON:** proceed with the original `<carousel-content>` without blocking.

```

- [ ] **Step 3: Manual verification**

Read the section around the Haiku resume marker. Confirm:
- `### Topic Validation Check` block appears immediately after the Haiku resume marker line
- The block contains the three conditional branches (2+ slides / 0–1 slides / failure)
- The existing `Use <carousel-content>.slides to populate every card...` line still follows after the new block

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "fix(marketing): add silent topic validation and correction step after Sonnet sub-agent"
```

---

### Task 4: Add Hard Rule for topic validation

**Files:**
- Modify: `.claude/skills/BusinessAgents/marketing.md` — the `## Hard Rules` section

- [ ] **Step 1: Locate the Hard Rules section**

Find the `## Hard Rules` section near the bottom of the file. Locate the rule that starts:
```
- `<topic-slug>` in all file and folder names must be derived from `<post-title>` (Q1)
```

- [ ] **Step 2: Add the new hard rule immediately after that line**

After:
```
- `<topic-slug>` in all file and folder names must be derived from `<post-title>` (Q1), slugified to lowercase hyphenated form — never from the template category name (e.g., `how-law-firms-can-use-ai-to-analyze-contracts`, not `tips-education`)
```

Insert:
```
- After receiving `<carousel-content>` from Sonnet, run a silent topic check against `<post-title>` before HTML assembly — if 2+ slide headlines drift from the title's specific angle, dispatch a minimal correction sub-agent to fix only those slides; merge corrections by slide `number`; never block HTML assembly on correction failure
```

- [ ] **Step 3: Manual verification**

Read the Hard Rules section and confirm the new rule is present immediately after the `<topic-slug>` rule.

- [ ] **Step 4: End-to-end manual verification**

Open `.claude/skills/BusinessAgents/marketing.md` and confirm all four changes are present:
1. `## CAROUSEL THESIS` block at the top of the sub-agent prompt
2. Thesis rule in the sub-agent Rules block
3. Four template anchor lines (one per template)
4. `### Topic Validation Check` block after the Haiku resume marker
5. New hard rule in `## Hard Rules`

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/BusinessAgents/marketing.md
git commit -m "fix(marketing): add hard rule enforcing post-title topic validation"
```
