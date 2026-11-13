// Lenient answer checking for typed flashcard responses

export const AnswerChecker = {
    // Main checking function
    check(userAnswer, correctAnswer, alternates = []) {
        if (!userAnswer || !correctAnswer) return false;

        // Check against main answer and all alternates
        const allAnswers = [correctAnswer, ...alternates];
        
        for (const answer of allAnswers) {
            if (this.matchesAnswer(userAnswer, answer)) {
                return true;
            }
        }
        
        return false;
    },

    // Check if user answer matches a single correct answer
    matchesAnswer(user, correct) {
        // Normalize both strings
        const u = this.normalize(user);
        const c = this.normalize(correct);

        // Exact match after normalization
        if (u === c) return true;

        // For short answers, check edit distance
        if (c.length <= 20) {
            const distance = this.editDistance(u, c);
            // Stricter threshold for very short answers
            const threshold = c.length <= 3 ? 0 : (c.length <= 5 ? 1 : 2);
            if (distance <= threshold) return true;
        }

        // For longer answers, check if key terms are present
        if (c.length > 20) {
            return this.containsKeyTerms(u, c);
        }

        return false;
    },

    // Normalize a string for comparison
    normalize(text) {
        let s = text.toLowerCase().trim();
        
        // Remove common punctuation
        s = s.replace(/[.,;:!?'"()\[\]{}]/g, ' ');
        
        // Normalize whitespace
        s = s.replace(/\s+/g, ' ').trim();
        
        // Normalize hyphens and dashes
        s = s.replace(/[-–—]/g, ' ');
        
        // Greek letter normalization
        const greekMap = {
            'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ',
            'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ',
            'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ',
            'nu': 'ν', 'xi': 'ξ', 'omicron': 'ο', 'pi': 'π',
            'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ',
            'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω'
        };
        
        for (const [spelled, symbol] of Object.entries(greekMap)) {
            s = s.replace(new RegExp('\\b' + spelled + '\\b', 'gi'), symbol);
        }
        
        // Common abbreviations
        const abbrevMap = {
            'dna': 'deoxyribonucleic acid',
            'rna': 'ribonucleic acid',
            'mrna': 'messenger rna',
            'trna': 'transfer rna',
            'rrna': 'ribosomal rna',
            'atp': 'adenosine triphosphate',
            'dna': 'deoxyribonucleic acid',
            'pcr': 'polymerase chain reaction'
        };
        
        for (const [abbrev, full] of Object.entries(abbrevMap)) {
            const abbrevRegex = new RegExp('\\b' + abbrev + '\\b', 'gi');
            const fullRegex = new RegExp('\\b' + full + '\\b', 'gi');
            if (s.match(abbrevRegex) || s.match(fullRegex)) {
                s = s.replace(abbrevRegex, abbrev);
                s = s.replace(fullRegex, abbrev);
            }
        }
        
        return s;
    },

    // Levenshtein edit distance
    editDistance(a, b) {
        const matrix = [];

        for (let i = 0; i <= b.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= a.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= b.length; i++) {
            for (let j = 1; j <= a.length; j++) {
                if (b.charAt(i - 1) === a.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }

        return matrix[b.length][a.length];
    },

    // Check if user answer contains key terms from correct answer
    containsKeyTerms(user, correct) {
        // Split into words, filter out common words
        const commonWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being']);
        
        const correctWords = correct.split(/\s+/).filter(w => 
            w.length > 2 && !commonWords.has(w)
        );
        
        if (correctWords.length === 0) return false;

        // Check how many key terms are present
        let matches = 0;
        for (const word of correctWords) {
            if (user.includes(word)) {
                matches++;
            }
        }

        // Require at least 60% of key terms
        const threshold = Math.ceil(correctWords.length * 0.6);
        return matches >= threshold;
    },

    // Extract key terms from a multi-part answer (separated by semicolons)
    extractParts(answer) {
        return answer.split(/[;/]/).map(p => p.trim()).filter(p => p);
    }
};
