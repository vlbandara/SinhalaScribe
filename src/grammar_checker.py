# # grammar_checker.py
# class GrammarChecker:
#     def __init__(self, dictionary_path, bert_model=None):
#         self.dictionary = self.load_dictionary(dictionary_path)
#         self.bert_model = bert_model
        
#     def load_dictionary(self, path):
#         """Load Sinhala dictionary from file"""
#         try:
#             with open(path, 'r', encoding='utf-8') as file:
#                 return set(word.strip() for word in file.readlines())
#         except Exception as e:
#             print(f"Error loading dictionary: {e}")
#             return set()
    
#     def check_grammar(self, text):
#         """Check grammar rules in the text"""
#         sentences = [s.strip() for s in text.split('.') if s.strip()]
#         errors = []
#         correct = []
        
#         for sentence in sentences:
#             words = sentence.split()
#             if not words:
#                 continue
                
#             if words[0] == "මම":
#                 if not words[-1].endswith("මි"):
#                     errors.append({
#                         'sentence': sentence,
#                         'type': 'මම_rule',
#                         'suggestion': self.get_mi_suggestion(sentence)
#                     })
#                 else:
#                     correct.append(sentence)
                    
#             elif words[0] == "අපි":
#                 if not words[-1].endswith("මු"):
#                     errors.append({
#                         'sentence': sentence,
#                         'type': 'අපි_rule',
#                         'suggestion': self.get_mu_suggestion(sentence)
#                     })
#                 else:
#                     correct.append(sentence)
                    
#         return {
#             'errors': errors,
#             'correct': correct
#         }
        
#     def get_mi_suggestion(self, sentence):
#         """Generate suggestion for මම rule"""
#         words = sentence.split()
#         if len(words) > 1:
#             base_word = words[-1].rstrip('වා')
#             return ' '.join(words[:-1]) + ' ' + base_word + 'මි'
#         return sentence
        
#     def get_mu_suggestion(self, sentence):
#         """Generate suggestion for අපි rule"""
#         words = sentence.split()
#         if len(words) > 1:
#             base_word = words[-1].rstrip('වා')
#             return ' '.join(words[:-1]) + ' ' + base_word + 'මු'
#         return sentence

#     def get_word_suggestions(self, current_input, is_space_pressed=False):
#         """Get word suggestions based on input"""
#         if is_space_pressed and self.bert_model:
#             try:
#                 # Use BERT model for next word prediction
#                 text_with_mask = current_input + " " + self.bert_model.tokenizer.mask_token
#                 predictions = self.bert_model(text_with_mask)
#                 return [pred['token_str'] for pred in predictions[:5]]
#             except Exception as e:
#                 print(f"Error in BERT prediction: {e}")
#                 return []
#         else:
#             # Use dictionary for word completion
#             if not current_input:
#                 return []
#             return [word for word in self.dictionary 
#                    if word.startswith(current_input)][:5]


# grammar_checker.py

class GrammarChecker:
    def __init__(self, dictionary_path, bert_model=None):
        self.dictionary = self.load_dictionary(dictionary_path)
        self.bert_model = bert_model
        # Define descriptions for each error type
        self.error_descriptions = {
            'මම_rule': "Should end with 'මි'",
            'අපි_rule': "Should end with 'මු'",
            # Add more error types and their descriptions here
        }
        
    def load_dictionary(self, path):
        """Load Sinhala dictionary from file"""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return set(word.strip() for word in file.readlines())
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            return set()
    
    def check_grammar(self, text):
        """Check grammar rules in the text"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        errors = []
        correct = []
        
        for sentence in sentences:
            words = sentence.split()
            if not words:
                continue
                
            if words[0] == "මම":
                if not words[-1].endswith("මි"):
                    errors.append({
                        'sentence': sentence,
                        'type': 'මම_rule',
                        'description': self.error_descriptions.get('මම_rule', 'Grammar error detected.'),
                        'suggestion': self.get_mi_suggestion(sentence)
                    })
                else:
                    correct.append(sentence)
                    
            elif words[0] == "අපි":
                if not words[-1].endswith("මු"):
                    errors.append({
                        'sentence': sentence,
                        'type': 'අපි_rule',
                        'description': self.error_descriptions.get('අපි_rule', 'Grammar error detected.'),
                        'suggestion': self.get_mu_suggestion(sentence)
                    })
                else:
                    correct.append(sentence)
                    
            # Add more grammar rules here as needed
                
        return {
            'errors': errors,
            'correct': correct
        }
        
    def get_mi_suggestion(self, sentence):
        """Generate suggestion for මම rule"""
        words = sentence.split()
        if len(words) > 1:
            last_word = words[-1]
            if last_word.endswith('වා'):
                base_word = last_word[:-2]  # Remove 'වා'
                return ' '.join(words[:-1]) + ' ' + base_word + 'මි'
            elif last_word.endswith('ව'):
                base_word = last_word[:-1]  # Remove 'ව'
                return ' '.join(words[:-1]) + ' ' + base_word + 'මි'
            else:
                # Handle other cases or return the original sentence
                return sentence
        return sentence
        
    def get_mu_suggestion(self, sentence):
        """Generate suggestion for අපි rule"""
        words = sentence.split()
        if len(words) > 1:
            last_word = words[-1]
            if last_word.endswith('වා'):
                base_word = last_word[:-2]  # Remove 'වා'
                return ' '.join(words[:-1]) + ' ' + base_word + 'මු'
            elif last_word.endswith('ව'):
                base_word = last_word[:-1]  # Remove 'ව'
                return ' '.join(words[:-1]) + ' ' + base_word + 'මු'
            else:
                # Handle other cases or return the original sentence
                return sentence
        return sentence

    def get_word_suggestions(self, current_input, is_space_pressed=False):
        """Get word suggestions based on input"""
        if is_space_pressed and self.bert_model:
            try:
                # Use BERT model for next word prediction
                text_with_mask = current_input + " " + self.bert_model.tokenizer.mask_token
                predictions = self.bert_model(text_with_mask)
                return [pred['token_str'].strip() for pred in predictions[:5]]
            except Exception as e:
                print(f"Error in BERT prediction: {e}")
                return []
        else:
            # Use dictionary for word completion
            if not current_input:
                return []
            return [word for word in self.dictionary 
                   if word.startswith(current_input)][:5]