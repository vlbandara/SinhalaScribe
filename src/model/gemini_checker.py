# gemini_checker.py
class GeminiChecker:
    def __init__(self, model):
        self.model = model

    def check_grammar(self, text: str) -> str:
        """Check grammar using Gemini AI"""
        prompt = f"""
        Please analyze the following Sinhala text for grammar and spelling errors:
        Text: {text}
        
        Please provide:
        1. Any grammar errors found
        2. Any spelling errors found
        3. Suggestions for improvement
        4. Corrected version
        
        Please respond in both Sinhala and English.
        Format the response clearly with proper headings and bullet points.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error getting AI suggestions: {str(e)}"