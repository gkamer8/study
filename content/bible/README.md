# Bible verse memorization content (schema v1)

Data for the study site's second subject: well-known verses in the **Douay-Rheims Bible, Challoner revision** (public domain; the traditional Catholic English Bible). 105 items (110 verses) in 8 decks, 210 cards. Each item has two typed drills: text → reference and reference → text. The site code changes needed are in `IMPLEMENTATION.md`. A tested reference implementation of the checker, scorer and cloze is in `_impl/`.

## Files

- `index.json`: subject metadata, sources, the deck list (`units`, same shape as biology so the dashboard works), `books` (alias table), `scoring` (machine-readable copy of the spec below), and every item.
- `NN-<deck>.json`: one per deck: `{unit, slug, title, summary, kind: "verses", items: [...], cards: [...], lesson: "", glossary: [], quiz: []}`.
- `_impl/bible-checker.js`: an ES module with `buildBookIndex`, `parseReference`, `checkReference`, `tokenize`, `alignWords`, `scoreText`, `renderDiff`, `clozeScaffold`. Copy it to `js/bible-checker.js`.
- `_impl/tests.json` and `_impl/bible-checker.test.mjs`: test cases. Run `cd _impl && node bible-checker.test.mjs` (Node 18+). The run checks 23 reference cases, 17 text cases, 5 cloze cases, diff rendering, and every item's own text and references: 527 checks in total.
- `_src/`: the build.
  - `items.py`: the selection, context lines, and numbering overrides.
  - `books.py`: the book table.
  - `scoring_spec.json`
  - `fetch_sources.py`: network; refreshes `sources/`.
  - `build.py`: offline; writes `index.json` and the deck files, and fails on any wording mismatch between the two sources.
  - `usfm.py`: a minimal USFM reader.
  - `sources/`: cached verse text from both sources, plus the WEB verses used only to confirm modern verse numbers.

To rebuild, run `cd _src && python3 build.py`. To refresh the sources first, run `python3 fetch_sources.py`.

## Decks (ordered short → long inside each deck)

| # | slug | title | items |
|---|---|---|---|
| 1 | gospels | Words of Christ | 13 |
| 2 | sermon | Sermon on the Mount (8 Beatitudes, Our Father as one passage) | 15 |
| 3 | psalms | Psalms (Vulgate numbering) | 13 |
| 4 | old-testament | Law, history and wisdom | 12 |
| 5 | prophets | Prophets | 12 |
| 6 | epistles | Epistles | 12 |
| 7 | doctrine | Catholic doctrine and the Mass | 15 |
| 8 | passion | Passion and Resurrection (all Seven Last Words) | 13 |

Decks are sorted by the word count of `recite`. The Beatitudes stay together in canonical order, placed at their average length.

## Item fields

| field | notes |
|---|---|
| `id` | `bible-<deck>-NN`. Cards are `<id>-text` and `<id>-ref`. |
| `ref_drb` | Douay name and Vulgate numbering, e.g. `Psalm 22:1`, `1 Kings 3:10`, `Matthew 6:9–13` (en dash). |
| `ref_modern` | Only when it differs: the modern English book name and RSV/NRSV/ESV/KJV numbering, e.g. `Psalm 23:1`, `1 Samuel 3:10`. |
| `ref_nabre` | Only when NABRE/Hebrew verse numbering differs from both of the above, e.g. `Psalm 51:3`, `Isaiah 9:5`. |
| `book`, `book_drb`, `book_modern` | `book` is a USFM code (e.g. `1SA`), plus both display names. |
| `chapter`, `verse_start`, `verse_end` | DRB numbering. `verses` (a per-verse array) is present only for passages. |
| `numberings` | `[{system: drb\|modern\|nabre, chapter, verse_start, verse_end}]`. Every numbering here counts as correct. |
| `text` | The verse exactly as printed (primary source), including a psalm title or Hebrew acrostic letter if the edition prints one inside the verse. |
| `recite` | What is memorized and scored: `text` minus `recite_prefix`. |
| `recite_prefix` | Present on 4 items: `A psalm for David.` (Ps 22:1), `The psalm of David before he was anointed.` (Ps 26:1), `NUN.` (Ps 118:105), `Lamed.` (Lam 1:12). |
| `word_count` | Tokens in `recite`. |
| `context` | One sentence: who is speaking or the situation. It is the optional hint on the reference → text card. |
| `deck`, `group` | `group` is `beatitudes` for Matt 5:3–10. |
| `accept` | Flat list of accepted reference strings (first entry canonical). Each is a book alias combined with an allowed numbering; for passages, both the starting verse alone and the full range. Compare after reference normalization (below). The structured checker in `_impl` is preferred, and the tests assert that it accepts every `accept` entry. |
| `note` | Shown after every answer when present: Douay vs modern book name, and numbering differences. |
| `source` | Primary source, cross-check source, `crosscheck_status` (`exact` or `reviewed`), and `review_note` when reviewed. |

