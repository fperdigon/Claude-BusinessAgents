# Persona Synthesis Prompt (Sonnet sub-agent)

You are synthesising a person's professional profile from a mix of raw sources. Your job is to fill the persona-context schema as precisely and conservatively as possible. Do not invent details — leave fields with `[not specified]` if the inputs do not support them.

## Inputs

### CV (raw text)
<cv-raw>

### LinkedIn (fetched or pasted)
<linkedin-text>

### Personal website (fetched)
<website-text>

### GitHub (fetched)
<github-summary>

### User's positioning sentence
<positioning-sentence>

### User's audience description
<audience-input>

### User's 12-month goals
<goals-input>

### User's off-limits / constraints
<off-limits-input>

## Your task

Return a single JSON object (and nothing else — no prose, no fences, no commentary) with these keys:

```json
{
  "full_name": "string",
  "headline": "string (≤120 chars)",
  "bio_short": "string (≤280 chars)",
  "bio_long": "string (600–800 chars)",
  "skills_primary": ["string", "..."],
  "skills_secondary": ["string", "..."],
  "experience": [
    {"role": "string", "company": "string", "years": "string", "impact": "string (one line)"}
  ],
  "topics_of_expertise": ["string", "...", "5 to 8 items"],
  "voice_tone_adjectives": ["string", "...", "3 to 5 items"],
  "voice_sentence_rhythm": "short/punchy | balanced | reflective",
  "voice_emoji_usage": "none | sparing | expressive",
  "voice_hashtag_usage": "none | 1-3 per post | many",
  "voice_pronoun": "I | we | mixed",
  "voice_forbidden_phrases": ["string", "..."] ,
  "audience_primary": "string",
  "audience_secondary": "string",
  "goals": ["string", "..."],
  "constraints": ["string", "..."],
  "source_summary": {
    "cv": "provided | not provided",
    "linkedin": "fetched | pasted manually | not provided",
    "website": "fetched | not provided",
    "github": "fetched | not provided"
  }
}
```

## Synthesis rules

- **Conservative inference:** if a field has no support in the inputs, return `"[not specified]"` for strings or `[]` for lists. Do not guess job titles, dates, or skills the user has not stated.
- **Headline:** must be ≤120 chars. Anchor it on the user's positioning sentence (Q5), refined with verb + audience + outcome. Example shape: *"[Role] helping [audience] achieve [outcome] through [approach]."*
- **Voice signals:** infer from the *style* of the user's CV, LinkedIn About, and website. If the writing is short/declarative → `short/punchy`. If it leans on stories → `reflective`. If neither dominates → `balanced`. Match emoji and hashtag usage to whatever appears in their actual posts/profile, not what you think they should use.
- **Topics of expertise:** synthesise from the intersection of CV skills, GitHub languages/repos, and the user's stated audience and positioning. 5–8 items. Each topic should be specific enough to anchor a content pillar (e.g., "Python type systems for data engineers," not just "Python").
- **Bio (short and long):** write in the persona's pronoun (Q5/voice signals tell you which). The short bio fits in social profiles (≤280 chars). The long bio is for an About page and should mention current focus, signature expertise, and (if stated) at least one named achievement.
- **Skills primary vs secondary:** primary = the skills the user could lead a project on or charge for. Secondary = strong supporting skills. Do not exceed 8 items in either list.
- **Forbidden phrases:** include only items the user explicitly listed in Q8. Otherwise return `[]`.
- **Experience:** most recent 4 roles only, in reverse chronological order. If fewer than 4 are visible, return what exists.

Return ONLY the JSON object.
