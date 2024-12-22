from difflib import get_close_matches
import re

class TextProcessor:
    def __init__(self, dictionary_path):
        self.dictionary = self.load_dictionary(dictionary_path)
        self.word_freq = {}  # For storing word frequencies
        self.build_word_frequencies()

    def load_dictionary(self, path):
        """Load Sinhala dictionary and create a set for O(1) lookup"""
        with open(path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file.readlines())

    def build_word_frequencies(self):
        """Build character frequency distributions for Sinhala words"""
        for word in self.dictionary:
            for char in word:
                if char not in self.word_freq:
                    self.word_freq[char] = {}
                
                # Count character positions
                for i, c in enumerate(word):
                    if c not in self.word_freq[char]:
                        self.word_freq[char][i] = 0
                    self.word_freq[char][i] += 1

    def get_character_similarity(self, word1, word2):
        """Calculate character-level similarity between two words"""
        if not word1 or not word2:
            return 0
        
        matches = sum(1 for c1, c2 in zip(word1, word2) if c1 == c2)
        return matches / max(len(word1), len(word2))

    def get_suggestions(self, word, max_suggestions=5, min_similarity=0.6):
        """Get spell-check suggestions for a word"""
        if word in self.dictionary:
            return []

        suggestions = []
        word_len = len(word)

        # Get close matches based on edit distance
        close_matches = get_close_matches(word, self.dictionary, n=max_suggestions, cutoff=min_similarity)
        
        # Add matches with similar length
        len_range = 2  # Allow words within ±2 characters
        similar_length_words = [w for w in self.dictionary 
                              if abs(len(w) - word_len) <= len_range 
                              and self.get_character_similarity(word, w) >= min_similarity]
        
        # Combine and sort suggestions
        all_suggestions = set(close_matches + similar_length_words)
        
        # Score each suggestion
        for suggestion in all_suggestions:
            score = self.calculate_suggestion_score(word, suggestion)
            suggestions.append((suggestion, score))
        
        # Sort by score and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:max_suggestions]

    def calculate_suggestion_score(self, original, suggestion):
        """Calculate how good a suggestion is based on multiple factors"""
        # Base similarity score
        base_score = self.get_character_similarity(original, suggestion)
        
        # Length similarity score (penalize big length differences)
        len_diff = abs(len(original) - len(suggestion))
        length_score = 1 / (1 + len_diff)
        
        # Position-based character frequency score
        freq_score = 0
        for i, char in enumerate(suggestion):
            if char in self.word_freq and i in self.word_freq[char]:
                freq_score += self.word_freq[char][i]
        freq_score = freq_score / (len(suggestion) * 100)  # Normalize
        
        # Combine scores with weights
        final_score = (base_score * 0.5 + 
                      length_score * 0.3 + 
                      freq_score * 0.2)
        
        return final_score