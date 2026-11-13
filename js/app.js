import { Router } from './router.js';
import { Storage } from './storage.js';
import { SpacedRepetition } from './spaced-repetition.js';
import { Markdown } from './markdown.js';
import { AnswerChecker } from './answer-checker.js';

class StudyApp {
    constructor() {
        this.router = new Router();
        this.appEl = document.getElementById('app');
        this.subjects = null;
        this.currentCleanup = null; // Track cleanup function for current view
        
        this.initTheme();
        this.setupRoutes();
        this.setupThemeToggle();
    }

    async init() {
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
        icon.textContent = theme === 'light' ? '☾' : '☼';
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
        this.router.on('/terms/:subjectId/:unitSlug', (params) => 
            this.renderTermsDrill(params.subjectId, params.unitSlug));
        this.router.on('/settings', () => this.renderSettings());
    }

    cleanup() {
        if (this.currentCleanup) {
            this.currentCleanup();
            this.currentCleanup = null;
        }
    }

    async loadSubjectIndex(subjectId) {
        const response = await fetch(`content/${subjectId}/index.json`);
        return await response.json();
    }

    async loadUnit(subjectId, unitFile) {
        const response = await fetch(`content/${subjectId}/${unitFile}`);
        return await response.json();
    }

    async renderDashboard() {
        this.cleanup();
        if (!this.subjects) await this.init();

        const stats = Storage.getStats();
        const progress = Storage.getAllCardProgress();
        const settings = Storage.getSettings();

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
            <h1>Dashboard</h1>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">${dueCards + limitedNewCards}</span>
                    <span class="stat-label">Cards to Review</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">${limitedNewCards}</span>
                    <span class="stat-label">New Cards</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">${stats.streak}</span>
                    <span class="stat-label">Streak</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">${stats.totalReviews}</span>
                    <span class="stat-label">Reviews</span>
                </div>
            </div>

            ${dueCards + limitedNewCards > 0 ? `
                <p>${dueCards + limitedNewCards} cards waiting. ${this.subjects.subjects.map(s => 
                    `<a href="#/review/${s.id}">Review ${s.title}</a>`
                ).join(' | ')}</p>
            ` : '<p>All caught up.</p>'}

            <h2>Units</h2>
            <div class="unit-list">
                ${Object.values(unitMastery).sort((a, b) => a.unit - b.unit).map(unit => `
                    <div class="unit-card">
                        <div class="unit-title">Unit ${unit.unit}: ${unit.title}</div>
                        <div class="unit-summary">${unit.summary}</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${unit.mastery}%"></div>
                        </div>
                        <div class="unit-meta">
                            <span>${unit.mastery}% mastered</span>
                            <span>${unit.card_count} cards</span>
                            ${unit.due > 0 ? `<span>${unit.due} due</span>` : ''}
                        </div>
                        <div>
                            <a href="#/lesson/${unit.subjectId}/${unit.slug}" class="btn">Lesson</a>
                            <a href="#/review/${unit.subjectId}/${unit.slug}" class="btn">Review</a>
                            <a href="#/quiz/${unit.subjectId}/${unit.slug}" class="btn">Quiz</a>
                            <a href="#/terms/${unit.subjectId}/${unit.slug}" class="btn">Terms</a>
                            <a href="#/match/${unit.subjectId}/${unit.slug}" class="btn">Match</a>
                        </div>
                    </div>
                `).join('')}
            </div>

            <p><a href="#/settings">Settings</a></p>
        `;
    }

    async renderSubjects() {
        this.cleanup();
        if (!this.subjects) await this.init();

        this.appEl.innerHTML = `
            <h1>Subjects</h1>
            <div class="unit-list">
                ${this.subjects.subjects.map(subject => `
                    <a href="#/subject/${subject.id}" class="unit-card">
                        <div class="unit-title">${subject.title}</div>
                        <div class="unit-summary">${subject.description}</div>
                    </a>
                `).join('')}
            </div>
        `;
    }

    async renderSubject(subjectId) {
        this.cleanup();
        const index = await this.loadSubjectIndex(subjectId);

        this.appEl.innerHTML = `
            <h1>${index.title}</h1>
            <p>${index.description}</p>
            
            <p><strong>${index.totals.cards}</strong> cards, <strong>${index.totals.quiz}</strong> quiz questions. <a href="#/review/${subjectId}">Review all units</a></p>

            <h2>Units</h2>
            <div class="unit-list">
                ${index.units.map(unit => `
                    <div class="unit-card">
                        <div class="unit-title">Unit ${unit.unit}: ${unit.title}</div>
                        <div class="unit-summary">${unit.summary}</div>
                        <div class="unit-meta">
                            <span>${unit.card_count} cards</span>
                            <span>${unit.quiz_count} quiz</span>
                            ${unit.prerequisites.length > 0 ? `<span>Prereq: ${unit.prerequisites.join(', ')}</span>` : ''}
                        </div>
                        <div>
                            <a href="#/lesson/${subjectId}/${unit.slug}" class="btn">Lesson</a>
                            <a href="#/review/${subjectId}/${unit.slug}" class="btn">Review</a>
                            <a href="#/quiz/${subjectId}/${unit.slug}" class="btn">Quiz</a>
                            <a href="#/terms/${subjectId}/${unit.slug}" class="btn">Terms</a>
                            <a href="#/match/${subjectId}/${unit.slug}" class="btn">Match</a>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    async renderLesson(subjectId, unitSlug) {
        this.cleanup();
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        const lessonHtml = Markdown.render(unit.lesson);
        const glossaryHtml = this.renderGlossary(unit.glossary || []);
        const lessonWithTooltips = this.addGlossaryTooltips(lessonHtml, unit.glossary || []);

        this.appEl.innerHTML = `
            <p><a href="#/subject/${subjectId}">← Back</a></p>
            
            <h1>Unit ${unit.unit}: ${unit.title}</h1>
            <p>${unit.summary}</p>

            ${glossaryHtml}

            <div class="lesson-content">
                ${lessonWithTooltips}
            </div>

            <p>
                <a href="#/review/${subjectId}/${unitSlug}" class="btn">Review</a>
                <a href="#/quiz/${subjectId}/${unitSlug}" class="btn">Quiz</a>
                <a href="#/match/${subjectId}/${unitSlug}" class="btn">Match</a>
                <a href="#/terms/${subjectId}/${unitSlug}" class="btn">Terms</a>
            </p>
        `;

        this.setupTooltips();
    }

    renderGlossary(glossary) {
        if (!glossary || glossary.length === 0) return '';

        return `
            <details class="glossary" open>
                <summary><strong>Key terms</strong></summary>
                <dl class="glossary-list">
                    ${glossary.map(entry => `
                        <dt>${this.escapeHtml(entry.term)}</dt>
                        <dd>${this.escapeHtml(entry.definition)}</dd>
                    `).join('')}
                </dl>
            </details>
        `;
    }

    addGlossaryTooltips(html, glossary) {
        if (!glossary || glossary.length === 0) return html;

        // Sort terms by length (longest first) to avoid partial matches
        const sortedGlossary = [...glossary].sort((a, b) => b.term.length - a.term.length);

        let result = html;
        for (const entry of sortedGlossary) {
            const term = entry.term;
            const definition = entry.definition;
            
            // Create a pattern that matches the term as a whole word
            // Don't match if already inside a tag
            const pattern = new RegExp(`(?<![<>])\\b(${this.escapeRegex(term)})\\b(?![^<>]*>)`, 'gi');
            
            result = result.replace(pattern, (match) => {
                return `<span class="glossary-term" data-definition="${this.escapeHtml(definition)}">${match}</span>`;
            });
        }

        return result;
    }

    setupTooltips() {
        // Add tooltip behavior to glossary terms
        document.querySelectorAll('.glossary-term').forEach(el => {
            el.addEventListener('mouseenter', (e) => {
                const definition = e.target.getAttribute('data-definition');
                this.showTooltip(e.target, definition);
            });

            el.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });

            el.addEventListener('click', (e) => {
                e.preventDefault();
                const definition = e.target.getAttribute('data-definition');
                this.showTooltip(e.target, definition);
            });
        });
    }

    showTooltip(element, text) {
        this.hideTooltip();
        
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.bottom + 5) + 'px';
    }

    hideTooltip() {
        const existing = document.querySelector('.tooltip');
        if (existing) {
            existing.remove();
        }
    }

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    async renderReview(subjectId, unitSlug, mode) {
        this.cleanup();
        const index = await this.loadSubjectIndex(subjectId);
        const progress = Storage.getAllCardProgress();
        const settings = Storage.getSettings();

        let allCards = [];
        if (mode === 'unit') {
            const unitInfo = index.units.find(u => u.slug === unitSlug);
            const unit = await this.loadUnit(subjectId, unitInfo.file);
            allCards = unit.cards;
        } else {
            for (const unitInfo of index.units) {
                const unit = await this.loadUnit(subjectId, unitInfo.file);
                allCards.push(...unit.cards);
            }
        }

        const dueCardIds = SpacedRepetition.getDueCards(progress);
        const dueCardsInSet = allCards.filter(c => dueCardIds.includes(c.id));
        
        const newCardIds = SpacedRepetition.getNewCards(allCards, progress, settings.newCardsPerDay);
        const newCards = allCards.filter(c => newCardIds.includes(c.id));

        const queue = [...dueCardsInSet, ...newCards];

        if (queue.length === 0) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <h2>All done</h2>
                    <p>No cards to review right now.</p>
                    <p><a href="#/">Dashboard</a></p>
                </div>
            `;
            return;
        }

        this.startReviewSession(queue, subjectId, unitSlug, mode, settings.typedAnswers);
    }

    startReviewSession(queue, subjectId, unitSlug, mode, typedMode) {
        let currentIndex = 0;
        let sessionStats = { correct: 0, incorrect: 0 };
        let answered = false;
        let userAnswer = '';
        let startTime = Date.now();

        const cleanup = () => {
            document.removeEventListener('keydown', keyHandler);
        };
        this.currentCleanup = cleanup;

        const render = () => {
            if (currentIndex >= queue.length) {
                cleanup();
                this.showReviewComplete(sessionStats, subjectId, unitSlug, mode);
                return;
            }

            const card = queue[currentIndex];
            const progress = Storage.getCardProgress(card.id);
            const isNew = !progress || progress.isNew;

            if (typedMode) {
                this.renderTypedAnswerCard(card, isNew, currentIndex, queue.length, answered, userAnswer, 
                    () => {
                        // Next card
                        answered = false;
                        userAnswer = '';
                        currentIndex++;
                        startTime = Date.now();
                        render();
                    },
                    (result) => {
                        // Submit answer
                        answered = true;
                        const responseTime = Date.now() - startTime;
                        if (result === 'correct') {
                            sessionStats.correct++;
                            const quality = responseTime < 5000 ? 3 : 2; // Easy if < 5s, Good otherwise
                            this.gradeCard(card, quality);
                        } else {
                            sessionStats.incorrect++;
                            this.gradeCard(card, 0); // Again
                        }
                        render();
                    }
                );
            } else {
                this.renderSelfGradeCard(card, isNew, currentIndex, queue.length, answered,
                    () => {
                        // Reveal
                        answered = true;
                        render();
                    },
                    (grade) => {
                        // Grade and next
                        this.gradeCard(card, grade);
                        if (grade >= 2) sessionStats.correct++; else sessionStats.incorrect++;
                        answered = false;
                        currentIndex++;
                        render();
                    }
                );
            }
        };

        const keyHandler = (e) => {
            if (e.key === 'Escape' && typedMode && !answered) {
                // Show answer on Esc
                answered = true;
                sessionStats.incorrect++;
                this.gradeCard(queue[currentIndex], 0);
                render();
            }
        };

        document.addEventListener('keydown', keyHandler);
        render();
    }

    renderTypedAnswerCard(card, isNew, index, total, answered, userAnswer, onNext, onSubmit) {
        const correctAnswer = card.accept ? card.accept[0] : card.back;
        
        let isCorrect = false;
        if (answered) {
            isCorrect = AnswerChecker.check(userAnswer, card);
        }

        this.appEl.innerHTML = `
            <div class="flashcard-container">
                <div class="flashcard-info">
                    <span>Card ${index + 1} / ${total}</span>
                    <span>${isNew ? 'New' : 'Review'}</span>
                </div>

                <div class="flashcard-question">
                    <div class="flashcard-label">${this.getCardTypeLabel(card.type)}</div>
                    <div class="flashcard-text">${this.escapeHtml(card.front)}</div>
                </div>

                ${!answered ? `
                    <form id="answer-form">
                        <input type="text" class="answer-input" id="answer-input" 
                               placeholder="Type your answer..." autocomplete="off" autofocus>
                        <button type="submit" class="btn">Submit (Enter)</button>
                        <button type="button" class="btn" id="show-answer-btn">I don't know (Esc)</button>
                    </form>
                ` : `
                    <div class="answer-result ${isCorrect ? 'correct' : 'incorrect'}">
                        <strong>${isCorrect ? 'Correct' : 'Incorrect'}</strong>
                        <p><strong>Your answer:</strong> ${this.escapeHtml(userAnswer)}</p>
                        <p><strong>Correct answer:</strong> ${this.escapeHtml(correctAnswer)}</p>
                        ${card.tags && card.tags.length > 0 ? `<p style="margin-top: 0.5rem; font-size: 0.9rem;">Tags: ${card.tags.join(', ')}</p>` : ''}
                    </div>
                    ${!isCorrect ? `<button class="btn" id="override-btn">I was actually right</button>` : ''}
                    <button class="btn" id="next-btn">Next</button>
                `}
            </div>
        `;

        if (!answered) {
            const form = document.getElementById('answer-form');
            const input = document.getElementById('answer-input');
            const showBtn = document.getElementById('show-answer-btn');

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                userAnswer = input.value.trim();
                if (userAnswer) {
                    onSubmit('check');
                }
            });

            showBtn.addEventListener('click', () => {
                userAnswer = '';
                onSubmit('incorrect');
            });
        } else {
            const nextBtn = document.getElementById('next-btn');
            nextBtn.addEventListener('click', onNext);

            const overrideBtn = document.getElementById('override-btn');
            if (overrideBtn) {
                overrideBtn.addEventListener('click', () => {
                    // Override: change to correct and regrade
                    sessionStats.incorrect--;
                    sessionStats.correct++;
                    this.gradeCard(card, 2); // Good
                    onNext();
                });
            }
        }
    }

    renderSelfGradeCard(card, isNew, index, total, flipped, onReveal, onGrade) {
        this.appEl.innerHTML = `
            <div class="flashcard-container">
                <div class="flashcard-info">
                    <span>Card ${index + 1} / ${total}</span>
                    <span>${isNew ? 'New' : 'Review'}</span>
                </div>

                ${!flipped ? `
                    <div class="flashcard-question">
                        <div class="flashcard-label">${this.getCardTypeLabel(card.type)}</div>
                        <div class="flashcard-text">${this.escapeHtml(card.front)}</div>
                    </div>
                    <button class="btn" id="reveal-btn">Reveal (Space)</button>
                ` : `
                    <div class="flashcard-question">
                        <div class="flashcard-label">Question</div>
                        <div class="flashcard-text">${this.escapeHtml(card.front)}</div>
                    </div>
                    <div class="flashcard-question">
                        <div class="flashcard-label">Answer</div>
                        <div class="flashcard-text">${this.escapeHtml(card.back)}</div>
                        ${card.tags && card.tags.length > 0 ? `<p style="margin-top: 0.5rem; font-size: 0.9rem;">Tags: ${card.tags.join(', ')}</p>` : ''}
                    </div>
                    <div>
                        <button class="btn" data-grade="0">Again (1)</button>
                        <button class="btn" data-grade="1">Hard (2)</button>
                        <button class="btn" data-grade="2">Good (3)</button>
                        <button class="btn" data-grade="3">Easy (4)</button>
                    </div>
                `}
            </div>
        `;

        if (!flipped) {
            const revealBtn = document.getElementById('reveal-btn');
            revealBtn.addEventListener('click', onReveal);

            const spaceHandler = (e) => {
                if (e.key === ' ' || e.key === 'Spacebar') {
                    e.preventDefault();
                    document.removeEventListener('keydown', spaceHandler);
                    onReveal();
                }
            };
            document.addEventListener('keydown', spaceHandler);
        } else {
            document.querySelectorAll('[data-grade]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const grade = parseInt(e.currentTarget.getAttribute('data-grade'));
                    onGrade(grade);
                });
            });

            const numHandler = (e) => {
                if (e.key >= '1' && e.key <= '4') {
                    e.preventDefault();
                    document.removeEventListener('keydown', numHandler);
                    onGrade(parseInt(e.key) - 1);
                }
            };
            document.addEventListener('keydown', numHandler);
        }
    }

    gradeCard(card, grade) {
        let progress = Storage.getCardProgress(card.id);
        if (!progress) {
            progress = SpacedRepetition.initCard();
        }

        progress = SpacedRepetition.gradeCard(progress, grade);
        Storage.setCardProgress(card.id, progress);

        const stats = Storage.getStats();
        Storage.updateStats({
            totalReviews: stats.totalReviews + 1
        });
        Storage.updateStreak();
    }

    showReviewComplete(sessionStats, subjectId, unitSlug, mode) {
        const total = sessionStats.correct + sessionStats.incorrect;

        this.appEl.innerHTML = `
            <div class="empty-state">
                <h2>Session Complete</h2>
                <p>You reviewed ${total} cards.</p>
                <p>Correct: ${sessionStats.correct} | Incorrect: ${sessionStats.incorrect}</p>
                <p>
                    <a href="#/" class="btn">Dashboard</a>
                    ${mode === 'unit' ? `<a href="#/subject/${subjectId}" class="btn">Back</a>` : ''}
                </p>
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

    async renderQuiz(subjectId, unitSlug) {
        this.cleanup();
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        if (unit.quiz.length === 0) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <p>No quiz questions available.</p>
                    <p><a href="#/subject/${subjectId}">Back</a></p>
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

        const cleanup = () => {};
        this.currentCleanup = cleanup;

        const render = () => {
            if (currentIndex >= questions.length) {
                cleanup();
                this.showQuizComplete(score, questions.length, subjectId, unitSlug);
                return;
            }

            const question = questions[currentIndex];
            
            const shuffled = question.choices.map((choice, idx) => ({ choice, idx }));
            for (let i = shuffled.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
            const correctShuffledIndex = shuffled.findIndex(s => s.idx === question.answer_index);

            this.appEl.innerHTML = `
                <div class="quiz-question">
                    <p><a href="#/subject/${subjectId}">← Back</a></p>

                    <h2>${unitTitle} - Quiz</h2>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${(currentIndex / questions.length) * 100}%"></div>
                    </div>
                    <p>Question ${currentIndex + 1} of ${questions.length}</p>

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

                            return `<div class="${className}" data-choice="${idx}">${this.escapeHtml(item.choice)}</div>`;
                        }).join('')}
                    </div>

                    ${answered ? `
                        <div class="explanation">
                            <div class="explanation-label">
                                ${selectedChoice === correctShuffledIndex ? 'Correct' : 'Incorrect'}
                            </div>
                            <p>${this.escapeHtml(question.explanation)}</p>
                        </div>
                        <button class="btn" id="next-btn">Next</button>
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

    showQuizComplete(score, total, subjectId, unitSlug) {
        const percentage = Math.round((score / total) * 100);
        
        const stats = Storage.getStats();
        Storage.updateStats({
            quizAttempts: stats.quizAttempts + 1
        });

        this.appEl.innerHTML = `
            <div class="empty-state">
                <h2>Quiz Complete</h2>
                <p>Score: ${score} / ${total} (${percentage}%)</p>
                <p>
                    <a href="#/quiz/${subjectId}/${unitSlug}" class="btn">Retake</a>
                    <a href="#/subject/${subjectId}" class="btn">Back</a>
                </p>
            </div>
        `;
    }

    async renderMatch(subjectId, unitSlug) {
        this.cleanup();
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        const matchableCards = unit.cards.filter(c => 
            c.type === 'recall' || c.type === 'identify'
        );

        if (matchableCards.length < 4) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <p>Not enough cards for match game.</p>
                    <p><a href="#/subject/${subjectId}">Back</a></p>
                </div>
            `;
            return;
        }

        const selected = matchableCards.sort(() => Math.random() - 0.5).slice(0, 6);
        
        const pairs = [];
        selected.forEach(card => {
            pairs.push({ text: card.front, pairId: card.id, type: 'front' });
            pairs.push({ text: card.back, pairId: card.id, type: 'back' });
        });

        pairs.sort(() => Math.random() - 0.5);

        this.startMatchGame(pairs, subjectId, unitSlug, unit.title);
    }

    startMatchGame(pairs, subjectId, unitSlug, unitTitle) {
        let selected = [];
        let matched = new Set();
        let startTime = Date.now();
        let timerInterval = null;

        const cleanup = () => {
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
        };
        this.currentCleanup = cleanup;

        const render = () => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;

            this.appEl.innerHTML = `
                <div class="match-game">
                    <p><a href="#/subject/${subjectId}">← Back</a></p>

                    <div class="match-header">
                        <h2>${unitTitle} - Match</h2>
                        <div class="match-timer">${minutes}:${seconds.toString().padStart(2, '0')}</div>
                    </div>
                    <p>Match ${pairs.length / 2} pairs.</p>

                    <div class="match-grid">
                        ${pairs.map((pair, idx) => {
                            let className = 'match-card';
                            if (matched.has(idx)) className += ' matched';
                            if (selected.includes(idx)) className += ' selected';

                            return `<div class="${className}" data-idx="${idx}" data-pair="${pair.pairId}">${this.escapeHtml(pair.text)}</div>`;
                        }).join('')}
                    </div>

                    <p>Matched: ${matched.size / 2} / ${pairs.length / 2}</p>
                </div>
            `;

            document.querySelectorAll('.match-card:not(.matched)').forEach(el => {
                el.addEventListener('click', (e) => {
                    const idx = parseInt(e.currentTarget.getAttribute('data-idx'));

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
                                    cleanup();
                                    const finalTime = Math.floor((Date.now() - startTime) / 1000);
                                    setTimeout(() => this.showMatchComplete(finalTime, subjectId, unitSlug), 300);
                                    return;
                                }
                            } else {
                                setTimeout(() => {
                                    selected = [];
                                    render();
                                }, 800);
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
                <h2>Complete</h2>
                <p>Time: ${minutes}:${secs.toString().padStart(2, '0')}</p>
                <p>
                    <a href="#/match/${subjectId}/${unitSlug}" class="btn">Play Again</a>
                    <a href="#/subject/${subjectId}" class="btn">Back</a>
                </p>
            </div>
        `;
    }

    async renderTermsDrill(subjectId, unitSlug) {
        this.cleanup();
        const index = await this.loadSubjectIndex(subjectId);
        const unitInfo = index.units.find(u => u.slug === unitSlug);
        const unit = await this.loadUnit(subjectId, unitInfo.file);

        if (!unit.glossary || unit.glossary.length === 0) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <p>No glossary terms available.</p>
                    <p><a href="#/subject/${subjectId}">Back</a></p>
                </div>
            `;
            return;
        }

        // Convert glossary to card-like format for review
        const termCards = unit.glossary.map((entry, idx) => ({
            id: `u${unit.unit}-g-${this.slugify(entry.term)}`,
            front: entry.definition,
            back: entry.term,
            accept: [entry.term],
            type: 'identify',
            tags: ['glossary']
        }));

        const progress = Storage.getAllCardProgress();
        const settings = Storage.getSettings();

        const dueCardIds = SpacedRepetition.getDueCards(progress);
        const dueCards = termCards.filter(c => dueCardIds.includes(c.id));
        
        const newCardIds = SpacedRepetition.getNewCards(termCards, progress, settings.newCardsPerDay);
        const newCards = termCards.filter(c => newCardIds.includes(c.id));

        const queue = [...dueCards, ...newCards];

        if (queue.length === 0) {
            this.appEl.innerHTML = `
                <div class="empty-state">
                    <h2>All terms mastered</h2>
                    <p>Come back later for review.</p>
                    <p><a href="#/lesson/${subjectId}/${unitSlug}">Back to Lesson</a></p>
                </div>
            `;
            return;
        }

        this.startReviewSession(queue, subjectId, unitSlug, 'terms', settings.typedAnswers);
    }

    slugify(text) {
        return text.toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    renderSettings() {
        this.cleanup();
        const settings = Storage.getSettings();
        const stats = Storage.getStats();

        this.appEl.innerHTML = `
            <h1>Settings</h1>

            <h3>Study Settings</h3>
            <div class="input-group">
                <label for="new-cards-per-day">New cards per day</label>
                <input type="number" id="new-cards-per-day" value="${settings.newCardsPerDay}" min="1" max="100">
            </div>
            <div class="input-group">
                <label>
                    <input type="checkbox" id="typed-answers" ${settings.typedAnswers ? 'checked' : ''}>
                    Typed answers (with lenient checking)
                </label>
            </div>
            <button class="btn" id="save-settings-btn">Save</button>

            <h3>Progress Data</h3>
            <p>Export your progress to move between devices.</p>
            <button class="btn" id="export-btn">Export</button>
            <button class="btn" id="import-btn">Import</button>
            <input type="file" id="import-file" accept=".json" style="display: none;">

            <h3>Statistics</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">${stats.totalReviews}</span>
                    <span class="stat-label">Reviews</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">${stats.quizAttempts}</span>
                    <span class="stat-label">Quizzes</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">${stats.streak}</span>
                    <span class="stat-label">Streak</span>
                </div>
            </div>

            <h3>Danger Zone</h3>
            <p>Delete all progress (cannot be undone).</p>
            <button class="btn" id="reset-btn">Reset All Data</button>
        `;

        document.getElementById('save-settings-btn').addEventListener('click', () => {
            const newCardsPerDay = parseInt(document.getElementById('new-cards-per-day').value);
            const typedAnswers = document.getElementById('typed-answers').checked;
            Storage.setSetting('newCardsPerDay', newCardsPerDay);
            Storage.setSetting('typedAnswers', typedAnswers);
            this.showAlert('Settings saved', 'success');
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
                        this.showAlert('Progress imported', 'success');
                        setTimeout(() => window.location.reload(), 1500);
                    } catch (error) {
                        this.showAlert('Failed to import', 'error');
                    }
                };
                reader.readAsText(file);
            }
        });

        document.getElementById('reset-btn').addEventListener('click', () => {
            if (confirm('Delete all progress? Cannot be undone.')) {
                if (confirm('Really delete everything?')) {
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
        setTimeout(() => alert.remove(), 2000);
    }

    showError(message) {
        this.appEl.innerHTML = `
            <div class="empty-state">
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

const app = new StudyApp();
app.init();
