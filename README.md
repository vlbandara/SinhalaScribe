# SinhalaScribe

A real-time grammar and spell checking application for Sinhala language, powered by BERT to word suggestions and custom text processing algorithms.
![Screenshot 2024-12-22 at 22 54 11](https://github.com/user-attachments/assets/1fb0032e-0170-4943-96d1-64ccf6fd1e6f)

## Features

### Grammar Checking
- First Person Singular ("මම" - mama) verification
  - Ensures verbs end with "මි" (mi) in present tense
  - Example: මම යමි (mama yami) – "I go"
- First Person Plural ("අපි" - api) verification
  - Ensures verbs end with "මු" (mu) in present tense
  - Example: අපි යමු (api yamu) – "We go"

### Spell Checking
- Real-time spell checking using comprehensive Sinhala dictionary
- Advanced suggestion algorithm using:
  - Character-level similarity matching
  - Position-based character frequency analysis
  - Length-aware suggestion generation
  - Weighted scoring system

### BERT Integration to suggest next word
- Uses Sinhala BERT model for context-aware suggestions
- Provides confidence scores for suggestions
- Model: Ransaka/sinhala-bert-medium-v2

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sinhala-grammar-checker.git
cd sinhala-grammar-checker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the BERT model (will be downloaded automatically on first run):
```python
from transformers import AutoTokenizer, AutoModelForMaskedLM
tokenizer = AutoTokenizer.from_pretrained("Ransaka/sinhala-bert-medium-v2")
model = AutoModelForMaskedLM.from_pretrained("Ransaka/sinhala-bert-medium-v2")
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter Sinhala text in the input area

4. View real-time suggestions and corrections

## Project Structure
```
project_root/
├── README.md
├── requirements.txt
├── data/
│   └── sinhala_dictionary.txt
├── src/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── bert_model.py
│   │   └── grammar_checker.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── text_processor.py
│   └── app.py
└── tests/
    ├── __init__.py
    └── test_grammar_checker.py
```

## Dependencies

- Python 3.8+
- transformers==4.36.2
- torch==2.1.2
- streamlit==1.29.0
- pandas==2.1.4
- numpy==1.26.2

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add some amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## Future Improvements

- [ ] Add support for compound words
- [ ] Implement context-aware suggestions
- [ ] Add phonetic similarity matching
- [ ] Create custom edit distance algorithm for Sinhala
- [ ] Add support for common typing mistakes
- [ ] Implement n-gram analysis

## Acknowledgments

- BERT model: [Ransaka/sinhala-bert-medium-v2](https://huggingface.co/Ransaka/sinhala-bert-medium-v2)
