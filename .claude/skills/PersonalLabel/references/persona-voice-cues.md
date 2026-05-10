# Persona Voice Cues

Lookup tables used by `persona_marketing` to translate `Voice & Tone Signals` from `persona-context.md` into prompt instructions for the Sonnet content sub-agent. Persona Brand also reads this for the brand guidelines voice section.

## Tone adjective → writing instruction

When the persona's tone adjectives are listed, expand each to a one-line writing instruction in the Sonnet prompt's Voice Anchor block.

| Adjective | Writing instruction |
|---|---|
| direct | State the claim first; cut hedges; avoid throat-clearing phrases. |
| warm | Address the reader as "you"; include one human-relatable line per post. |
| technically precise | Use the correct term; never approximate jargon; show numbers when stated. |
| analytical | Lead with a thesis; support with evidence; close with implication. |
| reflective | Allow short narrative beats; one personal observation per post is fine. |
| bold | Stake a position; willing to disagree with prevailing views. |
| playful | One light moment per post; never at the expense of accuracy. |
| scholarly | Cite sources or named frameworks; full sentences over fragments. |
| approachable | Define jargon in-line the first time it appears. |
| pragmatic | Show the trade-off; never promise without caveats. |
| confident | No "I think" or "maybe"; assert and let the reader push back. |
| curious | Frame at least one open question; don't pretend to closure. |
| measured | Avoid superlatives; let evidence carry the weight. |
| irreverent | Light sarcasm OK; never about people, only about ideas. |

For adjectives not listed, the sub-agent should infer from analogous entries.

## Sentence rhythm → structure rule

| Rhythm | Structure rule |
|---|---|
| short/punchy | Average sentence ≤14 words; no clause stacking; line breaks frequent. |
| balanced | Mix 8–24 word sentences; one clause-stacked sentence per paragraph max. |
| reflective | 18–32 word sentences allowed; one or two per post may exceed. |

## Emoji policy → enforcement

| Policy | Enforcement |
|---|---|
| none | Zero emojis in any post. Hard rule. |
| sparing | At most 1 emoji in the hook OR in the CTA, never both. |
| expressive | Up to 3 emojis per post, never more than 1 per paragraph. |

## Hashtag policy → enforcement

| Policy | Enforcement |
|---|---|
| none | Zero hashtags. |
| 1–3 per post | Exactly 1 to 3, placed at the end as a single line. |
| many | 4 to 8 allowed, end of post, single line. |

## Pronoun → enforcement

| Pronoun | Enforcement |
|---|---|
| I | First person singular only. Never use "we." |
| we | First person plural ("we"/"our") for the brand voice. Acceptable on collective work. |
| mixed | "I" for personal experience, "we" for collaborative claims. |

## Voice Anchor block (template for marketing prompts)

Persona marketing prompts should always start with a block built like this:

```
## Voice Anchor

You are writing as [Full Name], whose voice signals are:

- Tone: [adjectives]
  → [writing instruction per adjective, joined by line breaks]
- Sentence rhythm: [rhythm]
  → [structure rule]
- Emoji: [policy] → [enforcement]
- Hashtags: [policy] → [enforcement]
- Pronoun: [pronoun] → [enforcement]
- Forbidden phrases: do not use any of: [comma list, or "none specified"]

Style exemplars (write in this register):
> [bio_short from persona-context]

[If long bio is present, append:]
> [first sentence of bio_long]
```

## Forbidden phrase handling

If the persona lists forbidden phrases in `persona-context.md`, the marketing skill must:
1. Pass the list verbatim into the Voice Anchor block.
2. After the sub-agent returns content, scan output for any forbidden phrase (case-insensitive). If any appear, dispatch a one-shot retry asking the sub-agent to rewrite removing those phrases.
