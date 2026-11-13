# Biology study content

Content for the spaced-repetition study site. This folder holds only data; the site code lives elsewhere.

## Files

- `index.json`: subject metadata plus the ordered list of units (file, counts, prerequisites).
- `NN-slug.json`: one file per unit.
- `_src/`: Python generators (`uN.py` + `common.py`). Edit these and run `python3 _src/uN.py` to regenerate a unit file. They assign IDs, validate types, and deterministically shuffle quiz choices.

## index.json

```json
{
  "subject": "biology",
  "title": "...",
  "description": "...",
  "schema_version": 1,
  "generated": "YYYY-MM-DD",
  "units": [
    {"unit": 1, "slug": "central-dogma", "title": "...", "summary": "...",
     "file": "01-central-dogma.json", "card_count": 42, "quiz_count": 13,
     "prerequisites": []}
  ],
  "totals": {"cards": 0, "quiz": 0}
}
```

`prerequisites` lists unit numbers worth finishing first. Use it for suggested ordering only; don't enforce it.

## Unit file

| Field | Type | Notes |
|---|---|---|
| `unit` | int | 1-based order |
| `slug` | string | URL-safe identifier |
| `title` | string | |
| `summary` | string | 2–4 sentences |
| `lesson` | string | Markdown primer (600–1200 words). Uses GFM tables, fenced code, `^...^` superscripts in a few places (e.g. `p16^INK4a^`, `Kras^LSL-G12D^`); render them as `<sup>` or leave as-is |
| `cards` | array | flashcards (below) |
| `quiz` | array | multiple-choice questions (below) |

### Card

```json
{"id": "u2-c29", "front": "In HGVS c. numbering, what is c.1?",
 "back": "The A of the ATG start codon", "tags": ["HGVS"], "type": "recall"}
```

- `id`: stable, `u<unit>-c<NN>`. Key spaced-repetition state on this ID. Appending new cards to the end of a generator keeps existing IDs stable; inserting in the middle renumbers everything after it.
- `type`:
  - `recall`: question → answer.
  - `cloze`: `front` contains `___` blanks; `back` gives the fill(s), separated by `;` or `…` when there are several.
  - `identify`: `front` is an identifier, symbol, or notation (e.g. `NM_000546`, `HLA-DRB1*15:01`); `back` says what it is.
  - `apply`: a short scenario that needs reasoning.
- `tags`: free-form topic tags for filtering and drill modes.

All cards are self-graded (show the answer, rate Again/Hard/Good/Easy). Answers are short, so a typed-answer mode would need fuzzy matching.

### Quiz question

```json
{"id": "u1-q02", "question": "...", "choices": ["a","b","c","d"],
 "answer_index": 2, "explanation": "..."}
```

- Always exactly 4 choices; `answer_index` is 0-based.
- Choices are already shuffled once at generation time, but the site should still shuffle at display time (remapping `answer_index`). Explanations never refer to choice letters or positions.
