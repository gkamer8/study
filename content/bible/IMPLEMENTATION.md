# Implementation spec: Bible subject (site code)

Target repo: `gkamer8/study`, a static ES-module site with no build step. Copy this folder to `content/bible/`. Keep the `_src/` and `_impl/` folders; they are harmless when served. Data shapes are in `README.md`.

## 0. Files to add or change

| file | change |
|---|---|
| `content/subjects.json` | add `{"id": "bible", "title": "Bible verses (Douay-Rheims)", "description": "Memorize well-known verses in the traditional Catholic English Bible", "path": "bible"}` |
| `js/bible-checker.js` | copy `content/bible/_impl/bible-checker.js` unchanged |
| `js/storage.js` | new key `CLOZE: 'study_cloze_state'` with `getCloze(id)`, `setCloze(id, state)` and `clearCloze(id)`. Include it in `exportData` (`cloze`), `importData` and `clearAllData` |
| `js/app.js` | verse card renderers, queue rules, and subject page links (below) |
| `css/style.css` | a few classes for the diff and scaffold (below). Match the existing dense style: no hover effects, no decoration |

Nothing in `spaced-repetition.js` changes. Bible cards are ordinary cards in `unit.cards`, keyed by id in `study_card_progress`. The two directions are separate cards: `<item>-text` and `<item>-ref`.

## 1. Loading

`index.json` has `units` with `file`, `card_count` and so on, so `renderDashboard` and `renderReview` pick up the decks unchanged. `unit.lesson`, `glossary` and `quiz` are empty, and `index.totals.quiz` is 0. Each deck file also has `items`. Build lookups once per subject load:

```js
import { buildBookIndex, checkReference, scoreText, renderDiff, clozeScaffold } from './bible-checker.js';
const bookIndex = buildBookIndex(index.books);          // once
const itemsById = Object.fromEntries(index.items.map(i => [i.id, i]));
// card.item -> itemsById[card.item]
```

Cache `index.json` per subject. `renderDashboard` already fetches every unit file; that is fine for 8 small files.

## 2. Subject page (`#/subject/bible`)

When `index.kind === 'verses'`, render the deck list in the same table style as biology, but with these links per deck instead of Lesson / Quiz / Match / Terms:

- **Review**: `#/review/bible/<slug>` runs both directions, using the existing route and queue.
- **Verse → reference**: `#/verses/bible/<slug>/ref` runs only the `-ref` cards of that deck (due ones first, then new).
- **Reference → verse**: `#/verses/bible/<slug>/text` runs only the `-text` cards.
- **Browse**: `#/verses/bible/<slug>/list` is a read-only table of `ref_drb`, `ref_modern`, `context` and `recite`. It is useful before learning.

The header line shows `index.totals.items` verses and `index.totals.cards` cards, plus a one-line note: "Douay-Rheims (Challoner). Psalms use Vulgate numbering; modern numbers are accepted too."

Add the route `this.router.on('/verses/:subjectId/:unitSlug/:mode', p => this.renderVerseDrill(p.subjectId, p.unitSlug, p.mode))`. `renderVerseDrill` builds a queue the same way `renderReview` does, filtered by `card.type`, and calls `startReviewSession`.

## 3. Dispatch inside `startReviewSession`

In `render()`, before the `typedMode` branch:

```js
if (card.type === 'verse-ref')  return this.renderVerseRefCard(card, ctx);
if (card.type === 'verse-text') return this.renderVerseTextCard(card, ctx);
```

`ctx` carries `currentIndex`, `queue.length`, `onNext()`, `onGraded(grade)` (which updates sessionStats and calls `this.gradeCard(card, grade)`), and the session's Esc handling. Verse cards are always typed, even when the `typedAnswers` setting is off.

The existing global Esc handler grades the current card Again. For verse-text cards in a cloze step it must not call `gradeCard`. Either let the verse renderers own Esc and have the session handler skip verse cards, or check a `ctx.handlesEsc` flag.

## 4. Queue rules for verse cards

Apply these in `renderReview` and `renderVerseDrill` after the due and new lists are built:

1. **New `-ref` cards wait for their sibling.** A new `<item>-ref` card is eligible only if `<item>-text` already has a progress record (it has graduated from the cloze ramp). Otherwise the `-ref` card's front, the verse text, would be a first exposure without any learning.
2. **Siblings in the same session.** If both `-text` and `-ref` of an item are in the queue, put `-text` first and move `-ref` to the end of the queue. That way the reference isn't answered right after seeing it.
3. **Order of new cards** follows deck order (short → long), which is the card order in the files. `newCardsPerDay` counts cards, so it counts each `-text` cloze run as one.
4. **Unfinished cloze runs resume.** A `-text` card in the ramp has no progress record (it is still "new"), so `getNewCards` keeps returning it. `study_cloze_state` stores the step to resume at.

## 5. `renderVerseRefCard` (text → reference)

Layout, top to bottom:

