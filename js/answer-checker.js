// Lenient answer checking for typed flashcard responses

export const AnswerChecker = {
    // Main checking function - uses accept array if present
    check(userAnswer, card) {
        if (!userAnswer) return false;

        // Use accept array if present, otherwise fall back to back field
        const acceptedAnswers = card.accept || [card.back];
        
        // First entry in accept is canonical
        const canonical = acceptedAnswers[0];
        
        // Check if this looks like it needs exact matching
        const needsExact = this.needsExactMatch(canonical);
        
        for (const answer of acceptedAnswers) {
            if (needsExact) {
                if (this.exactMatch(userAnswer, answer)) {
                    return true;
                }
            } else {
                if (this.matchesAnswer(userAnswer, answer)) {
                    return true;
                }
            }
        }
        
        return false;
    },

    // Determine if answer needs exact matching (no typo tolerance)
    needsExactMatch(answer) {
        const normalized = this.normalize(answer);
        
        // Very short answers (≤3 chars) need exact match
        if (normalized.length <= 3) return true;
        
        // Gene symbols: capital letters with numbers, or format like TP53, BRCA1
        if (/^[A-Z]{2,}[0-9]+/.test(answer) || /^[A-Z]{3,}[0-9]*$/.test(answer)) {
            return true;
        }
        
        // Identifiers: contains underscores, dots, or colon patterns
        if (/[_.:]+/.test(answer)) return true;
        
        // Numbers with units need exact match
        if (/^[\d.,]+\s*(bp|kb|Mb|Gb|nt|aa|kDa|Da|%|mM|μM|nM)/.test(answer)) {
            return true;
        }
        
        return false;
    },

    // Exact match after normalization (no typo tolerance)
    exactMatch(user, correct) {
        return this.normalize(user) === this.normalize(correct);
    },

    // Lenient matching with typo tolerance
    matchesAnswer(user, correct) {
        const u = this.normalize(user);
        const c = this.normalize(correct);

        // Exact match
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
        s = s.replace(/[-–—]/g, '');
        
        // Normalize primes (5' / 5′ / 5 prime)
        s = s.replace(/['′´`]/g, '');
        s = s.replace(/\b(\d+)\s*prime\b/g, '$1');
        
        // Normalize arrows
        s = s.replace(/[→←↔⇒⇐⇔]/g, 'to');
        
        // k-mer and kmer are the same
        s = s.replace(/(\d+)\s*-\s*mer\b/g, '$1mer');
        
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
        const commonWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being']);
        
        const correctWords = correct.split(/\s+/).filter(w => 
            w.length > 2 && !commonWords.has(w)
        );
        
        if (correctWords.length === 0) return false;

        let matches = 0;
        for (const word of correctWords) {
            if (user.includes(word)) {
                matches++;
            }
        }

        const threshold = Math.ceil(correctWords.length * 0.6);
        return matches >= threshold;
    }
};
