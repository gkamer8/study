// Reference implementation for the Bible subject's two typed drills.
// Drop into the site as js/bible-checker.js (ES module, no dependencies).
// Data comes from content/bible/index.json: `books`, `scoring`, `items`.

// ---------- shared ----------
const stripMarks = (s) => s.normalize('NFKD').replace(/[\u0300-\u036f]/g, '');

// ---------- reference checker (text -> reference) ----------
const FILLER = /\b(the|book|of|gospel|according|to|saint|st|epistle|letter|holy|prophet|prophecy)\b/g;
const NUMWORD = [
  [/^(first|1st|i)\b\.?\s*/, '1'], [/^(second|2nd|ii)\b\.?\s*/, '2'],
  [/^(third|3rd|iii)\b\.?\s*/, '3'], [/^(fourth|4th|iv)\b\.?\s*/, '4'],
];

// Normalize a book name or alias to a lookup key: "1 Kings" -> "1kings", "Song of Songs" -> "songsongs".
export function bookKey(name) {
  let s = stripMarks(String(name)).toLowerCase().trim();
  let num = '';
  const m = s.match(/^([1-4])\s*/);
  if (m) { num = m[1]; s = s.slice(m[0].length); }
  else {
    for (const [re, d] of NUMWORD) {
      // only treat i/ii/iii/iv as numerals when a book name follows
      const mm = s.match(re);
      if (mm && s.slice(mm[0].length).match(/^[a-z]{2,}/)) { num = d; s = s.slice(mm[0].length); break; }
    }
  }
  s = s.replace(FILLER, ' ').replace(/[^a-z]/g, '');
  return num + s;
}

// Map from book key -> array of USFM codes (array because DRB "1 Kings" = 1SA but modern "1 Kings" = 1KI).
export function buildBookIndex(books) {
  const idx = new Map();
  const add = (k, code) => {
    if (!k) return;
    const arr = idx.get(k) || [];
    if (!arr.includes(code)) arr.push(code);
    idx.set(k, arr);
  };
  for (const b of books) {
    for (const n of [b.drb, b.modern, ...b.drb_aliases, ...b.modern_aliases]) {
      add(bookKey(n), b.usfm);
      add(String(n).toLowerCase().replace(/[^a-z0-9]/g, ''), b.usfm);
    }
  }
  return idx;
}

// Parse "Jn 3 16", "John 3:16", "1 Kings 3.10", "Ps 22:1-6", "Apocalypse 3, 20" -> {key, chapter, vStart, vEnd}
export function parseReference(input) {
  let s = stripMarks(String(input)).toLowerCase().trim();
  s = s.replace(/[\u2010-\u2015]/g, '-').replace(/\s+/g, ' ');
  const m = s.match(/^(.*?[a-z][a-z .]*?)\s*\.?\s*(\d+)\s*(?:[:.,]|\s|v\.?|vs\.?|verse)\s*(\d+)\s*(?:-\s*(\d+))?\s*[.]?$/);
  if (!m) return null;
  return {
    key: bookKey(m[1].replace(/\.$/, '')),
    chapter: +m[2], vStart: +m[3], vEnd: m[4] ? +m[4] : null,
  };
}

// Returns {verdict: 'correct'|'close'|'wrong', system, note, reason}
export function checkReference(input, item, bookIndex) {
  const p = parseReference(input);
  if (!p) return { verdict: 'wrong', reason: 'unparsed', note: item.note || null };
  const books = bookIndex.get(p.key) || [];
  if (!books.includes(item.book)) {
    return { verdict: 'wrong', reason: books.length ? 'book' : 'unknown-book', note: item.note || null };
  }
  for (const n of item.numberings) {
    if (n.chapter !== p.chapter || n.verse_start !== p.vStart) continue;
    const endOk = p.vEnd === null || p.vEnd === n.verse_end;
    if (endOk) return { verdict: 'correct', system: n.system, note: item.note || null };
  }
  for (const n of item.numberings) {
    if (n.chapter === p.chapter && Math.abs(p.vStart - n.verse_start) === 1) {
      return { verdict: 'close', system: n.system, reason: 'verse-off-by-one', note: item.note || null };
    }
  }
  const sameChapter = item.numberings.some((n) => n.chapter === p.chapter);
  return { verdict: 'wrong', reason: sameChapter ? 'verse' : 'chapter', note: item.note || null };
}

