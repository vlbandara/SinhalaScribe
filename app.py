# app.py
import streamlit as st
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
import logging
import re
from streamlit.components.v1 import html as st_html
import os
from dotenv import load_dotenv

# Import our model classes
from src.model.grammar_checker import GrammarChecker
from src.model.gemini_checker import GeminiChecker
from src.model.rule_based_checker import RuleBasedChecker

# Set page configuration
st.set_page_config(
    page_title="SinhalaScribe",
    page_icon="🖋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='logs/sinhala_scribe.log',
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
                model = genai.GenerativeModel('gemini-pro')
                logging.info("Gemini model loaded successfully.")
                return model
            except Exception as e:
                logging.error(f"Error loading Gemini model: {e}")
                st.error(f"Error loading Gemini model: {e}")
                return None

        self.bert_model = load_bert()
        self.gemini_model = load_gemini()
        
        # Initialize all checkers
        self.bert_checker = GrammarChecker(
            "data/sinhala_dictionary.txt",
            self.bert_model
        )
        self.gemini_checker = GeminiChecker(self.gemini_model)
        self.rule_checker = RuleBasedChecker("data/sinhala_dictionary.txt")
        
    def run(self):
        st.title("SinhalaScribe")
        
        # Add sidebar with information
        
        with st.sidebar:
            st.header("About")
            st.write("""
            SinhalaScribe is a comprehensive grammar and spell checker for Sinhala text. 
            It offers three different approaches:
            
            1. **BERT-based Model**: Uses deep learning for context-aware checking
            2. **Gemini AI Model**: Leverages Google's Gemini for advanced analysis
            3. **Rule-based Model**: Uses traditional grammar rules and dictionary
            """)
            
            st.header("How to Use")
            st.write("""
            1. Select your preferred checking model
            2. Enter or paste your Sinhala text
            3. View the analysis results
            4. Provide feedback to help improve the system
            """)
        
        # Model selection dropdown with enhanced UI
        model_choice = st.selectbox(
            "Select Grammar Checking Model:",
            ["BERT-based Model", "Gemini AI Model", "Rule-based Model"],
            help="Choose between BERT-based local model, Gemini AI, or rule-based approach for grammar checking"
        )
        
        # Model description based on selection
        model_descriptions = {
            "BERT-based Model": "Uses contextual understanding for accurate grammar checking",
            "Gemini AI Model": "Provides comprehensive language analysis with AI",
            "Rule-based Model": "Fast, deterministic checking based on Sinhala grammar rules"
        }
        st.info(model_descriptions[model_choice])
        
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
                height=300,
                help="Type or paste your Sinhala text here for analysis"
            )
        
        # Clear button
        if st.button("Clear Text"):
            st.session_state.current_text = ""
            st.experimental_rerun()
        
        if text:
            with st.spinner('Analyzing text...'):
                if model_choice == "BERT-based Model":
                    self.process_bert_results(text)
                elif model_choice == "Gemini AI Model":
                    self.process_gemini_results(text)
                else:  # Rule-based Model
                    self.process_rule_based_results(text)
                    
            # User Feedback Section
            st.markdown("---")
            st.subheader("Was this analysis helpful?")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("👍 Yes"):
                    self.save_feedback("Positive feedback received")
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 No"):
                    feedback_text = st.text_area(
                        "Please tell us how we can improve:",
                        key="feedback_text"
                    )
                    if st.button("Submit Feedback"):
                        self.save_feedback(feedback_text)
                        st.success("Thank you for your feedback!")

    def process_bert_results(self, text):
        """Process and display results from BERT-based checker."""
        try:
            results = self.bert_checker.check_grammar(text)
            
            # Highlight misspelled words
            if results['spelling_errors']:
                misspelled_words = [word for error in results['spelling_errors'] for word in error['misspelled']]
                highlighted_text = self.highlight_misspelled(text, misspelled_words)
                st.markdown("**Text with Highlighted Errors:**")
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
                    
        except Exception as e:
            st.error(f"Error processing text with BERT model: {str(e)}")
            logging.error(f"BERT processing error: {str(e)}")

    def process_gemini_results(self, text):
        """Process and display results from Gemini checker."""
        try:
            results = self.gemini_checker.check_grammar(text)
            st.markdown("**Gemini AI Analysis:**")
            st.markdown(results)
        except Exception as e:
            st.error(f"Error processing text with Gemini model: {str(e)}")
            logging.error(f"Gemini processing error: {str(e)}")

    def process_rule_based_results(self, text):
        """Process and display results from rule-based checker."""
        try:
            results = self.rule_checker.check_grammar(text)
            
            # Display Grammar Errors
            if results['grammar_errors']:
                st.error("**Grammar Errors Found:**")
                for sentence_data in results['grammar_errors']:
                    st.markdown(f"**In sentence:** {sentence_data['sentence']}")
                    for error in sentence_data['errors']:
                        st.markdown(f"- {error['description']}")
                        st.markdown(f"  **Suggestion:** {error['suggestion']}")
            
            # Display Spelling Errors
            if results['spelling_errors']:
                st.warning("**Spelling Errors Found:**")
                for sentence_data in results['spelling_errors']:
                    st.markdown(f"**In sentence:** {sentence_data['sentence']}")
                    for error in sentence_data['errors']:
                        suggestions = ', '.join(error['suggestions']) if error['suggestions'] else 'No suggestions available'
                        st.markdown(f"- Misspelled word: **{error['word']}**")
                        st.markdown(f"  **Suggestions:** {suggestions}")
            
            # Display Correct Sentences
            if results['correct_sentences']:
                st.success("**Correct Sentences:**")
                for sentence in results['correct_sentences']:
                    st.markdown(f"✓ {sentence}")
                    
        except Exception as e:
            st.error(f"Error processing text with rule-based checker: {str(e)}")
            logging.error(f"Rule-based processing error: {str(e)}")

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
        """Save user feedback to log file."""
        try:
            with open('logs/feedback.log', 'a', encoding='utf-8') as f:
                f.write(f"{feedback_text}\n")
            logging.info(f"User feedback saved: {feedback_text}")
        except Exception as e:
            st.error("Error saving feedback. Please try again later.")
            logging.error(f"Error saving feedback: {e}")

def main():
    try:
        app = MultiModelSinhalaApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logging.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()