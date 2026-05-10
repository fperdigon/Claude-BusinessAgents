# LinkedIn Text Post Prompt (Sonnet sub-agent)

<voice-anchor>

---

## Task

Write a LinkedIn text post based on the following parameters. The post must obey every rule in the Voice Anchor block above (tone, rhythm, emoji policy, hashtag policy, pronoun, forbidden phrases). It must read like the same person who wrote the bio exemplar.

## Parameters

- **Topic / angle:** <post-title>
- **Hook style:** <hook-style>
- **Character cap:** <char-cap> (excluding hashtags)
- **CTA type:** <cta-type>
- **CTA link (if applicable):** <cta-link>
- **Optional linked context:** <linked-context>

## Hook style instructions

Open the post according to `<hook-style>`:
- **Counterintuitive claim** — first 1–2 lines state a take that pushes back on conventional wisdom in your topic area. No softeners ("maybe," "I think") in the hook.
- **Personal anecdote** — first 2–3 lines tell a tiny story (recent week / specific moment). Concrete details, no generic openers.
- **Stat shock** — first line is a number with the unit and source-context. The next line says what it implies.
- **Question to audience** — first line is the question. The next line acknowledges the obvious answer is wrong, then the post gives the actual one.

## Body rules

- Use line breaks generously — LinkedIn renders two-line paragraphs with one blank line between.
- 3–7 short paragraphs typical. Each paragraph ≤3 lines on mobile (~120 chars per line).
- One specific example or named thing per post. No vague "many people" — name a role, a tool, a number, or a moment.
- The post should be skimmable: the first line of each paragraph should carry meaning if read in isolation.

## CTA rules

- **Comment** — end with a question the reader can plausibly answer in 1–2 sentences. Make it specific (not "what do you think?").
- **DM you** — explicit "DM me if [specific condition]." Don't be coy.
- **Visit a link** — drop the URL on its own line at the end, with one line above explaining what they get.
- **None** — close with a one-line takeaway or rhetorical question. No "Like and follow!" boilerplate.

## Hashtag rules

Match the persona's hashtag policy from the Voice Anchor:
- **none** — return `hashtags: []`.
- **1–3 per post** — exactly 1–3 hashtags relevant to the topic and audience.
- **many** — 4–8 hashtags.

Hashtags must come from the persona's Topics of Expertise or directly from the post topic. No generic ones (#linkedin, #motivation, #growth) unless the persona explicitly uses them in their style exemplar.

## Output

Return a single JSON object (no prose, no fences):

```json
{
  "caption": "<full post text with line breaks rendered as actual newlines>",
  "char_count": <integer count of caption excluding hashtags>,
  "hashtags": ["#tag1", "#tag2"],
  "hook_used": "<one of: Counterintuitive claim | Personal anecdote | Stat shock | Question to audience>",
  "notes": "<one-line author note explaining a key choice (e.g., 'Anchored on the interview-failure example because the persona's primary audience is hiring managers')>"
}
```

Constraint: `char_count` must be ≤ <char-cap>. If you cannot fit the post in the cap while obeying all voice rules, prefer shorter — never exceed the cap.