// ---------- text scorer (reference -> text) ----------
export function tokenize(text, variants = {}) {
  let s = stripMarks(String(text)).toLowerCase();
  s = s.replace(/[\u2018\u2019\u02bc`\u00b4']/g, '');      // apostrophes vanish: mother's -> mothers
  s = s.replace(/[\u2010-\u2015-]/g, ' ');                  // hyphens/dashes split words
  s = s.replace(/[^a-z0-9]+/g, ' ').trim();
  if (!s) return [];
  return s.split(' ').map((w) => variants[w] || w);
}

function damerau1(a, b) {
  // true when Damerau-Levenshtein distance is exactly 1
  if (a === b) return false;
  const la = a.length, lb = b.length;
  if (Math.abs(la - lb) > 1) return false;
  if (la === lb) {
    const diff = [];
    for (let i = 0; i < la; i++) if (a[i] !== b[i]) diff.push(i);
    if (diff.length === 1) return true;
    return diff.length === 2 && diff[1] === diff[0] + 1 && a[diff[0]] === b[diff[1]] && a[diff[1]] === b[diff[0]];
  }
  const [s, l] = la < lb ? [a, b] : [b, a];
  let i = 0, j = 0, skipped = false;
  while (i < s.length && j < l.length) {
    if (s[i] === l[j]) { i++; j++; }
    else if (skipped) return false;
    else { skipped = true; j++; }
  }
  return true;
}

// Word-level alignment. Returns ops in reference order:
// {op:'ok'|'typo'|'wrong'|'missing'|'extra', ref, typed}
export function alignWords(ref, typed) {
  const n = ref.length, m = typed.length, INF = 1e9;
  const D = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(INF));
  const P = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(null));
  D[0][0] = 0;
  for (let i = 0; i <= n; i++) {
    for (let j = 0; j <= m; j++) {
      const d = D[i][j];
      if (d === INF) continue;
      const relax = (ii, jj, cost, op) => {
        if (ii <= n && jj <= m && d + cost < D[ii][jj]) { D[ii][jj] = d + cost; P[ii][jj] = { i, j, op }; }
      };
      if (i < n && j < m) {
        if (ref[i] === typed[j]) relax(i + 1, j + 1, 0, 'ok');
        else if (ref[i].length >= 6 && damerau1(ref[i], typed[j])) relax(i + 1, j + 1, 0, 'typo');
        else relax(i + 1, j + 1, 1, 'wrong');
      }
      if (i < n && j + 1 < m && typed[j] + typed[j + 1] === ref[i]) relax(i + 1, j + 2, 0, 'ok');   // "to day" = "today"
      if (i + 1 < n && j < m && ref[i] + ref[i + 1] === typed[j]) relax(i + 2, j + 1, 0, 'ok');     // "anyone" = "any one"
      if (i < n) relax(i + 1, j, 1, 'missing');
      if (j < m) relax(i, j + 1, 1, 'extra');
    }
  }
  const ops = [];
  let i = n, j = m;
  while (i > 0 || j > 0) {
    const p = P[i][j];
    ops.push({ op: p.op, ref: ref.slice(p.i, i).join(' ') || null, typed: typed.slice(p.j, j).join(' ') || null,
               refStart: p.i, refEnd: i });
    i = p.i; j = p.j;
  }
  ops.reverse();
  return { errors: D[n][m], ops };
}

// Returns {verdict, score, errors, n, ops, grade}
export function scoreText(input, recite, scoring) {
  const variants = (scoring && scoring.text && scoring.text.spelling_variants) || {};
  const ref = tokenize(recite, variants);
  const typed = tokenize(input, variants);
  const { errors, ops } = alignWords(ref, typed);
  const n = ref.length;
  const score = Math.max(0, 1 - errors / n);
  let verdict;
  if (errors === 0 || (n >= 6 && (score >= 0.95 || errors <= 1))) verdict = 'correct';
  else if (score >= 0.80 || (n <= 5 && errors === 1)) verdict = 'close';
  else verdict = 'wrong';
  const grade = { correct: 2, close: 1, wrong: 0 }[verdict];
  return { verdict, score, errors, n, ops, grade };
}

// ---------- cloze scaffold ----------
// step 0: every 3rd word hidden; 1: every other word hidden; 2: first letters; 3: nothing shown.
export function clozeScaffold(recite, step) {
  if (step >= 3) return '';
  const words = recite.split(/\s+/);
  return words.map((w, i) => {
    const hide = (step === 0 && i % 3 === 2) || (step === 1 && i % 2 === 1);
    if (step === 2) {
      let seen = false;
      return w.replace(/[A-Za-z\u00C0-\u024F\u2019']/g, (ch) => {
        if (/[\u2019']/.test(ch)) return seen ? '' : ch;
        if (!seen) { seen = true; return ch; }
        return '';
      });
    }
    if (!hide) return w;
    const letters = (w.match(/[A-Za-z\u00C0-\u024F]/g) || []).length;
    return w.replace(/[A-Za-z\u00C0-\u024F\u2019']+/, '_'.repeat(Math.min(8, Math.max(1, letters))));
  }).join(' ');
}

// Map alignment ops back onto the printed words of the verse for display.
// Returns [{word, status:'ok'|'typo'|'wrong'|'missing', typed}] plus {extra: 'typed words'} entries
// at the position where the extra words were typed. Render: ok plain, typo amber, wrong/missing red
// (show `typed` struck through next to it), extra struck-through grey.
export function renderDiff(recite, ops, scoring) {
  const variants = (scoring && scoring.text && scoring.text.spelling_variants) || {};
  const printed = recite.split(/\s+/);
  const owner = [];                       // token index -> printed word index
  printed.forEach((w, wi) => tokenize(w, variants).forEach(() => owner.push(wi)));
  const rank = { ok: 0, typo: 1, wrong: 2, missing: 2 };
  const out = printed.map((w) => ({ word: w, status: null, typed: [] }));
  const extras = [];
  for (const o of ops) {
    if (o.op === 'extra') { extras.push({ before: o.refStart < owner.length ? owner[o.refStart] : printed.length, typed: o.typed }); continue; }
    for (let t = o.refStart; t < o.refEnd; t++) {
      const cell = out[owner[t]];
      if (cell.status === null || rank[o.op] > rank[cell.status]) cell.status = o.op;
      if (o.op !== 'ok' && o.typed && !cell.typed.includes(o.typed)) cell.typed.push(o.typed);
    }
  }
  const res = [];
  out.forEach((c, wi) => {
    for (const e of extras) if (e.before === wi) res.push({ extra: e.typed });
    res.push({ word: c.word, status: c.status || 'ok', typed: c.typed.join(' ') || null });
  });
  for (const e of extras) if (e.before >= printed.length) res.push({ extra: e.typed });
  return res;
}
