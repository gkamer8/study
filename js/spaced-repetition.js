// SM-2 algorithm for spaced repetition
// Based on SuperMemo 2 (Wozniak, 1990)

export const SpacedRepetition = {
    // Initialize card state
    initCard() {
        return {
            interval: 0,
            repetitions: 0,
            easeFactor: 2.5,
            nextReview: Date.now(),
            lastReview: null,
            isNew: true
        };
    },

    // Grade a card review
    // quality: 0 = Again, 1 = Hard, 2 = Good, 3 = Easy
    gradeCard(cardState, quality) {
        const state = { ...cardState };
        const now = Date.now();
        
        state.lastReview = now;
        state.isNew = false;

        // Update ease factor
        const oldEF = state.easeFactor;
        state.easeFactor = Math.max(1.3, oldEF + (0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02)));

        if (quality < 2) {
            // Again or Hard: reset repetitions but keep ease factor
            state.repetitions = 0;
            state.interval = quality === 0 ? 1 : 10; // 1 min or 10 min
        } else {
            // Good or Easy
            state.repetitions += 1;

            if (state.repetitions === 1) {
                state.interval = 1; // 1 day
            } else if (state.repetitions === 2) {
                state.interval = 6; // 6 days
            } else {
                state.interval = Math.round(state.interval * state.easeFactor);
                if (quality === 3) {
                    // Easy: add bonus
                    state.interval = Math.round(state.interval * 1.3);
                }
            }
        }

        // Calculate next review date
        const intervalMs = state.interval < 1 
            ? state.interval * 60 * 1000 // minutes
            : state.interval * 24 * 60 * 60 * 1000; // days
        
        state.nextReview = now + intervalMs;

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
