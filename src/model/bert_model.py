from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

class BertModelWrapper:
    def __init__(self):
        self.model_name = "Ransaka/sinhala-bert-medium-v2"
        self.tokenizer = None
        self.model = None
        self.fill_mask = None
        self.initialize_model()

    def initialize_model(self):
        """Initialize the BERT model and tokenizer"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(self.model_name)
        self.fill_mask = pipeline('fill-mask', model=self.model, tokenizer=self.tokenizer)

    def get_mask_predictions(self, text):
        """Get predictions for masked text"""
        try:
            predictions = self.fill_mask(text)
            return predictions
        except Exception as e:
            print(f"Error in mask prediction: {e}")
            return []