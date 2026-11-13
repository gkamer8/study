// FSRS (Free Spaced Repetition Scheduler) algorithm
// Simplified implementation with SM-2 fallback for compatibility

export const SpacedRepetition = {
    // Initialize card state (FSRS format, compatible with old SM-2)
    initCard() {
        return {
            // FSRS parameters
            stability: 0,
            difficulty: 5,
            
            // SM-2 compatibility
            interval: 0,
            repetitions: 0,
            easeFactor: 2.5,
            
            nextReview: Date.now(),
            lastReview: null,
            isNew: true,
            algorithm: 'fsrs' // Track which algorithm is in use
        };
    },

    // FSRS parameters
    w: [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61],

    // Grade a card review
    // quality: 0 = Again, 1 = Hard, 2 = Good, 3 = Easy
    gradeCard(cardState, quality) {
        const state = { ...cardState };
        const now = Date.now();
        
        state.lastReview = now;
        state.isNew = false;

        // Use FSRS if available, otherwise fall back to SM-2
        if (state.algorithm === 'fsrs' || !state.algorithm) {
            return this.gradeCardFSRS(state, quality, now);
        } else {
            return this.gradeCardSM2(state, quality, now);
        }
    },

    // FSRS implementation (simplified)
    gradeCardFSRS(state, quality, now) {
        const elapsed = state.lastReview ? (now - state.lastReview) / (24 * 60 * 60 * 1000) : 0;

        // Update difficulty
        const deltaD = quality - 2;
        state.difficulty = Math.max(1, Math.min(10, state.difficulty - this.w[6] * deltaD));

        if (quality === 0) {
            // Again: reset
            state.stability = Math.max(1, state.stability * this.w[11]);
            state.repetitions = 0;
        } else {
            // Calculate new stability
            let S = 0;
            if (state.repetitions === 0) {
                S = this.w[quality];
            } else {
                const retrievability = Math.pow(1 + elapsed / (9 * state.stability), -1);
                S = state.stability * (1 + Math.exp(this.w[8]) * 
                    (11 - state.difficulty) * 
                    Math.pow(state.stability, -this.w[9]) * 
                    (Math.exp((1 - retrievability) * this.w[10]) - 1));
            }
            state.stability = Math.max(0.1, S);
            state.repetitions += 1;
        }

        // Calculate interval in days
        state.interval = Math.max(1, Math.round(state.stability * 9 * (1 / 0.9 - 1)));
        
        // Calculate next review date
        const intervalMs = state.interval * 24 * 60 * 60 * 1000;
        state.nextReview = now + intervalMs;

        state.algorithm = 'fsrs';
        return state;
    },

    // SM-2 fallback for old cards
    gradeCardSM2(state, quality, now) {
        const oldEF = state.easeFactor;
        state.easeFactor = Math.max(1.3, oldEF + (0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02)));

        if (quality < 2) {
            state.repetitions = 0;
            state.interval = quality === 0 ? 1 / (24 * 60) : 10 / (24 * 60); // minutes to days
        } else {
            state.repetitions += 1;
            if (state.repetitions === 1) {
                state.interval = 1;
            } else if (state.repetitions === 2) {
                state.interval = 6;
            } else {
                state.interval = Math.round(state.interval * state.easeFactor);
                if (quality === 3) {
                    state.interval = Math.round(state.interval * 1.3);
                }
            }
        }

        const intervalMs = state.interval < 1 
            ? state.interval * 24 * 60 * 60 * 1000
            : state.interval * 24 * 60 * 60 * 1000;
        
        state.nextReview = now + intervalMs;
        state.algorithm = 'sm2';
        
        return state;
    },

    // Check if card is due for review
    isDue(cardState) {
        if (!cardState || cardState.isNew) return false;
        return Date.now() >= cardState.nextReview;
    },

    // Get cards due today
    getDueCards(allProgress) {
        const due = [];
        for (const [cardId, progress] of Object.entries(allProgress)) {
            if (this.isDue(progress)) {
                due.push(cardId);
            }
        }
        return due;
    },

    // Get new cards (never seen before)
    getNewCards(allCards, allProgress, limit) {
        const newCards = [];
        for (const card of allCards) {
            if (!allProgress[card.id]) {
                newCards.push(card.id);
                if (newCards.length >= limit) break;
            }
        }
        return newCards;
    },

    // Format interval for display
    formatInterval(days) {
        if (days < 1) {
            const minutes = Math.round(days * 24 * 60);
            return `${minutes}m`;
        } else if (days < 30) {
            return `${Math.round(days)}d`;
        } else if (days < 365) {
            return `${Math.round(days / 30)}mo`;
        } else {
            return `${(days / 365).toFixed(1)}y`;
        }
    }
};
