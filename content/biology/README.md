# Biology study content (schema v4)

Content for the spaced-repetition study site. This folder holds only data; the site code lives elsewhere.

## Files

- `index.json`: subject metadata, a changelog, and the ordered list of units with counts and suggested prerequisites.
- `NN-slug.json`: one file per unit.
- `figures/`: lesson figures (SVG diagrams, one PNG photo), referenced from the lessons as `content/biology/figures/<file>`. Filenames use only lowercase letters, digits and hyphens.
- `_src/`: generators. Each unit is built from three sources:
  - `lessons/uN.md`: the lesson Markdown
  - `cards_uN.py`: the flashcards
  - `uN.py`: metadata and quiz questions; it also calls `common.build`

  - `glossaries.py`: the source of every lesson's Key terms block. Run `python3 glossaries.py` to write the blocks into `lessons/uN.md`

  Edit those, then run `cd _src && python3 uN.py` to regenerate. `common.py` assigns IDs, validates fields, extracts the glossary, dedupes `accept` entries, and shuffles quiz choices. After changing counts, regenerate `index.json` too.

## index.json

```json
{
  "subject": "biology", "title": "...", "description": "...",
  "schema_version": 4, "generated": "YYYY-MM-DD", "changes": ["..."],
  "units": [
    {"unit": 1, "slug": "central-dogma", "title": "...", "summary": "...",
     "file": "01-central-dogma.json", "card_count": 80, "quiz_count": 13,
     "glossary_count": 38, "lesson_words": 2609, "prerequisites": [],
     "figure_count": 7}
  ],
  "totals": {"cards": 456, "quiz": 100, "glossary_terms": 200, "figures": 33}
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
| `glossary` | array of `{term, definition, accept}` | Same content as the lesson's Key terms list, pre-parsed. Use it for tooltips, a glossary page, and the Terms drill (show `definition`, the user types the term, check against `accept`) |
| `lesson` | string | Markdown, ~1,450–2,000 words. See the glossary convention below |
| `cards` | array | flashcards |
| `quiz` | array | multiple-choice questions |

### Lesson / glossary convention

- Every lesson **starts** with a `### Key terms` heading, then a bullet list with **one term per bullet**, then a blank line. Bullets look like `- **Term**: definition` or `- **Term (ABBR)**: definition`.
- Glossary `accept` is built automatically from the term, the parenthesized abbreviation, and a simple plural, plus extra variants listed in `glossary_accept` in `cards_uN.py`.
- `common.py` enforces that each definition points to exactly one term: terms and definitions are unique within a unit, and no definition contains its own term or any accepted variant of 3+ characters. Each unit is self-contained for the drill; the same term may appear again in a later unit with a "(see Unit N)" note.
- In the body, each technical term is defined in plain words where it first appears, usually bolded. Terms that belong to another unit are briefly re-defined or marked "(see Unit N)". The site can turn "Unit N" into a link.
- Lesson Markdown uses GFM tables, fenced code blocks, and a few `^...^` superscripts (e.g. `p16^INK4a^`). Render those as `<sup>` or leave them as plain text.

### Figures

Each figure is one Markdown paragraph: an image line, then a caption line.

```
![Alt text describing what the figure shows.](content/biology/figures/u4-domains.svg)
**Figure 4.3.** What to notice, in the lesson's own terms. Credits and links for real images go here.
```

- Render a paragraph whose first line is a lone image as `<figure><img src alt loading="lazy"><figcaption>…</figcaption></figure>`; the caption may contain inline Markdown (bold, links, `\*` escapes). Image `src` paths are relative to the site root.
- Alt text and captions can contain `_` inside words (NM_000546.6) and `*` in alt text, so the renderer must handle images, links and code before emphasis, and treat `_` as emphasis only at word boundaries. A drop-in `js/markdown.js` that does this was delivered with v4.
- Figures are drawn on a white background at 720 px wide (viewBox, so they scale); use `max-width: 100%`.
- Sources: `_src/figures/`. `figlib.py` is a tiny SVG writer (palette, arrows, boxes, monospace grids), `uN_figs.py` draws each unit's figures, `build_all.py` writes them all into `figures/`, `render.py` renders PNGs for checking, and `placements.py` inserts the figure blocks (alt text, captions, position) into `lessons/uN.md` (idempotent). `data/` holds the AlphaFold p53 data used by `u4-alphafold-p53.svg` (CC-BY 4.0).
- Rebuild: `python3 -m venv /workspace/figenv && /workspace/figenv/bin/pip install cairosvg pillow numpy`, then `cd _src/figures && /workspace/figenv/bin/python build_all.py && python3 placements.py`, then regenerate the units (`cd .. && python3 uN.py`). Only `render.py` needs cairosvg; `build_all.py` needs numpy and pillow (AlphaFold panel, karyotype labels) and the Liberation Sans fonts (`fonts-liberation`), which `figlib.tw()` uses to measure label widths.
- Real images: `u1-karyotype.png` (NHGRI, public domain, Wikimedia Commons). Data-derived: `u4-alphafold-p53.svg` (AlphaFold DB AF-P04637-F1 v6, CC-BY 4.0). Everything else is drawn for this site; feature coordinates come from UniProt, InterPro, QuickGO, NCBI/Ensembl and UCSC (GRCh38).

### Card

```json
{"id": "u1-c55", "front": "Term: one copy of each chromosome, as in eggs and sperm. (one word)",
 "back": "Haploid (n)", "accept": ["haploid", "1n", "n"],
 "tags": ["basics", "ploidy"], "type": "recall"}
```

- `id`: stable, `u<unit>-c<NN>`. Key spaced-repetition state on it. Every v1/v2 ID still tests the same fact. When a card was split, the original ID kept the first part and the other parts got new IDs appended at the end (in `cards_uN.py` they sit in `splits`). Always append; never insert or reuse an ID.
- `front`: the prompt. As of v3, every prompt has exactly one unambiguous answer of at most ~4 words, and ends with the **expected form in parentheses**, e.g. `(gene symbol)`, `(one word)`, `(letter)`, `(number, in Gb)`, `(5' or 3')`, `(yes/no)`. No answer depends on formatting, ordering, or separators. Comparisons and lists are split into separate cards.
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