- `Verse → reference · <deck title> · n / N`
- The verse (`card.front`, which is the item's `recite`), escaped, in the normal body font.
- A single-line input with placeholder `book chapter:verse, e.g. John 3:16`. Enter submits; Esc is "I don't know".

On submit, `r = checkReference(input, item, bookIndex)`:

| r.verdict | show | grade |
|---|---|---|
| correct | "Correct", then the canonical reference line `card.back` | 3 if answered in under 5000 ms, else 2 (same as the biology typed cards) |
| close | "Close: right chapter, verse off by one", then `card.back` | 1 |
| wrong | "Not quite", then `card.back`. If `r.reason === 'unparsed'`, add "Type book chapter:verse." | 0 |
| bail (Esc or "I don't know" button) | `card.back` | 0 |

Always show `item.note` under the answer when present (Douay vs modern name and numbering). Also show `item.context` in small text after answering.

When the verdict is not correct, offer an **"I was actually right"** button (it regrades to 2). It must replace the earlier grade, not add a second review: call `gradeCard` only once, when the user presses Next or the override.

Enter on the result screen goes to Next.

## 6. `renderVerseTextCard` (reference → text)

### State

```js
const prog = Storage.getCardProgress(card.id);           // null => new
let cloze = Storage.getCloze(card.id);                   // {step, failed} or null
if (!prog && !cloze) cloze = {step: 0, failed: false};   // brand-new card: start the ramp
// cards whose last grade was Again carry {step: 2, failed: false}, set in step 6.4
const step = cloze ? cloze.step : 3;                     // reviews without cloze state are full recall
```

### Layout

- `Reference → verse · <deck title> · n / N`, plus `· Learning step k/4` when `cloze` is set.
- The reference line (`card.front`), e.g. `Psalm 22:1 (Psalm 23:1 in modern Bibles)`.
- A small "Show context" link that reveals `card.hint`. In steps 0–2 the context is shown automatically. Revealing it in step 3 does not change the grade.
- The scaffold line (steps 0–2): `clozeScaffold(item.recite, step)` in the body font with `white-space: pre-wrap`. Underscores render as-is.
- A `<textarea rows=3>`, full width, with `spellcheck=false` and `autocapitalize=off`. Enter submits; Shift+Enter inserts a newline; Esc means "I don't know".

### On submit

Compute `s = scoreText(input, item.recite, index.scoring)` and `d = renderDiff(item.recite, s.ops, index.scoring)`.

Show the verdict (Correct / Close / Not quite), `Math.round(s.score*100)%`, and the diff:

- `ok` words are plain.
- `typo` words get class `.vt-typo` (amber).
- `wrong` and `missing` words get `.vt-miss` (red). A wrong word is followed by the typed word in `<del class="vt-typed">`.
- `{extra}` entries render as `<del class="vt-extra">`.

Then show the full verse (`item.recite`) and `item.note`.

### Grading

| situation | action |
|---|---|
| cloze step 0–2, verdict correct | `cloze.step++` and save. Show "Next step" (Enter), which re-renders the **same card** at the next step without advancing `currentIndex`. Do not call `gradeCard`. |
| cloze step 0–2, verdict close or wrong | `cloze.failed = true` and save. Offer "Try again" (Enter): same step, input cleared. After 2 failed tries at the same step, drop one step (minimum 0). |
| cloze step 3, verdict correct | `gradeCard(card, cloze.failed ? 1 : 2)`, then `Storage.clearCloze(card.id)`. The card graduates. |
| cloze step 3, close or wrong | `cloze.failed = true`, set step to 2 and save, then "Try again". The ramp continues until step 3 passes or the user leaves. If they leave, the state persists and resumes next session. |
| review (no cloze state), correct | `gradeCard(card, 2)` |
| review, close | `gradeCard(card, 1)` |
| review, wrong or bail | `gradeCard(card, 0)` and `Storage.setCloze(card.id, {step: 2, failed: false})`. Next time the card shows, it runs step 2 then step 3. A pass at step 3 is graded Hard (1), since `failed` becomes true on any miss; a clean pass is Good (2). `gradeCard` is called on that later pass like any review. |
| "I was actually right" (shown on close or wrong) | treat as correct for the current step or review: grade 2 for a review, or advance for a cloze step. |
| Esc / "I don't know" in a cloze step | show the verse and the diff of an empty answer, mark `failed`, stay on the step. No `gradeCard`. |

Session stats: count a card once, at the moment `gradeCard` is called. Cloze steps don't count.

## 7. CSS (minimal, matching the current style)

```css
.vt-scaffold { white-space: pre-wrap; line-height: 1.5; margin: .25rem 0 .5rem; }
.vt-input { width: 100%; font: inherit; }
.vt-diff { line-height: 1.6; }
.vt-typo { background: #fff3c4; }
.vt-miss { color: #b00020; text-decoration: underline; }
.vt-typed, .vt-extra { color: #888; margin-left: .2em; }
@media (prefers-color-scheme: dark) { .vt-typo { background: #5a4a00; } .vt-miss { color: #ff6b81; } }
```

No hover styles.

## 8. Tests

- `node content/bible/_impl/bible-checker.test.mjs` must report 0 failed (527 checks). If you edit `js/bible-checker.js`, keep `_impl/` in sync or point the test import at `../../../js/bible-checker.js`.
- Manual smoke test:
  1. Open `#/subject/bible` and start **Reference → verse** on Psalms. It should begin at step 0 for `Psalm 22:1`.
  2. Type the verse at each step. After step 3, check that the progress record exists in localStorage under `bible-psalms-01-text`, and that `study_cloze_state` no longer has the key.
  3. In **Verse → reference**, Psalms should show only `-ref` cards whose `-text` sibling has graduated.
  4. Type `ps 23 1`: correct, with the numbering note.
  5. Type `Psalm 22:2`: close.
- Export, Clear, Import should round-trip `study_cloze_state`.
