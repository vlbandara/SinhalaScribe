# # app.py
# import streamlit as st
# from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

# from model.grammar_checker import GrammarChecker

# class SinhalaScribeApp:
#     def __init__(self):
#         self.initialize_models()
        
#     def initialize_models(self):
#         # Initialize BERT model
#         @st.cache_resource
#         def load_bert():
#             try:
#                 model_name = "Ransaka/sinhala-bert-medium-v2"
#                 tokenizer = AutoTokenizer.from_pretrained(model_name)
#                 model = AutoModelForMaskedLM.from_pretrained(model_name)
#                 return pipeline('fill-mask', model=model, tokenizer=tokenizer)
#             except Exception as e:
#                 st.error(f"Error loading BERT model: {e}")
#                 return None
            
#         self.bert_model = load_bert()
#         self.grammar_checker = GrammarChecker(
#             "/Users/vinodlahiru/Documents/GitHub/SinhalaScribe/data/sinhala_dictionary.txt",
#             self.bert_model
#         )
        
#     def run(self):
#         st.title("SinhalaScribe Grammar Checker")
        
#         # Initialize session state
#         if 'current_text' not in st.session_state:
#             st.session_state.current_text = ""
#         if 'space_pressed' not in st.session_state:
#             st.session_state.space_pressed = False
            
