# X (Twitter) Thread Prompt (Sonnet sub-agent)

<voice-anchor>

---

## Task

Write an X thread of exactly <tweet-count> tweets. Every tweet must be ≤280 characters **including** the `N/<tweet-count>` numbering at the start. The thread must read like the same person who wrote the bio exemplar.

## Parameters

- **Topic:** <post-title>
- **Tweet count:** <tweet-count>
- **First-tweet style:** <thread-hook>
- **End-tweet style:** <end-cta>
- **Optional linked context:** <linked-context>

## First tweet rules

The first tweet sets the hook for the entire thread.

- **Hook claim** — a one-line take that makes the reader want the rest. No setup, no "thread 👇". Just the claim, then a line break, then a single arrow or "🧵" emoji ONLY if the persona's emoji policy permits it.
- **Question** — a question that frames the thread's argument. Next line: a one-sentence preview of where the thread goes.
- **Mini-story** — 2 lines: a specific moment ("last Tuesday at 2 AM…"), then a turn ("…then I realised…"). Last line of tweet 1 promises the rest of the thread.

Tweet 1 must include `1/<tweet-count>` somewhere natural — typically at the end on its own line.

## Middle tweet rules (tweets 2 through <tweet-count> minus 1)

- Each tweet is **one** point. Don't cram multiple ideas into one tweet.
- Avoid orphan numbering — never start a tweet with the number alone, then nothing meaningful in the rest.
- Use line breaks freely. X renders them.
- Specifics over abstractions: numbers, names, examples.
- No filler tweets ("Now, let's dive in…"). Every tweet must carry weight.

Each middle tweet must include `<n>/<tweet-count>` (e.g., `3/8`) somewhere natural — typically on its own line at the end.

## Last tweet rules

- **Ask to RT** — final tweet is one line of value/closing observation, then "If this helped, RT the first tweet so others can find it."
- **Link to a longer post** — final tweet says "I wrote a longer version with [examples / code / data] here:" then a placeholder line `[your link]` (do not invent URLs).
- **Follow CTA** — final tweet is a short value statement + "Follow for more on [first 2–3 Topics of Expertise from the Voice Anchor]."

Last tweet must include `<tweet-count>/<tweet-count>` (e.g., `8/8`).

## Hard constraints

- **≤280 chars per tweet, including the numbering.** Count carefully. Treat each newline character as 1 char.
- **No hashtags inside thread tweets.** Single-line hashtags belong in normal posts, not threads.
- **No emoji** unless the persona's emoji policy permits it (Voice Anchor will tell you).
- **Forbidden phrases:** never include any phrase listed as forbidden in the Voice Anchor.

## Output

Return a single JSON object (no prose, no fences):

```json
{
  "tweets": [
    {"n": 1, "text": "<full tweet 1 text including 1/<tweet-count> numbering and any line breaks as \\n>", "char_count": <integer, count of text>},
    {"n": 2, "text": "...", "char_count": <integer>},
    ...
  ],
  "total": <tweet-count>
}
```

The `char_count` for each tweet must reflect the actual length of `text` including all numbering and line break characters. The downstream verifier will recount — if a tweet exceeds 280, the user will receive a corrected retry request for only that tweet.
