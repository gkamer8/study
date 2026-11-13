import { Router } from './router.js';
import { Storage } from './storage.js';
import { SpacedRepetition } from './spaced-repetition.js';
import { Markdown } from './markdown.js';

class StudyApp {
    constructor() {
        this.router = new Router();
        this.appEl = document.getElementById('app');
        this.subjects = null;
        this.currentSubject = null;
        this.currentUnit = null;
        
        this.initTheme();
        this.setupRoutes();
        this.setupThemeToggle();
    }

    async init() {
        // Load subjects
        try {
            const response = await fetch('content/subjects.json');
            this.subjects = await response.json();
        } catch (error) {
            this.showError('Failed to load subjects');
            console.error(error);
        }
    }

    initTheme() {
        const settings = Storage.getSettings();
        document.body.setAttribute('data-theme', settings.theme);
        this.updateThemeIcon(settings.theme);
    }

    setupThemeToggle() {
        const toggle = document.getElementById('theme-toggle');
        toggle.addEventListener('click', () => {
            const settings = Storage.getSettings();
            const newTheme = settings.theme === 'light' ? 'dark' : 'light';
            Storage.setSetting('theme', newTheme);
            document.body.setAttribute('data-theme', newTheme);
            this.updateThemeIcon(newTheme);
        });
    }

    updateThemeIcon(theme) {
        const icon = document.querySelector('.theme-icon');
        icon.textContent = theme === 'light' ? '🌙' : '☀️';
    }

    setupRoutes() {
        this.router.on('/', () => this.renderDashboard());
        this.router.on('/subjects', () => this.renderSubjects());
        this.router.on('/subject/:subjectId', (params) => this.renderSubject(params.subjectId));
        this.router.on('/lesson/:subjectId/:unitSlug', (params) => 
            this.renderLesson(params.subjectId, params.unitSlug));
        this.router.on('/review/:subjectId/:unitSlug', (params) => 
            this.renderReview(params.subjectId, params.unitSlug, 'unit'));
        this.router.on('/review/:subjectId', (params) => 
            this.renderReview(params.subjectId, null, 'all'));
        this.router.on('/quiz/:subjectId/:unitSlug', (params) => 
            this.renderQuiz(params.subjectId, params.unitSlug));
        this.router.on('/match/:subjectId/:unitSlug', (params) => 
            this.renderMatch(params.subjectId, params.unitSlug));
        this.router.on('/settings', () => this.renderSettings());
    }

    async loadSubjectIndex(subjectId) {
        const response = await fetch(`content/${subjectId}/index.json`);
        return await response.json();
    }

    async loadUnit(subjectId, unitFile) {
        const response = await fetch(`content/${subjectId}/${unitFile}`);
        return await response.json();
    }

