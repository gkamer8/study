# Biology study content (schema v2)

Content for the spaced-repetition study site. This folder holds only data; the site code lives elsewhere.

## Files

- `index.json`: subject metadata, a changelog, and the ordered list of units with counts and suggested prerequisites.
- `NN-slug.json`: one file per unit.
- `_src/`: generators. Each unit is built from three sources:
  - `lessons/uN.md`: the lesson Markdown
  - `cards_uN.py`: the flashcards
  - `uN.py`: metadata and quiz questions; it also calls `common.build`

  Edit those, then run `cd _src && python3 uN.py` to regenerate. `common.py` assigns IDs, validates fields, extracts the glossary, dedupes `accept` entries, and shuffles quiz choices. After changing counts, regenerate `index.json` too.

## index.json

```json
{
  "subject": "biology", "title": "...", "description": "...",
  "schema_version": 2, "generated": "YYYY-MM-DD", "changes": ["..."],
  "units": [
    {"unit": 1, "slug": "central-dogma", "title": "...", "summary": "...",
     "file": "01-central-dogma.json", "card_count": 74, "quiz_count": 13,
     "glossary_count": 28, "lesson_words": 2021, "prerequisites": []}
  ],
  "totals": {"cards": 437, "quiz": 100, "glossary_terms": 161}
}
```

`prerequisites` lists units worth reading first. It is advisory only. Lessons re-define or cross-reference ("see Unit N") every term they rely on, so any unit can be read on its own.

## Unit file

| Field | Type | Notes |
|---|---|---|
| `unit` | int | 1-based order |
| `slug` | string | URL-safe identifier |
| `title` | string | |
| `summary` | string | 2–4 sentences |
| `glossary` | array of `{term, definition}` | Same content as the lesson's Key terms list, pre-parsed. Use it for hover tooltips, a glossary page, or a terms drill |
| `lesson` | string | Markdown, ~1,450–2,000 words. See the glossary convention below |
| `cards` | array | flashcards |
| `quiz` | array | multiple-choice questions |

### Lesson / glossary convention

- Every lesson **starts** with a `### Key terms` heading, then a bullet list in the form `- **Term**: one-line plain-language definition.`, then a blank line. `common.py` enforces this.
- In the body, each technical term is defined in plain words where it first appears, usually bolded. Terms that belong to another unit are briefly re-defined or marked "(see Unit N)". The site can turn "Unit N" into a link.
- Lesson Markdown uses GFM tables, fenced code blocks, and a few `^...^` superscripts (e.g. `p16^INK4a^`). Render those as `<sup>` or leave them as plain text.

### Card

```json
{"id": "u1-c55", "front": "Term: one copy of each chromosome (as in eggs and sperm).",
 "back": "Haploid (n)", "accept": ["haploid", "1n", "n", "monoploid"],
 "tags": ["basics", "ploidy"], "type": "recall"}
```

- `id`: stable, `u<unit>-c<NN>`. Key spaced-repetition state on it. v2 kept every v1 ID on the same topic (some cards were reworded so the answer is typeable) and appended new cards after the old ones. Always append; never insert.
- `front`: the prompt. It asks for something short: a term, ID, number, or a few words.
- `back`: the canonical answer plus a short explanation. Show it after every attempt, right or wrong.
- `accept`: acceptable typed answers. The **first entry is the canonical short answer** (use it for "the answer was…"), followed by synonyms, abbreviations and alternate spellings. Entries are already deduped case-insensitively.
- `type`: `recall` (question → answer), `cloze` (`front` contains `___`), `identify` (an ID, symbol or notation → what it is), or `apply` (a short scenario).
- `tags`: topic tags. `basics` marks the foundational vocabulary cards added in v2.

**Suggested answer checking** (both the typed answer and each `accept` entry get normalized the same way):

1. Lowercase, trim, and collapse whitespace.
2. Unify look-alike characters: ’ ′ → `'`; → and -> → `to`; en/em dashes → `-`; Greek letters → their names (α → alpha, β → beta, κ → kappa, ρ → rho); `Å` → `a`.
3. Strip surrounding punctuation and a leading article ("the", "a", "an").
4. Correct if the result equals any normalized `accept` entry. Also try removing all spaces, hyphens and dots from both sides, so "dbSNP" = "db snp" and "k-mer" = "kmer".
5. Optionally allow a typo (Levenshtein distance ≤ 1 for answers of 6+ characters). Don't allow typos for IDs, gene symbols, or answers of 3 characters or fewer: "K" vs "R", or "CDK1" vs "CDK2", must be exact.
6. Always offer "I don't know / show answer" (counts as a fail) and "I was right" (override, for valid answers the list misses).

### Quiz question

```json
{"id": "u1-q02", "question": "...", "choices": ["a","b","c","d"],
 "answer_index": 2, "explanation": "..."}
```

Always exactly 4 choices; `answer_index` is 0-based. Choices are shuffled once at generation time. The site should shuffle again at display time (remapping `answer_index`). Explanations never refer to choice letters or positions.
