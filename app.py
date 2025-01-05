# app.py
import streamlit as st
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
import logging
import re
from streamlit.components.v1 import html as st_html
from src.model.grammar_checker import GrammarChecker
from src.model.gemini_checker import GeminiChecker
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='sinhala_scribe.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MultiModelSinhalaApp:
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

        # Initialize Gemini
        @st.cache_resource
        def load_gemini():
            try:
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                #genai.configure(api_key="AIzaSyD5-Te5Ai22sHHsbBg_IUtJ_Nj4kWUbL9s")
                model = genai.GenerativeModel('gemini-pro')
                logging.info("Gemini model loaded successfully.")
                return model
            except Exception as e:
                logging.error(f"Error loading Gemini model: {e}")
                st.error(f"Error loading Gemini model: {e}")
                return None

        self.bert_model = load_bert()
        self.gemini_model = load_gemini()
        
        # Initialize checkers
        self.bert_checker = GrammarChecker(
            "data/sinhala_dictionary.txt",
            self.bert_model
        )
        self.gemini_checker = GeminiChecker(self.gemini_model)
        
    def run(self):
        st.title("SinhalaScribe Grammar and Spell Checker")
        
        # Model selection dropdown
        model_choice = st.selectbox(
            "Select Grammar Checking Model:",
            ["BERT-based Model", "Gemini AI Model"],
            help="Choose between BERT-based local model or Gemini AI for grammar checking"
        )
        
        # Initialize session state
        if 'current_text' not in st.session_state:
            st.session_state.current_text = ""
        if 'space_pressed' not in st.session_state:
            st.session_state.space_pressed = False
            
        # Text input with suggestions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            text = st.text_area(
                "Enter Sinhala text:", 
                value=st.session_state.current_text,
                key="text_input",
                height=300
            )
        
        if text:
            with st.spinner('Analyzing text...'):
                if model_choice == "BERT-based Model":
                    self.process_bert_results(text)
                else:
                    self.process_gemini_results(text)
                    
            # Optional: User Feedback Mechanism
            st.markdown("---")
            st.subheader("Was this helpful?")
            feedback = st.radio("Please select:", ("Yes", "No"), horizontal=True)
            if feedback == "No":
                feedback_text = st.text_area("Please provide your feedback:")
                if st.button("Submit Feedback"):
                    self.save_feedback(feedback_text)

    def process_bert_results(self, text):
        results = self.bert_checker.check_grammar(text)
        
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

    def process_gemini_results(self, text):
        results = self.gemini_checker.check_grammar(text)
        st.markdown("**Gemini AI Analysis:**")
        st.markdown(results)

    def highlight_misspelled(self, text, misspelled_words):
        """Highlight misspelled words in the text."""
        escaped_text = re.escape(text)
        for word in misspelled_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            replacement = f'<span style="background-color: yellow">{word}</span>'
            escaped_text = re.sub(pattern, replacement, escaped_text)
        highlighted_text = escaped_text.replace('\\<span', '<span').replace('\\</span>', '</span>')
        return highlighted_text

    def save_feedback(self, feedback_text):
        try:
            with open('feedback.log', 'a', encoding='utf-8') as f:
                f.write(f"Feedback: {feedback_text}\n")
            st.success("Thank you for your feedback!")
            logging.info(f"User feedback submitted: {feedback_text}")
        except Exception as e:
            st.error("Error saving feedback. Please try again later.")
            logging.error(f"Error saving feedback: {e}")

def main():
    app = MultiModelSinhalaApp()
    app.run()

if __name__ == "__main__":
    main()