#         # Text input with suggestions
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             text = st.text_area(
#                 "Enter text (Press space for BERT suggestions):", 
#                 value=st.session_state.current_text,
#                 key="text_input",
#                 height=200
#             )
                              
#         # Update suggestions based on input
#         if text != st.session_state.current_text:
#             st.session_state.current_text = text
#             words = text.split()
#             current_word = words[-1] if words else ""
            
#             # Detect space press
#             st.session_state.space_pressed = text.endswith(" ")
            
#             # Get suggestions
#             suggestions = self.grammar_checker.get_word_suggestions(
#                 current_word if not st.session_state.space_pressed else text.rstrip(),
#                 st.session_state.space_pressed
#             )
            
#             # Display suggestions
#             with col2:
#                 st.write("Suggestions:")
#                 for suggestion in suggestions:
#                     if st.button(suggestion, key=f"suggest_{suggestion}"):
#                         if st.session_state.space_pressed:
#                             # Add new word
#                             st.session_state.current_text = text + suggestion
#                         else:
#                             # Replace current word
#                             words = text.split()
#                             words[-1] = suggestion
#                             st.session_state.current_text = " ".join(words)
#                         st.rerun()
        
#         # Grammar checking
#         if text:
#             results = self.grammar_checker.check_grammar(text)
            
#             if results['errors']:
#                 st.error("Grammar Errors Found:")
#                 for error in results['errors']:
#                     st.write(f"❌ {error['sentence']}")
#                     st.write(f"Suggestion: {error['suggestion']}")
                    
#             if results['correct']:
#                 st.success("Correct Sentences:")
#                 for sentence in results['correct']:
#                     st.write(f"✓ {sentence}")

# def main():
#     app = SinhalaScribeApp()
#     app.run()

# if __name__ == "__main__":
#     main()




# # app.py
# import streamlit as st
# from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

# from model.grammar_checker import GrammarChecker

# class SinhalaScribeApp:
#     def __init__(self):
#         self.initialize_models()
        
#     def initialize_models(self):
#         # Initialize BERT model
#         @st.cache_resource
#         def load_bert():
#             try:
#                 model_name = "Ransaka/sinhala-bert-medium-v2"
#                 tokenizer = AutoTokenizer.from_pretrained(model_name)
#                 model = AutoModelForMaskedLM.from_pretrained(model_name)
#                 return pipeline('fill-mask', model=model, tokenizer=tokenizer)
#             except Exception as e:
#                 st.error(f"Error loading BERT model: {e}")
#                 return None
            
#         self.bert_model = load_bert()
#         self.grammar_checker = GrammarChecker(
#             "/Users/vinodlahiru/Documents/GitHub/SinhalaScribe/data/sinhala_dictionary.txt",
#             self.bert_model
#         )
        
#     def run(self):
#         st.title("SinhalaScribe Grammar Checker")
        
#         # Initialize session state
#         if 'current_text' not in st.session_state:
#             st.session_state.current_text = ""
#         if 'space_pressed' not in st.session_state:
#             st.session_state.space_pressed = False
            
#         # Text input with suggestions
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             text = st.text_area(
#                 "Enter text (Press space for BERT suggestions):", 
#                 value=st.session_state.current_text,
#                 key="text_input",
#                 height=200
#             )
                              
#         # Update suggestions based on input
#         if text != st.session_state.current_text:
#             st.session_state.current_text = text
#             words = text.split()
#             current_word = words[-1] if words else ""
            
#             # Detect space press
#             st.session_state.space_pressed = text.endswith(" ")
            
#             # Get suggestions
#             suggestions = self.grammar_checker.get_word_suggestions(
#                 current_word if not st.session_state.space_pressed else text.rstrip(),
#                 st.session_state.space_pressed
#             )
            
#             # Display suggestions
#             with col2:
#                 st.write("Suggestions:")
#                 for suggestion in suggestions:
#                     if st.button(suggestion, key=f"suggest_{suggestion}"):
#                         if st.session_state.space_pressed:
#                             # Add new word
#                             st.session_state.current_text = text + suggestion + " "
#                         else:
#                             # Replace current word
#                             words = text.split()
#                             words[-1] = suggestion
#                             st.session_state.current_text = " ".join(words) + " "
#                         st.experimental_rerun()
        
#         # Grammar checking
#         if text:
#             results = self.grammar_checker.check_grammar(text)
            
#             if results['errors']:
#                 st.markdown("❌ **Grammar Errors Found:**")
#                 for idx, error in enumerate(results['errors'], start=1):
#                     st.markdown(f"**{idx}. \"{error['sentence']}\"** - {error['description']}")
#                     st.markdown(f"   *Suggestion:* `{error['suggestion']}`")
                    
#             if results['correct']:
#                 st.success("✓ **Correct Sentences:**")
#                 for sentence in results['correct']:
#                     st.write(f"✓ {sentence}")

# def main():
#     app = SinhalaScribeApp()
#     app.run()

# if __name__ == "__main__":
#     main()
# src/app.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from model.grammar_checker import GrammarChecker
import logging
import re
from streamlit.components.v1 import html as st_html

# Configure logging
logging.basicConfig(
    filename='sinhala_scribe.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SinhalaScribeApp:
    def __init__(self):
        self.initialize_models()
        
    def initialize_models(self):
        # Initialize BERT model
        @st.cache_resource
        def load_bert():
            try:
                model_name = "Ransaka/sinhala-bert-medium-v2"
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForMaskedLM.from_pretrained(model_name)
                bert_pipeline = pipeline('fill-mask', model=model, tokenizer=tokenizer)
                logging.info("BERT model loaded successfully.")
                return bert_pipeline
            except Exception as e:
                logging.error(f"Error loading BERT model: {e}")
                st.error(f"Error loading BERT model: {e}")
                return None
            
        self.bert_model = load_bert()
        self.grammar_checker = GrammarChecker(
            "/Users/vinodlahiru/Documents/GitHub/SinhalaScribe/data/sinhala_dictionary.txt",
            self.bert_model
        )
        
    def run(self):
        st.title("SinhalaScribe Grammar and Spell Checker")
        
        # Initialize session state
        if 'current_text' not in st.session_state:
            st.session_state.current_text = ""
        if 'space_pressed' not in st.session_state:
            st.session_state.space_pressed = False
            
        # Text input with suggestions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            text = st.text_area(
                "Enter Sinhala text (Press space for suggestions):", 
                value=st.session_state.current_text,
                key="text_input",
                height=300
            )
                              
        # Update suggestions based on input
        if text != st.session_state.current_text:
            st.session_state.current_text = text
            words = text.split()
            current_word = words[-1] if words else ""
            
            # Detect space press
            st.session_state.space_pressed = text.endswith(" ")
            
            # Get suggestions
            suggestions = self.grammar_checker.get_word_suggestions(
                current_word if not st.session_state.space_pressed else text.rstrip(),
                st.session_state.space_pressed
            )
            
            # Display suggestions
            with col2:
                st.write("**Suggestions:**")
                for suggestion in suggestions:
                    if st.button(suggestion, key=f"suggest_{suggestion}"):
                        if st.session_state.space_pressed:
                            # Add new word with a space
                            st.session_state.current_text = text + suggestion + " "
                        else:
                            # Replace current word
                            if words:
                                words[-1] = suggestion
                                st.session_state.current_text = " ".join(words)
                        st.experimental_rerun()
        
        # Grammar and Spell Checking
        if text:
            results = self.grammar_checker.check_grammar(text)
            
            # Highlight misspelled words
            if results['spelling_errors']:
                misspelled_words = [word for error in results['spelling_errors'] for word in error['misspelled']]
                highlighted_text = self.highlight_misspelled(text, misspelled_words)
                st.markdown("**Highlighted Text with Misspellings:**")
                st_html(f"<p>{highlighted_text}</p>", height=100)
            
            # Display Grammar Errors
            if results['grammar_errors']:
                st.error("**Grammar Errors Found:**")
                for idx, error in enumerate(results['grammar_errors'], 1):
                    st.markdown(f"**{idx}. \"{error['sentence']}\"** - {error['description']}")
                    st.markdown(f"   **Suggestion:** {error['suggestion']}")
                    
            # Display Spelling Errors
            if results['spelling_errors']:
                st.warning("**Spelling Errors Found:**")
                for idx, spell_error in enumerate(results['spelling_errors'], 1):
                    st.markdown(f"**{idx}. \"{spell_error['sentence']}\"**")
                    for misspelled, sugg in zip(spell_error['misspelled'], spell_error['suggestions']):
                        st.markdown(f"   - **Misspelled:** {misspelled}")
                        if sugg:
                            st.markdown(f"     **Suggestions:** {', '.join(sugg)}")
                        else:
                            st.markdown("     **Suggestions:** None found")
            
            # Display Correct Sentences
            if results['correct_sentences']:
                st.success("**Correct Sentences:**")
                for sentence in results['correct_sentences']:
                    st.markdown(f"✓ {sentence}")
            
            # Optional: User Feedback Mechanism
            if results['grammar_errors'] or results['spelling_errors']:
                st.markdown("---")
                st.subheader("Was this helpful?")
                feedback = st.radio("Please select:", ("Yes", "No"), horizontal=True)
                if feedback == "No":
                    feedback_text = st.text_area("Please provide your feedback:")
                    if st.button("Submit Feedback"):
                        try:
                            with open('feedback.log', 'a', encoding='utf-8') as f:
                                f.write(f"Feedback: {feedback_text}\n")
                            st.success("Thank you for your feedback!")
                            logging.info(f"User feedback submitted: {feedback_text}")
                        except Exception as e:
                            st.error("Error saving feedback. Please try again later.")
                            logging.error(f"Error saving feedback: {e}")

    def highlight_misspelled(self, text, misspelled_words):
        """Highlight misspelled words in the text."""
        # Escape HTML special characters
        escaped_text = re.escape(text)
        for word in misspelled_words:
            # Use regex to replace whole words only
            pattern = r'\b' + re.escape(word) + r'\b'
            replacement = f'<span style="background-color: yellow">{word}</span>'
            escaped_text = re.sub(pattern, replacement, escaped_text)
        # Unescape HTML characters except for the highlighted spans
        highlighted_text = escaped_text.replace('\\<span', '<span').replace('\\</span>', '</span>')
        return highlighted_text

def main():
    app = SinhalaScribeApp()
    app.run()

if __name__ == "__main__":
    main()