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




# app.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

from model.grammar_checker import GrammarChecker

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
                return pipeline('fill-mask', model=model, tokenizer=tokenizer)
            except Exception as e:
                st.error(f"Error loading BERT model: {e}")
                return None
            
        self.bert_model = load_bert()
        self.grammar_checker = GrammarChecker(
            "/Users/vinodlahiru/Documents/GitHub/SinhalaScribe/data/sinhala_dictionary.txt",
            self.bert_model
        )
        
    def run(self):
        st.title("SinhalaScribe Grammar Checker")
        
        # Initialize session state
        if 'current_text' not in st.session_state:
            st.session_state.current_text = ""
        if 'space_pressed' not in st.session_state:
            st.session_state.space_pressed = False
            
        # Text input with suggestions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            text = st.text_area(
                "Enter text (Press space for BERT suggestions):", 
                value=st.session_state.current_text,
                key="text_input",
                height=200
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
                st.write("Suggestions:")
                for suggestion in suggestions:
                    if st.button(suggestion, key=f"suggest_{suggestion}"):
                        if st.session_state.space_pressed:
                            # Add new word
                            st.session_state.current_text = text + suggestion + " "
                        else:
                            # Replace current word
                            words = text.split()
                            words[-1] = suggestion
                            st.session_state.current_text = " ".join(words) + " "
                        st.experimental_rerun()
        
        # Grammar checking
        if text:
            results = self.grammar_checker.check_grammar(text)
            
            if results['errors']:
                st.markdown("❌ **Grammar Errors Found:**")
                for idx, error in enumerate(results['errors'], start=1):
                    st.markdown(f"**{idx}. \"{error['sentence']}\"** - {error['description']}")
                    st.markdown(f"   *Suggestion:* `{error['suggestion']}`")
                    
            if results['correct']:
                st.success("✓ **Correct Sentences:**")
                for sentence in results['correct']:
                    st.write(f"✓ {sentence}")

def main():
    app = SinhalaScribeApp()
    app.run()

if __name__ == "__main__":
    main()