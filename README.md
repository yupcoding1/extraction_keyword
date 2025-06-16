# Python Keyword Extractor Web App

This project is a web application for extracting keywords and analyzing text statistics from either pasted text or the content of a provided URL. It is inspired by [wordcount.com/keyword-extractor](https://wordcount.com/keyword-extractor) and uses popular NLP libraries for keyword extraction and text analysis.

## Features
- **Paste Text or Enter URL:** Extract keywords and analyze statistics from user-pasted text or from the main content of a web page (URL).
- **Extraction Methods:** Choose between RAKE, YAKE, KeyBERT, and TextRank keyword extraction algorithms.
- **Text Statistics:** Instantly get:
  - Number of words
  - Number of characters
  - Number of characters (excluding spaces)
  - Number of syllables
  - Number of sentences
  - Number of paragraphs
- **Top Keywords:**
  - 1-word, 2-word, and 3-word keywords (n-grams), filtered to exclude common stopwords (prepositions, pronouns, etc.)
- **Multilanguage Support:**
  - Stopword filtering and n-gram keyword extraction for English, Hindi, Marathi, and Arabic.
  - **Auto Language Detection:** The app can automatically detect the language of the input text and use the appropriate stopword list for filtering.
- **Modern UI:** Clean, responsive, and user-friendly interface.

## How It Works
1. **Paste text** or **enter a URL** in the web form.
2. Select the extraction method (RAKE, YAKE, KeyBERT, or TextRank).
3. Select the language (or choose "Auto Detect").
4. Click **Extract Keywords**.
5. The app will display:
   - Detected language (if auto-detect is used)
   - Text statistics (words, characters, syllables, etc.)
   - Top 1-word, 2-word, and 3-word keywords (excluding stopwords)
   - Extracted keywords using the selected method

## Installation & Setup

### 1. Clone the Repository
```
git clone <your-repo-url>
cd keyword_extractor
```

### 2. Create a Virtual Environment
```
python -m venv .venv
```

### 3. Activate the Virtual Environment
- **Windows (PowerShell):**
  ```
  .venv\Scripts\Activate
  ```
- **macOS/Linux:**
  ```
  source .venv/bin/activate
  ```

### 4. Install Dependencies
```
pip install -r requirements.txt
```

### 5. Run the Application
```
python app.py
```

The app will be available at [http://localhost:5000](http://localhost:5000).

## Usage
- Paste any text or provide a news/article URL.
- Select the extraction method (RAKE, YAKE, KeyBERT, or TextRank).
- Select the language (or "Auto Detect").
- Click **Extract Keywords**.
- View:
  - Detected language (if auto-detect is used)
  - Text statistics (top section)
  - Top 1-word, 2-word, and 3-word keywords (middle section)
  - Extracted keywords (bottom section)

## Project Structure
```
keyword_extractor/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend HTML (UI)
└── README.md             # This file
```

## Dependencies
- Flask
- requests
- beautifulsoup4
- rake-nltk
- yake
- nltk
- keybert
- sentence-transformers
- textrank4zh
- langdetect

## Notes
- The app uses NLTK for tokenization, stopword filtering, and text statistics. The first run will download required NLTK data.
- For URLs, the app attempts to extract the main content by collecting all `<p>` tags.
- Top n-gram keywords are filtered to exclude common stopwords in the selected or detected language.
- Auto language detection is powered by `langdetect` and supports English, Hindi, Marathi, and Arabic for stopword filtering.
- For TextRank, ensure `networkx==2.8` is installed for compatibility with `textrank4zh`.

## License
This project is for demonstration and educational purposes only.

---

For any issues or suggestions, please open an issue or submit a pull request.
