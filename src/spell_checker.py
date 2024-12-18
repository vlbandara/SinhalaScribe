import re
from typing import List, Tuple
from scipy.spatial.distance import edit_distance

class SinhalaSpellChecker:
    def __init__(self, dictionary_path: str):
        """
        Initialize the spell checker with a Sinhala dictionary
        
        :param dictionary_path: Path to the dictionary text file
        """
        self.dictionary = self._load_dictionary(dictionary_path)
    
    def _load_dictionary(self, path: str) -> set:
        """
        Load dictionary words from file
        
        :param path: Path to dictionary file
        :return: Set of dictionary words
        """
        with open(path, 'r', encoding='utf-8') as f:
            return set(word.strip() for word in f)
    
    def suggest_corrections(self, word: str, max_suggestions: int = 5) -> List[Tuple[str, float]]:
        """
        Generate spell correction suggestions
        
        :param word: Misspelled word
        :param max_suggestions: Maximum number of suggestions
        :return: List of (suggested word, similarity score) tuples
        """
        # If word is in dictionary, return it
        if word in self.dictionary:
            return [(word, 1.0)]
        
        # Calculate edit distances to find closest matches
        suggestions = []
        for dict_word in self.dictionary:
            # Calculate normalized edit distance
            dist = edit_distance(word, dict_word)
            similarity = 1 - (dist / max(len(word), len(dict_word)))
            
            # Only keep suggestions above a similarity threshold
            if similarity > 0.6:
                suggestions.append((dict_word, similarity))
        
        # Sort suggestions by similarity and return top max_suggestions
        return sorted(suggestions, key=lambda x: x[1], reverse=True)[:max_suggestions]
    
    def correct_text(self, text: str) -> str:
        """
        Correct spelling in the entire text
        
        :param text: Input text
        :return: Text with spelling corrections
        """
        # Split text into words
        words = re.findall(r'\S+', text)
        
        # Correct each word
        corrected_words = []
        for word in words:
            # Check if word needs correction
            if word not in self.dictionary:
                suggestions = self.suggest_corrections(word)
                if suggestions:
                    # Replace with the best suggestion
                    corrected_words.append(suggestions[0][0])
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        
        # Reconstruct text
        return ' '.join(corrected_words)