## Card fields

`{id, item, type: "verse-text"|"verse-ref", direction, front, hint?, answer_form, back, accept?, tags}`

- **verse-text**: `front` is the reference line, e.g. `Psalm 22:1 (Psalm 23:1 in modern Bibles)`. `hint` is the context line. `back` is `recite`.
- **verse-ref**: `front` is `recite`. `back` is the reference line. `accept` lists the accepted references.

## Book alias table (`index.json → books`)

There are 73 entries in Vulgate order: `{usfm, drb, modern, drb_aliases, modern_aliases}`.

- Aliases are normalized keys: lowercase, no spaces or periods, and a leading digit for numbered books.
- Douay names: Josue, 1–4 Kings, 1–2 Paralipomenon, 1–2 Esdras, Tobias, Canticle of Canticles, Ecclesiasticus, Isaias, Jeremias, Ezechiel, Osee, Abdias, Jonas, Micheas, Habacuc, Sophonias, Aggeus, Zacharias, Malachias, 1–2 Machabees, Apocalypse.
- One collision is deliberate: `1kings`/`2kings` resolve to both 1SA/2SA (Douay) and 1KI/2KI (modern). The checker accepts the answer if either book is the item's book.
- Ambiguous short forms were left out: `jud` (Jude or Judith?), `co`, `pp`. `jo` means John (the traditional Catholic abbreviation).

## Reference checker (text → reference)

1. **Normalize the book name.**
   - Strip accents and lowercase.
   - Turn a leading `first/1st/I`, `second/2nd/II`, `third/3rd/III` or `fourth/4th/IV` into a digit (roman numerals only when a book name follows).
   - Drop filler words: `the, book, of, gospel, according, to, saint, st, epistle, letter, holy, prophet, prophecy`.
   - Remove everything that is not a letter.
   - So `St. John` → `john`, `Song of Songs` → `songsongs`, `I Kings` → `1kings`.
2. **Parse.** The input is `<book> <chapter><sep><verse>[-<verse>]`, where `<sep>` is `:`, `.`, `,`, a space, `v` or `vs`. So `John 3 16`, `Jn 3.16`, `Jo 3:16` and `Ps 22:1-6` all parse. Input with no verse is wrong.
3. **Match.** The book must resolve to the item's book. Then, for any entry in `numberings`: the chapter equals, the start verse equals, and the end verse is either omitted or equal. That gives **correct**. Matching under modern or NABRE numbering is also correct, and the `note` explains the Douay number.
4. **Close.** Right book and chapter (under any numbering), verse off by exactly 1. This is graded Hard.
5. **Grades:** correct = Good, or Easy if answered in under 5 s (same rule as the biology cards); close = Hard; wrong or bail = Again. "I was actually right" = Good.

## Text scorer (reference → text)

1. **Tokenize** both `recite` and the input:
   - Unicode NFKD with combining marks stripped, then lowercase.
   - Delete apostrophes (`mother’s` → `mothers`, `justice’` → `justice`).
   - Turn hyphens and dashes into spaces, then every other non-alphanumeric character into a space, and split.
   - Map each token through `scoring.text.spelling_variants`, which covers spelling only, never wording (labour/labor, neighbour/neighbor, saviour/savior, fulness/fullness, shew/show, oh/o, zion/sion, …). Archaic forms are not variants: `hath`≠`has`, `thee`≠`you`, `believeth`≠`believes`, `shalt`≠`shall`. Memorizing the Douay wording is the point.
2. **Align** with word-level Levenshtein. Substitute, insert and delete each cost 1. These cost 0:
   - an exact or variant match
   - a **typo**: the reference token is ≥ 6 letters and Damerau-Levenshtein distance is 1. It is shown amber.
   - a **merge**: two adjacent tokens on one side concatenate to one on the other (`to day` = `today`).
3. **Score:** `score = max(0, 1 − errors / n)`, where n is the number of reference tokens.
4. **Verdict:**
   - **correct** if errors = 0, or (n ≥ 6 and (score ≥ 0.95 or errors ≤ 1)). So verses with fewer than 20 words allow 1 wrong word, and longer verses allow 5%.
   - **close** if score ≥ 0.80, or (n ≤ 5 and errors = 1). Close shows the diff and counts as Hard.
   - **wrong** otherwise.
