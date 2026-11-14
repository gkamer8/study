// node bible-checker.test.mjs   (run from content/bible/_impl; reads ../index.json and tests.json)
import { readFileSync } from 'node:fs';
import { buildBookIndex, checkReference, scoreText, clozeScaffold, renderDiff } from './bible-checker.js';
const here = new URL('.', import.meta.url);
const index = JSON.parse(readFileSync(new URL('../index.json', here)));
const tests = JSON.parse(readFileSync(new URL('tests.json', here)));
const items = Object.fromEntries(index.items.map((i) => [i.id, i]));
const books = buildBookIndex(index.books);
let fail = 0, pass = 0;
const ok = (cond, msg) => { if (cond) pass++; else { fail++; console.log('FAIL', msg); } };
for (const t of tests.reference) {
  const r = checkReference(t.input, items[t.item], books);
  ok(r.verdict === t.verdict && (!t.system || r.system === t.system),
     `ref ${t.item} "${t.input}" -> ${JSON.stringify(r)} expected ${t.verdict}${t.system ? '/' + t.system : ''} (${t.why})`);
  // the flat accept list must agree with the structured checker on every 'correct' case
  for (const a of items[t.item].accept) ok(checkReference(a, items[t.item], books).verdict === 'correct', `accept entry "${a}" rejected for ${t.item}`);
}
for (const t of tests.text) {
  const r = scoreText(t.input, items[t.item].recite, index.scoring);
  ok(r.verdict === t.verdict && (t.errors === undefined || r.errors === t.errors),
     `text ${t.item} "${t.input.slice(0, 40)}..." -> ${r.verdict} errors=${r.errors} score=${r.score.toFixed(2)} expected ${t.verdict}${t.errors !== undefined ? ' errors=' + t.errors : ''} (${t.why})`);
}
for (const t of tests.cloze) {
  const got = clozeScaffold(t.recite, t.step);
  ok(got === t.expect, `cloze step ${t.step}: got "${got}" expected "${t.expect}"`);
}
// diff rendering keeps every printed word, in order
{
  const it = items['bible-gospels-12'];
  const r = scoreText('For God so loved the world that he gave his only begotten Son', it.recite, index.scoring);
  const d = renderDiff(it.recite, r.ops, index.scoring);
  ok(d.filter((x) => x.word).map((x) => x.word).join(' ') === it.recite, 'renderDiff keeps the printed verse');
  ok(d.find((x) => x.word === 'give').status === 'wrong' && d.find((x) => x.word === 'give').typed === 'gave', 'renderDiff marks give/gave');
  ok(d.find((x) => x.word === 'everlasting.').status === 'missing', 'renderDiff marks missing tail');
}
// every item: its own recite text scores perfectly, its DRB ref is accepted
for (const it of index.items) {
  ok(scoreText(it.recite, it.recite, index.scoring).errors === 0, `self-score ${it.id}`);
  ok(checkReference(it.ref_drb, it, books).verdict === 'correct', `ref_drb ${it.id} ${it.ref_drb}`);
  if (it.ref_modern) ok(checkReference(it.ref_modern, it, books).verdict === 'correct', `ref_modern ${it.id} ${it.ref_modern}`);
  if (it.ref_nabre) ok(checkReference(it.ref_nabre, it, books).verdict === 'correct', `ref_nabre ${it.id} ${it.ref_nabre}`);
}
console.log(`${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
