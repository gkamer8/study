# Study Site - Gordon Kamer

A personal spaced-repetition study website for learning molecular biology and other subjects. Built with pure static HTML/CSS/JavaScript (no build step) and served via GitHub Pages at [study.g0rdon.com](https://study.g0rdon.com).

## Features

- **Spaced Repetition**: SM-2 algorithm for optimal review scheduling
- **Multiple Study Modes**:
  - Flashcard review with 4-grade system (Again/Hard/Good/Easy)
  - Multiple-choice quizzes with explanations
  - Match game for rapid recall practice
  - Lesson reader with Markdown support
- **Progress Tracking**: All progress stored in localStorage
- **Export/Import**: Move your progress between devices
- **Dark Mode**: Automatic theme switching
- **Mobile Responsive**: Works great on phones and tablets
- **Privacy-First**: No tracking, no analytics, all data stays local

## Content Structure

### Adding a New Subject

1. Create a new folder under `content/` (e.g., `content/chemistry/`)
2. Add your unit JSON files following the schema below
3. Create an `index.json` file listing all units
4. Update `content/subjects.json` to include the new subject:

```json
{
  "subjects": [
    {
      "id": "biology",
      "title": "Practical molecular biology for reading papers",
      "description": "...",
      "path": "biology"
    },
    {
      "id": "chemistry",
      "title": "Your New Subject",
      "description": "Subject description",
      "path": "chemistry"
    }
  ]
}
```

### Subject Index Format (`index.json`)

```json
{
  "subject": "biology",
  "title": "Subject Title",
  "description": "Brief description",
  "schema_version": 1,
  "generated": "YYYY-MM-DD",
  "units": [
    {
      "unit": 1,
      "slug": "unit-slug",
      "title": "Unit Title",
      "summary": "2-4 sentence summary",
      "file": "01-unit-slug.json",
      "card_count": 42,
      "quiz_count": 13,
      "prerequisites": []
    }
  ],
  "totals": {
    "cards": 100,
    "quiz": 50
  }
}
```

**Fields:**
- `prerequisites`: Array of unit numbers (e.g., `[1, 2]`) that should be completed first
- `slug`: URL-safe identifier (lowercase, hyphens)
- `file`: JSON filename for this unit

### Unit File Format (`NN-slug.json`)

```json
{
  "unit": 1,
  "slug": "unit-slug",
  "title": "Unit Title",
  "summary": "Brief summary",
  "lesson": "# Markdown Lesson Content\n\nYour lesson text here...",
  "cards": [...],
  "quiz": [...]
}
```

#### Lesson Content

The `lesson` field contains Markdown text with these features:
- GitHub Flavored Markdown (GFM) tables
- Fenced code blocks with ` ``` `
- Standard formatting: **bold**, *italic*, lists, headers
- Superscript: `^INK4a^` renders as <sup>INK4a</sup>
- Links: `[text](url)`

Keep lessons concise (600-1200 words recommended).

#### Flashcard Format

```json
{
  "id": "u2-c29",
  "front": "Question or prompt text",
  "back": "Answer text",
  "tags": ["topic", "subtopic"],
  "type": "recall"
}
```

**Card Types:**
- `recall`: Standard Q&A
- `cloze`: Fill-in-the-blank (use `___` in front, answer in back)
- `identify`: Term/notation → definition
- `apply`: Scenario requiring reasoning

**Card IDs:**
- Format: `u<unit>-c<number>` (e.g., `u2-c29`)
- Must be unique and stable
- Appending new cards preserves existing IDs
- Inserting renumbers everything after it

**Tags:** Optional, used for filtering and drill modes

#### Quiz Question Format

```json
{
  "id": "u1-q02",
  "question": "Question text",
  "choices": ["Choice A", "Choice B", "Choice C", "Choice D"],
  "answer_index": 2,
  "explanation": "Why this answer is correct"
}
```

- Always exactly 4 choices
- `answer_index` is 0-based (0 = first choice)
- Choices are shuffled at display time
- Explanations should not reference choice letters/positions

## Development

### Local Testing

Serve the site locally with any static server:

```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000`

### File Structure

```
.
├── index.html              # Main entry point
├── CNAME                   # Custom domain for GitHub Pages
├── .nojekyll               # Disable Jekyll processing
├── css/
│   └── style.css           # All styles (light/dark themes)
├── js/
│   ├── app.js              # Main application logic
│   ├── router.js           # Client-side routing
│   ├── storage.js          # localStorage management
│   ├── spaced-repetition.js # SM-2 algorithm
│   └── markdown.js         # Markdown renderer
└── content/
    ├── subjects.json       # List of all subjects
    └── biology/
        ├── index.json      # Biology subject metadata
        ├── README.md       # Content schema documentation
        ├── 01-central-dogma.json
        ├── 02-naming-conventions.json
        ├── ...
        └── _src/           # Content generators (optional)
```

## Spaced Repetition Algorithm

This site uses the **SM-2** (SuperMemo 2) algorithm:

- **Again** (1): Review in 1 minute, resets repetition count
- **Hard** (2): Review in 10 minutes, resets repetition count
- **Good** (3): First review in 1 day, second in 6 days, then intervals multiply by ease factor
- **Easy** (4): Like Good but with 1.3x bonus multiplier

Each card tracks:
- `interval`: Days until next review
- `repetitions`: Number of successful reviews
- `easeFactor`: Multiplier for future intervals (starts at 2.5)
- `nextReview`: Timestamp for next review
- `lastReview`: Timestamp of last review

## Progress Data

All progress is stored in browser localStorage:

- **Card Progress**: Review history and scheduling for each card
- **Settings**: New cards per day limit, theme preference
- **Stats**: Streak, total reviews, quiz attempts

### Export/Import

1. Go to Settings page
2. Click "Export Progress" to download a JSON file
3. On another device, click "Import Progress" and select the file

**Note**: Import overwrites existing progress. Export before importing to keep a backup.

## GitHub Pages Setup

This site is configured for GitHub Pages at the custom domain `study.g0rdon.com`.

### In GitHub Repository Settings:

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **(root)**
4. Save

The site will build and deploy automatically on every push to `main`.

### DNS Configuration

The DNS is already configured:
- CNAME record: `study.g0rdon.com` → `gkamer8.github.io`

The `CNAME` file in this repo tells GitHub Pages to serve the site at the custom domain.

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support (iOS 12+)
- Mobile browsers: ✅ Responsive design

Minimum requirements:
- ES6 modules support
- localStorage API
- CSS custom properties

## Credits

- **SM-2 Algorithm**: Piotr Wozniak, SuperMemo (1990)
- **Content**: Biology units for ML researchers
- **Built by**: Gordon Kamer

## License

Content and code are personal study materials. Not licensed for redistribution.
