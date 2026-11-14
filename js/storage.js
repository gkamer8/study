// Storage management for progress and settings

const STORAGE_KEYS = {
    CARD_PROGRESS: 'study_card_progress',
    SETTINGS: 'study_settings',
    STATS: 'study_stats',
    CLOZE: 'study_cloze_state'
};

export const Storage = {
    // Card progress
    getCardProgress(cardId) {
        const data = this.getAllCardProgress();
        return data[cardId] || null;
    },

    getAllCardProgress() {
        const raw = localStorage.getItem(STORAGE_KEYS.CARD_PROGRESS);
        return raw ? JSON.parse(raw) : {};
    },

    setCardProgress(cardId, progress) {
        const data = this.getAllCardProgress();
        data[cardId] = progress;
        localStorage.setItem(STORAGE_KEYS.CARD_PROGRESS, JSON.stringify(data));
    },

    // Cloze state (for Bible learning steps)
    getCloze(cardId) {
        const raw = localStorage.getItem(STORAGE_KEYS.CLOZE);
        const data = raw ? JSON.parse(raw) : {};
        return data[cardId] || null;
    },

    setCloze(cardId, state) {
        const raw = localStorage.getItem(STORAGE_KEYS.CLOZE);
        const data = raw ? JSON.parse(raw) : {};
        data[cardId] = state;
        localStorage.setItem(STORAGE_KEYS.CLOZE, JSON.stringify(data));
    },

    clearCloze(cardId) {
        const raw = localStorage.getItem(STORAGE_KEYS.CLOZE);
        const data = raw ? JSON.parse(raw) : {};
        delete data[cardId];
        localStorage.setItem(STORAGE_KEYS.CLOZE, JSON.stringify(data));
    },

    // Settings
    getSettings() {
        const raw = localStorage.getItem(STORAGE_KEYS.SETTINGS);
        return raw ? JSON.parse(raw) : {
            newCardsPerDay: 20,
            theme: 'light',
            typedAnswers: true  // Default to typed answers
        };
    },

    setSetting(key, value) {
        const settings = this.getSettings();
        settings[key] = value;
        localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
    },

    // Stats
    getStats() {
        const raw = localStorage.getItem(STORAGE_KEYS.STATS);
        return raw ? JSON.parse(raw) : {
            streak: 0,
            lastReviewDate: null,
            totalReviews: 0,
            quizAttempts: 0
        };
    },

    updateStats(updates) {
        const stats = this.getStats();
        Object.assign(stats, updates);
        localStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(stats));
    },

    updateStreak() {
        const stats = this.getStats();
        const today = new Date().toDateString();
        
        if (stats.lastReviewDate === today) {
            return stats.streak;
        }
        
        const yesterday = new Date(Date.now() - 86400000).toDateString();
        const newStreak = stats.lastReviewDate === yesterday ? stats.streak + 1 : 1;
        
        this.updateStats({
            streak: newStreak,
            lastReviewDate: today
        });
        
        return newStreak;
    },

    // Export/Import
    exportData() {
        const raw = localStorage.getItem(STORAGE_KEYS.CLOZE);
        const cloze = raw ? JSON.parse(raw) : {};
        return {
            cardProgress: this.getAllCardProgress(),
            settings: this.getSettings(),
            stats: this.getStats(),
            cloze: cloze,
            exportDate: new Date().toISOString()
        };
    },

    importData(data) {
        if (data.cardProgress) {
            localStorage.setItem(STORAGE_KEYS.CARD_PROGRESS, JSON.stringify(data.cardProgress));
        }
        if (data.settings) {
            localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(data.settings));
        }
        if (data.stats) {
            localStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(data.stats));
        }
        if (data.cloze) {
            localStorage.setItem(STORAGE_KEYS.CLOZE, JSON.stringify(data.cloze));
        }
    },

    clearAllData() {
        localStorage.removeItem(STORAGE_KEYS.CARD_PROGRESS);
        localStorage.removeItem(STORAGE_KEYS.SETTINGS);
        localStorage.removeItem(STORAGE_KEYS.STATS);
        localStorage.removeItem(STORAGE_KEYS.CLOZE);
    }
};
