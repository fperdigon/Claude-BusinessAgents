# Blog Article Prompt (Sonnet sub-agent)

<voice-anchor>

---

## Task

Write a personal blog article based on the following parameters. The article must read like the same person who wrote the bio exemplar in the Voice Anchor — same tone, same rhythm, same level of specificity.

## Parameters

- **Topic + angle:** <post-title>
- **Word target:** <word-target> (the user picked one of: 800 / 1200 / 1500)
- **Audience:** <article-audience>
  - **peers/practitioners** — assume domain knowledge; you can use jargon without defining it
  - **decision-makers** — translate technical trade-offs into business outcomes (cost, risk, time)
  - **general public** — define every jargon term inline the first time it appears
- **Section style:** <article-style>
  - **how-to** — numbered steps, each step has a brief example or rationale
  - **opinion** — argument with the strongest counterargument addressed in its own section
  - **case study** — story arc (situation → action → result → lesson)
- **Closing:** <article-close>
  - **takeaway list** — bulleted summary, 3–5 items
  - **call-to-discussion** — one or two open questions inviting the reader to respond
  - **related resources** — list of 3–5 further-reading items (label them `[your link to X]` — do not invent URLs)
- **Optional linked context:** <linked-context>

## Article structure

Every article has:

1. **Title** — punchy, specific, ≤80 chars. Should make a SERP click obvious.
2. **Subtitle** — one line that completes the promise of the title (~120 chars).
3. **Intro** — 100–150 words. Sets up the problem or claim, hints at the resolution. Specific from the first sentence — no "in today's fast-paced world" openers.
4. **3–5 body sections (`H2` headings)** — each section has a heading and 150–400 words of body text, depending on word target. Headings are scannable: a reader who reads only the headings should understand the spine of the argument.
5. **Conclusion** — one paragraph (60–120 words). Ties back to the intro's promise, then transitions into the closing per `<article-close>`.

## Style rules per audience

- **peers/practitioners** — code or examples are fine; assume the reader knows the field. Cite specific tools, papers, or frameworks by name. No remedial explanations.
- **decision-makers** — every technical claim is followed by its business implication. Use a sentence pattern like "X means Y for the team's [cost / risk / time]." Avoid raw code; use prose-level descriptions.
- **general public** — define jargon parenthetically the first time. Use analogies from everyday life. Keep paragraphs ≤4 lines on a phone.

## Section style rules

- **how-to** — section headings are imperative ("Validate the input first"). Each section opens with what the step accomplishes, then how, then a quick gotcha. Numbered list optional inside sections.
- **opinion** — section headings are claims ("Type-checking is overkill for one-off scripts"). Include one section explicitly titled around the strongest counterargument, then address it directly.
- **case study** — section headings are narrative beats ("The migration we thought was safe", "What broke at 3am", "What we changed"). Use the persona's pronoun consistently.

## Cover image prompt

Write a single-sentence prompt for image generators (Midjourney / DALL-E / Firefly / Stable Diffusion). Use only **descriptive color words** — never hex codes. Examples of descriptive words: "warm amber accents," "deep navy gradient," "muted forest green and parchment." Pull the colors from the persona brand palette.

The prompt should describe a scene that conceptually relates to the article (no people unless the article style explicitly requires a portrait).

## Hard constraints

- **Word count must be within ±15% of <word-target>.** Count words by whitespace-split.
- **3–5 H2 sections.** Not fewer than 3, not more than 5.
- **Forbidden phrases:** never include any phrase listed as forbidden in the Voice Anchor.
- **No hex codes in `cover_prompt`.** Only descriptive color words.
- **No invented URLs.** Use placeholder text like `[your link to X]` for any user-supplied resources.
- **Pronoun discipline:** stick to whichever pronoun is set in the Voice Anchor for the entire article.

## Output

Return a single JSON object (no prose, no fences):

```json
{
  "title": "<title>",
  "subtitle": "<subtitle>",
  "intro": "<intro paragraph(s)>",
  "sections": [
    {"heading": "<H2 heading 1>", "body": "<section body text with paragraph breaks as \\n\\n>"},
    {"heading": "<H2 heading 2>", "body": "..."},
    {"heading": "<H2 heading 3>", "body": "..."}
  ],
  "conclusion": "<closing paragraph + closing-style content per <article-close>>",
  "cover_prompt": "<single-sentence image prompt with descriptive color words only>",
  "word_count": <integer count>
}
```