    // Dashboard
    async renderDashboard() {
        if (!this.subjects) await this.init();

        const stats = Storage.getStats();
        const progress = Storage.getAllCardProgress();
        const settings = Storage.getSettings();

        // Calculate statistics
        let totalCards = 0;
        let dueCards = 0;
        let newCardsAvailable = 0;
        const unitMastery = {};

        for (const subject of this.subjects.subjects) {
            const index = await this.loadSubjectIndex(subject.id);
            
            for (const unitInfo of index.units) {
                const unit = await this.loadUnit(subject.id, unitInfo.file);
                totalCards += unit.cards.length;

                let unitDue = 0;
                let unitLearned = 0;

                for (const card of unit.cards) {
                    const cardProgress = progress[card.id];
                    
                    if (!cardProgress) {
                        newCardsAvailable++;
                    } else if (SpacedRepetition.isDue(cardProgress)) {
                        dueCards++;
                        unitDue++;
                    } else if (cardProgress.repetitions >= 1) {
                        unitLearned++;
                    }
                }

                const mastery = unit.cards.length > 0 
                    ? Math.round((unitLearned / unit.cards.length) * 100) 
                    : 0;
                unitMastery[`${subject.id}-${unitInfo.slug}`] = {
                    ...unitInfo,
                    mastery,
                    due: unitDue,
                    subjectId: subject.id
                };
            }
        }

        const limitedNewCards = Math.min(newCardsAvailable, settings.newCardsPerDay);

        this.appEl.innerHTML = `
            <div>
                <h1>Dashboard</h1>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-value">${dueCards + limitedNewCards}</span>
                        <span class="stat-label">Cards to Review</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${limitedNewCards}</span>
                        <span class="stat-label">New Cards Available</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${stats.streak}</span>
                        <span class="stat-label">Day Streak</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${stats.totalReviews}</span>
                        <span class="stat-label">Total Reviews</span>
                    </div>
                </div>

                ${dueCards + limitedNewCards > 0 ? `
                    <div class="card">
                        <h2>Ready to Study</h2>
                        <p>You have ${dueCards + limitedNewCards} cards waiting for review.</p>
                        <div class="action-buttons">
                            ${this.subjects.subjects.map(s => 
                                `<a href="#/review/${s.id}" class="btn">Review ${s.title}</a>`
                            ).join('')}
                        </div>
                    </div>
                ` : `
                    <div class="empty-state">
                        <div class="empty-state-icon">✅</div>
                        <p>All caught up! Come back later for more reviews.</p>
                    </div>
                `}

                <div class="card">
                    <h2>Unit Progress</h2>
                    <div class="unit-list">
                        ${Object.values(unitMastery).sort((a, b) => a.unit - b.unit).map(unit => `
                            <div class="unit-card">
                                <div class="unit-header">
                                    <div>
                                        <div class="unit-title">Unit ${unit.unit}: ${unit.title}</div>
                                        ${unit.due > 0 ? `<span class="unit-badge">${unit.due} due</span>` : ''}
                                    </div>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${unit.mastery}%"></div>
                                </div>
                                <div class="unit-meta">
                                    <span>${unit.mastery}% mastered</span>
                                    <span>${unit.card_count} cards</span>
                                </div>
                                <div class="action-buttons">
                                    <a href="#/lesson/${unit.subjectId}/${unit.slug}" class="btn btn-sm">Lesson</a>
                                    <a href="#/review/${unit.subjectId}/${unit.slug}" class="btn btn-sm">Review</a>
                                    <a href="#/quiz/${unit.subjectId}/${unit.slug}" class="btn btn-sm">Quiz</a>
                                    <a href="#/match/${unit.subjectId}/${unit.slug}" class="btn btn-sm">Match</a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="action-buttons">
                    <a href="#/subjects" class="btn btn-secondary">Browse Subjects</a>
                    <a href="#/settings" class="btn btn-secondary">Settings</a>
                </div>
            </div>
        `;
    }

    // Subjects list
    async renderSubjects() {
        if (!this.subjects) await this.init();

        this.appEl.innerHTML = `
            <div>
                <h1>Subjects</h1>
                <div class="unit-list">
                    ${this.subjects.subjects.map(subject => `
                        <a href="#/subject/${subject.id}" class="unit-card">
                            <div class="unit-title">${subject.title}</div>
                            <div class="unit-summary">${subject.description}</div>
                        </a>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Subject detail (units)
    async renderSubject(subjectId) {
        const index = await this.loadSubjectIndex(subjectId);
        const progress = Storage.getAllCardProgress();

        this.appEl.innerHTML = `
            <div>
                <h1>${index.title}</h1>
                <p>${index.description}</p>
                
                <div class="card">
                    <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                        <span><strong>${index.totals.cards}</strong> cards</span>
                        <span><strong>${index.totals.quiz}</strong> quiz questions</span>
                    </div>
                    <a href="#/review/${subjectId}" class="btn">Review All Units</a>
                </div>

                <h2>Units</h2>
                <div class="unit-list">
                    ${index.units.map(unit => {
                        // Calculate progress for this unit
                        const dueCount = 0; // We'd need to load each unit to count
                        const prereqText = unit.prerequisites.length > 0 
                            ? `Prerequisites: Unit ${unit.prerequisites.join(', ')}` 
                            : '';

                        return `
                            <div class="unit-card">
                                <div class="unit-header">
                                    <div class="unit-title">Unit ${unit.unit}: ${unit.title}</div>
                                </div>
                                <div class="unit-summary">${unit.summary}</div>
                                <div class="unit-meta">
                                    <span>${unit.card_count} cards</span>
                                    <span>${unit.quiz_count} quiz questions</span>
                                </div>
                                ${prereqText ? `<div class="prerequisites">${prereqText}</div>` : ''}
                                <div class="action-buttons">
                                    <a href="#/lesson/${subjectId}/${unit.slug}" class="btn btn-sm">Read Lesson</a>
                                    <a href="#/review/${subjectId}/${unit.slug}" class="btn btn-sm">Review Cards</a>
                                    <a href="#/quiz/${subjectId}/${unit.slug}" class="btn btn-sm">Take Quiz</a>
                                    <a href="#/match/${subjectId}/${unit.slug}" class="btn btn-sm">Match Game</a>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    // Lesson viewer
    async renderLesson(subjectId, unitSlug) {
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        const lessonHtml = Markdown.render(unit.lesson);

        this.appEl.innerHTML = `
            <div>
                <div style="margin-bottom: 1rem;">
                    <a href="#/subject/${subjectId}" class="btn btn-secondary btn-sm">← Back to ${index.title}</a>
                </div>
                
                <h1>Unit ${unit.unit}: ${unit.title}</h1>
                <p style="color: var(--text-secondary); margin-bottom: 2rem;">${unit.summary}</p>

                <div class="lesson-content">
                    ${lessonHtml}
                </div>

                <div class="card" style="margin-top: 2rem;">
                    <h3>Ready to practice?</h3>
                    <div class="action-buttons">
                        <a href="#/review/${subjectId}/${unitSlug}" class="btn">Review Cards</a>
                        <a href="#/quiz/${subjectId}/${unitSlug}" class="btn">Take Quiz</a>
                        <a href="#/match/${subjectId}/${unitSlug}" class="btn">Match Game</a>
                    </div>
                </div>
            </div>
        `;
    }

    // Flashcard review
    async renderReview(subjectId, unitSlug, mode) {
        const index = await this.loadSubjectIndex(subjectId);
        const progress = Storage.getAllCardProgress();
        const settings = Storage.getSettings();

        // Collect cards
        let allCards = [];
        if (mode === 'unit') {
            const unitInfo = index.units.find(u => u.slug === unitSlug);
            const unit = await this.loadUnit(subjectId, unitInfo.file);
            allCards = unit.cards;
        } else {
            // All units
            for (const unitInfo of index.units) {
                const unit = await this.loadUnit(subjectId, unitInfo.file);
                allCards.push(...unit.cards);
            }
        }

        // Build review queue: due cards + new cards up to limit
        const dueCardIds = SpacedRepetition.getDueCards(progress);
        const dueCardsInSet = allCards.filter(c => dueCardIds.includes(c.id));
        
        const newCardIds = SpacedRepetition.getNewCards(allCards, progress, settings.newCardsPerDay);
        const newCards = allCards.filter(c => newCardIds.includes(c.id));

        const queue = [...dueCardsInSet, ...newCards];

        if (queue.length === 0) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">✅</div>
                    <h2>All done!</h2>
                    <p>No cards to review right now. Come back later!</p>
                    <div class="action-buttons">
                        <a href="#/" class="btn">Back to Dashboard</a>
                        ${mode === 'unit' ? `<a href="#/subject/${subjectId}" class="btn btn-secondary">Back to Subject</a>` : ''}
                    </div>
                </div>
            `;
            return;
        }

        this.startReviewSession(queue, subjectId, unitSlug, mode);
    }

    startReviewSession(queue, subjectId, unitSlug, mode) {
        let currentIndex = 0;
        let flipped = false;
        let sessionStats = { again: 0, hard: 0, good: 0, easy: 0 };

        const render = () => {
            if (currentIndex >= queue.length) {
                this.showReviewComplete(sessionStats, subjectId, unitSlug, mode);
                return;
            }

            const card = queue[currentIndex];
            const progress = Storage.getCardProgress(card.id);
            const isNew = !progress || progress.isNew;

            this.appEl.innerHTML = `
                <div>
                    <div class="flashcard-info">
                        <span>Card ${currentIndex + 1} / ${queue.length}</span>
                        <span>${isNew ? 'New' : 'Review'}</span>
                    </div>

                    <div class="flashcard">
                        <div class="flashcard-inner ${flipped ? 'flipped' : ''}">
                            <div class="flashcard-face flashcard-front">
                                <div class="flashcard-label">${this.getCardTypeLabel(card.type)}</div>
                                <div class="flashcard-text">${this.escapeHtml(card.front)}</div>
                            </div>
                            <div class="flashcard-face flashcard-back">
                                <div class="flashcard-label">Answer</div>
                                <div class="flashcard-text">${this.escapeHtml(card.back)}</div>
                                ${card.tags && card.tags.length > 0 ? `
                                    <div style="margin-top: 1rem; font-size: 0.75rem; color: var(--text-secondary);">
                                        Tags: ${card.tags.join(', ')}
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>

                    <div class="flashcard-controls">
                        ${!flipped ? `
                            <button class="btn" id="reveal-btn">
                                Reveal Answer (Space)
                            </button>
                        ` : `
                            <div class="grade-buttons">
                                <button class="btn" data-grade="0" style="background: var(--error);">
                                    <span>Again</span>
                                    <span class="key">1</span>
                                </button>
                                <button class="btn" data-grade="1" style="background: var(--warning);">
                                    <span>Hard</span>
                                    <span class="key">2</span>
                                </button>
                                <button class="btn" data-grade="2" style="background: var(--success);">
                                    <span>Good</span>
                                    <span class="key">3</span>
                                </button>
                                <button class="btn" data-grade="3" style="background: var(--accent);">
                                    <span>Easy</span>
                                    <span class="key">4</span>
                                </button>
                            </div>
                        `}
                    </div>
                </div>
            `;

            // Event listeners
            const revealBtn = document.getElementById('reveal-btn');
            if (revealBtn) {
                revealBtn.addEventListener('click', () => {
                    flipped = true;
                    render();
                });
            }

            document.querySelectorAll('[data-grade]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const grade = parseInt(e.currentTarget.getAttribute('data-grade'));
                    this.gradeCard(card, grade, sessionStats);
                    flipped = false;
                    currentIndex++;
                    render();
                });
            });

            // Keyboard shortcuts
            const keyHandler = (e) => {
                if (e.key === ' ' || e.key === 'Spacebar') {
                    e.preventDefault();
                    if (!flipped) {
                        flipped = true;
                        render();
                    }
                } else if (flipped && e.key >= '1' && e.key <= '4') {
                    e.preventDefault();
                    const grade = parseInt(e.key) - 1;
                    this.gradeCard(card, grade, sessionStats);
                    flipped = false;
                    currentIndex++;
                    render();
                }
            };

            document.removeEventListener('keydown', keyHandler);
            document.addEventListener('keydown', keyHandler);
        };

        render();
    }

    gradeCard(card, grade, sessionStats) {
        const gradeNames = ['again', 'hard', 'good', 'easy'];
        sessionStats[gradeNames[grade]]++;

        let progress = Storage.getCardProgress(card.id);
        if (!progress) {
            progress = SpacedRepetition.initCard();
        }

        progress = SpacedRepetition.gradeCard(progress, grade);
        Storage.setCardProgress(card.id, progress);

        // Update stats
        const stats = Storage.getStats();
        Storage.updateStats({
            totalReviews: stats.totalReviews + 1
        });
        Storage.updateStreak();
    }

    showReviewComplete(sessionStats, subjectId, unitSlug, mode) {
        const total = sessionStats.again + sessionStats.hard + sessionStats.good + sessionStats.easy;

        this.appEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🎉</div>
                <h2>Session Complete!</h2>
                <p>You reviewed ${total} cards.</p>
                
                <div class="stats-grid" style="max-width: 600px; margin: 2rem auto;">
                    <div class="stat-card">
                        <span class="stat-value">${sessionStats.again}</span>
                        <span class="stat-label">Again</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${sessionStats.hard}</span>
                        <span class="stat-label">Hard</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${sessionStats.good}</span>
                        <span class="stat-label">Good</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${sessionStats.easy}</span>
                        <span class="stat-label">Easy</span>
                    </div>
                </div>

                <div class="action-buttons">
                    <a href="#/" class="btn">Back to Dashboard</a>
                    ${mode === 'unit' ? `<a href="#/subject/${subjectId}" class="btn btn-secondary">Back to Subject</a>` : ''}
                </div>
            </div>
        `;
    }

    getCardTypeLabel(type) {
        const labels = {
            recall: 'Recall',
            cloze: 'Fill in the blank',
            identify: 'Identify',
            apply: 'Apply'
        };
        return labels[type] || 'Question';
    }

    // Quiz mode
    async renderQuiz(subjectId, unitSlug) {
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        if (unit.quiz.length === 0) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📝</div>
                    <p>No quiz questions available for this unit.</p>
                    <a href="#/subject/${subjectId}" class="btn">Back to Subject</a>
                </div>
            `;
            return;
        }

        this.startQuizSession(unit.quiz, subjectId, unitSlug, unit.title);
    }

    startQuizSession(questions, subjectId, unitSlug, unitTitle) {
        let currentIndex = 0;
        let score = 0;
        let answered = false;
        let selectedChoice = null;
        let missedQuestions = [];

        const render = () => {
            if (currentIndex >= questions.length) {
                this.showQuizComplete(score, questions.length, missedQuestions, subjectId, unitSlug);
                return;
            }

            const question = questions[currentIndex];
            
            // Shuffle choices
            const shuffled = question.choices.map((choice, idx) => ({ choice, idx }));
            for (let i = shuffled.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
            const correctShuffledIndex = shuffled.findIndex(s => s.idx === question.answer_index);

            this.appEl.innerHTML = `
                <div class="quiz-question">
                    <div style="margin-bottom: 1rem;">
                        <a href="#/subject/${subjectId}" class="btn btn-secondary btn-sm">← Back</a>
                    </div>

                    <div class="quiz-progress">
                        <h2>${unitTitle} - Quiz</h2>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${(currentIndex / questions.length) * 100}%"></div>
                        </div>
                        <p>Question ${currentIndex + 1} of ${questions.length}</p>
                    </div>

                    <div class="question-text">${this.escapeHtml(question.question)}</div>

                    <div class="choices">
                        ${shuffled.map((item, idx) => {
                            let className = 'choice';
                            if (answered) {
                                if (idx === correctShuffledIndex) {
                                    className += ' correct';
                                } else if (idx === selectedChoice) {
                                    className += ' incorrect';
                                }
                            } else if (idx === selectedChoice) {
                                className += ' selected';
                            }

                            return `
                                <div class="${className}" data-choice="${idx}">
                                    ${this.escapeHtml(item.choice)}
                                </div>
                            `;
                        }).join('')}
                    </div>

                    ${answered ? `
                        <div class="explanation">
                            <div class="explanation-label">
                                ${selectedChoice === correctShuffledIndex ? '✅ Correct!' : '❌ Incorrect'}
                            </div>
                            <p>${this.escapeHtml(question.explanation)}</p>
                        </div>
                        <button class="btn" id="next-btn">Next Question</button>
                    ` : ''}
                </div>
            `;

            if (!answered) {
                document.querySelectorAll('.choice').forEach(el => {
                    el.addEventListener('click', (e) => {
                        selectedChoice = parseInt(e.currentTarget.getAttribute('data-choice'));
                        answered = true;
                        
                        if (selectedChoice === correctShuffledIndex) {
                            score++;
                        } else {
                            missedQuestions.push(question);
                        }
                        
                        render();
                    });
                });
            } else {
                document.getElementById('next-btn').addEventListener('click', () => {
                    currentIndex++;
                    answered = false;
                    selectedChoice = null;
                    render();
                });
            }
        };

        render();
    }

    showQuizComplete(score, total, missedQuestions, subjectId, unitSlug) {
        const percentage = Math.round((score / total) * 100);
        
        // Update stats
        const stats = Storage.getStats();
        Storage.updateStats({
            quizAttempts: stats.quizAttempts + 1
        });

        this.appEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">${percentage >= 80 ? '🎉' : '📝'}</div>
                <h2>Quiz Complete!</h2>
                <p>You scored ${score} out of ${total} (${percentage}%)</p>

                ${missedQuestions.length > 0 ? `
                    <div class="card" style="max-width: 600px; margin: 2rem auto; text-align: left;">
                        <h3>Review Missed Questions</h3>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem;">
                            These questions have been added to your review queue.
                        </p>
                    </div>
                ` : `
                    <p>Perfect score! 🌟</p>
                `}

                <div class="action-buttons">
                    <a href="#/quiz/${subjectId}/${unitSlug}" class="btn">Retake Quiz</a>
                    <a href="#/subject/${subjectId}" class="btn btn-secondary">Back to Subject</a>
                    <a href="#/" class="btn btn-secondary">Dashboard</a>
                </div>
            </div>
        `;
    }

    // Match game
    async renderMatch(subjectId, unitSlug) {
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        // Select cards suitable for matching (recall and identify types)
        const matchableCards = unit.cards.filter(c => 
            c.type === 'recall' || c.type === 'identify'
        );

        if (matchableCards.length < 4) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🎮</div>
                    <p>Not enough cards for a match game in this unit.</p>
                    <a href="#/subject/${subjectId}" class="btn">Back to Subject</a>
                </div>
            `;
            return;
        }

        // Pick 6 random cards
        const selected = matchableCards.sort(() => Math.random() - 0.5).slice(0, 6);
        
        // Create pairs
        const pairs = [];
        selected.forEach(card => {
            pairs.push({ text: card.front, pairId: card.id, type: 'front' });
            pairs.push({ text: card.back, pairId: card.id, type: 'back' });
        });

        // Shuffle
        pairs.sort(() => Math.random() - 0.5);

        this.startMatchGame(pairs, subjectId, unitSlug, unit.title);
    }

    startMatchGame(pairs, subjectId, unitSlug, unitTitle) {
        let selected = [];
        let matched = new Set();
        let startTime = Date.now();
        let timerInterval;

        const render = () => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;

            this.appEl.innerHTML = `
                <div class="match-game">
                    <div style="margin-bottom: 1rem;">
                        <a href="#/subject/${subjectId}" class="btn btn-secondary btn-sm">← Back</a>
                    </div>

                    <div class="match-header">
                        <h2>${unitTitle} - Match Game</h2>
                        <div class="match-timer">${minutes}:${seconds.toString().padStart(2, '0')}</div>
                    </div>
                    <p>Match ${pairs.length / 2} pairs as fast as you can!</p>

                    <div class="match-grid">
                        ${pairs.map((pair, idx) => {
                            let className = 'match-card';
                            if (matched.has(idx)) className += ' matched';
                            if (selected.includes(idx)) className += ' selected';

                            return `
                                <div class="${className}" data-idx="${idx}" data-pair="${pair.pairId}">
                                    ${this.escapeHtml(pair.text)}
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <p style="margin-top: 1rem; color: var(--text-secondary);">
                        Matched: ${matched.size / 2} / ${pairs.length / 2}
                    </p>
                </div>
            `;

            document.querySelectorAll('.match-card:not(.matched)').forEach(el => {
                el.addEventListener('click', (e) => {
                    const idx = parseInt(e.currentTarget.getAttribute('data-idx'));
                    const pairId = e.currentTarget.getAttribute('data-pair');

                    if (selected.includes(idx)) {
                        selected = selected.filter(i => i !== idx);
                    } else if (selected.length < 2) {
                        selected.push(idx);

                        if (selected.length === 2) {
                            const [first, second] = selected;
                            const firstPair = pairs[first].pairId;
                            const secondPair = pairs[second].pairId;

                            if (firstPair === secondPair) {
                                matched.add(first);
                                matched.add(second);
                                selected = [];

                                if (matched.size === pairs.length) {
                                    clearInterval(timerInterval);
                                    const finalTime = Math.floor((Date.now() - startTime) / 1000);
                                    setTimeout(() => this.showMatchComplete(finalTime, subjectId, unitSlug), 500);
                                    return;
                                }
                            } else {
                                setTimeout(() => {
                                    selected = [];
                                    render();
                                }, 1000);
                            }
                        }
                    }

                    render();
                });
            });
        };

        timerInterval = setInterval(() => render(), 1000);
        render();
    }

    showMatchComplete(seconds, subjectId, unitSlug) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;

        this.appEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🏆</div>
                <h2>Game Complete!</h2>
                <p>Time: ${minutes}:${secs.toString().padStart(2, '0')}</p>

                <div class="action-buttons">
                    <a href="#/match/${subjectId}/${unitSlug}" class="btn">Play Again</a>
                    <a href="#/subject/${subjectId}" class="btn btn-secondary">Back to Subject</a>
                </div>
            </div>
        `;
    }

    // Settings
    renderSettings() {
        const settings = Storage.getSettings();
        const stats = Storage.getStats();

        this.appEl.innerHTML = `
            <div>
                <h1>Settings</h1>

                <div class="card">
                    <h3>Study Settings</h3>
                    <div class="input-group">
                        <label for="new-cards-per-day">New cards per day</label>
                        <input type="number" id="new-cards-per-day" value="${settings.newCardsPerDay}" min="1" max="100">
                    </div>
                    <button class="btn" id="save-settings-btn">Save Settings</button>
                </div>

                <div class="card">
                    <h3>Progress Data</h3>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem;">
                        Export your progress to move it between devices.
                    </p>
                    <div class="action-buttons">
                        <button class="btn" id="export-btn">Export Progress</button>
                        <button class="btn btn-secondary" id="import-btn">Import Progress</button>
                    </div>
                    <input type="file" id="import-file" accept=".json" style="display: none;">
                </div>

                <div class="card">
                    <h3>Statistics</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <span class="stat-value">${stats.totalReviews}</span>
                            <span class="stat-label">Total Reviews</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-value">${stats.quizAttempts}</span>
                            <span class="stat-label">Quizzes Taken</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-value">${stats.streak}</span>
                            <span class="stat-label">Day Streak</span>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h3>Danger Zone</h3>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem;">
                        This will delete all your progress and cannot be undone.
                    </p>
                    <button class="btn" id="reset-btn" style="background: var(--error);">Reset All Data</button>
                </div>
            </div>
        `;

        // Event listeners
        document.getElementById('save-settings-btn').addEventListener('click', () => {
            const newCardsPerDay = parseInt(document.getElementById('new-cards-per-day').value);
            Storage.setSetting('newCardsPerDay', newCardsPerDay);
            this.showAlert('Settings saved!', 'success');
        });

        document.getElementById('export-btn').addEventListener('click', () => {
            const data = Storage.exportData();
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `study-progress-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        });

        document.getElementById('import-btn').addEventListener('click', () => {
            document.getElementById('import-file').click();
        });

        document.getElementById('import-file').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = JSON.parse(e.target.result);
                        Storage.importData(data);
                        this.showAlert('Progress imported successfully!', 'success');
                        setTimeout(() => window.location.reload(), 1500);
                    } catch (error) {
                        this.showAlert('Failed to import: Invalid file format', 'error');
                    }
                };
                reader.readAsText(file);
            }
        });

        document.getElementById('reset-btn').addEventListener('click', () => {
            if (confirm('Are you sure? This will delete ALL your progress and cannot be undone.')) {
                if (confirm('Really delete everything? This is your last chance!')) {
                    Storage.clearAllData();
                    window.location.reload();
                }
            }
        });
    }

    showAlert(message, type = 'success') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        alert.style.position = 'fixed';
        alert.style.top = '1rem';
        alert.style.right = '1rem';
        alert.style.zIndex = '10000';
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    }

    showError(message) {
        this.appEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">⚠️</div>
                <h2>Error</h2>
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app
const app = new StudyApp();
app.init();