5. **Always show a word diff** (`renderDiff`). Every printed word of the verse is marked ok, typo, wrong (with what was typed) or missing. Extra typed words are shown struck through where they were typed.
6. **Grades:** correct = Good, close = Hard, wrong or bail = Again. "I was actually right" = Good. Response time is ignored for typed verses.

## Cloze ramp (learning steps for `-text` cards)

The user always types the **whole verse** while looking at the scaffold. A step passes when the text verdict is correct.

| step | scaffold |
|---|---|
| 0 | every 3rd word hidden (`i % 3 == 2`): `Blessed are ___ merciful: for ____ shall obtain _____.` |
| 1 | every other word hidden (`i % 2 == 1`): `Blessed ___ the ________: for ____ shall ______ mercy.` |
| 2 | first letters only, punctuation kept: `B a t m: f t s o m.` |
| 3 | nothing: reference only, with context available as a hint |

Hidden words are drawn as one underscore per letter, capped at 8. A new `-text` card gets its **first FSRS grade only when step 3 passes**: Good if no step failed during the ramp, Hard otherwise. After a review graded Again, the next showing starts at step 2, then step 3, and the step 3 result is the FSRS grade. That is spaced retrieval with fading cues, the standard memorization ramp.

## Provenance and cross-check

- **Primary text:** eBible.org `engDRA` USFM, "The Holy Bible in English, Douay-Rheims American Edition of 1899, translated from the Latin Vulgate", public domain, https://ebible.org/Scriptures/engDRA_usfm.zip, retrieved 2026-11-14. This is the Challoner text. Strong's number tags and footnotes are stripped by `usfm.py`.
- **Cross-check:** drbo.org chapter pages (Douay-Rheims, Challoner revision), `https://www.drbo.org/chapter/BBCCC.htm`, retrieved 2026-11-14.
  - Only the verse text is used for comparison. The Challoner notes that follow a chapter's last verse are cut off.
  - `build.py` requires the memorized words (`recite`) to be identical, word for word, in both sources, and stops otherwise.
  - Result: 104 of 105 items are character-identical in both sources (apostrophe style aside). The remaining one (Ps 118:105) is `reviewed`: eBible prints the acrostic letter `NUN.` inside the verse and drbo.org prints it as a heading. Its `recite` is identical in both.
  - No text came from any other translation.
- **Modern numbering check:** eBible.org `eng-web` (World English Bible, public domain). It was used only to confirm which modern verse number holds the same content (e.g. 2 Maccabees has no 12:46 in modern numbering; the Douay 12:46 is 12:45). None of its wording is used.

## Numbering and naming gotchas handled

- **Psalms** use the Greek/Vulgate numbers, usually one lower than Hebrew/modern from Ps 10 to Ps 147. Douay verse numbers also count the psalm title as verse 1 when there is one, so the English (RSV/KJV) verse is often 1–2 lower. NABRE keeps the title verses, so it differs again. Example: the Miserere's opening line is Ps 50:3 (Douay) = Ps 51:1 (RSV/KJV) = Ps 51:3 (NABRE). All three are accepted.
- **Ps 94:8** (Douay) spans modern Ps 95:7c–8. `95:7`, `95:8` and `95:7-8` are all accepted.
- **Beatitudes:** the Vulgate puts "the meek" before "they that mourn". So Douay Matt 5:4 (meek) = modern 5:5, and Douay 5:5 (mourn) = modern 5:4.
- **John 6:** from verse 52 the Vulgate is one higher. Douay John 6:54 ("Except you eat the flesh…") = modern 6:53, and 6:56 = 6:55.
- **2 Thess 2:14** (hold the traditions) = modern 2:15. **2 Machabees 12:46** = modern 12:45.
- **Isaias 9:6** matches the RSV/KJV number, but the NABRE (Hebrew numbering) has 9:5.
- **Books:** Douay 1 Kings = 1 Samuel, and Douay 3 Kings = modern 1 Kings. The deck includes 3 Kings 19:12 (Elias and the "whistling of a gentle air") and 1 Kings 3:10 (Samuel) to exercise both. Other renamed books in the deck: Canticle of Canticles, Isaias, Jeremias, Ezechiel, Micheas, 2 Machabees.
- **Text quirks kept as printed:** small capitals rendered as capitals (`For a CHILD IS BORN to us`, `I AM WHO AM`), and `said Ecclesiastes vanity of vanities` without a comma. Both sources agree on these, and the scorer ignores case and punctuation.
