# Python Keyword Extractor Web App

This project is a web application for extracting keywords and analyzing text statistics from either pasted text or the content of a provided URL. It is inspired by [wordcount.com/keyword-extractor](https://wordcount.com/keyword-extractor) and uses popular NLP libraries for keyword extraction and text analysis.

## Features
- **Paste Text or Enter URL:** Extract keywords and analyze statistics from user-pasted text or from the main content of a web page (URL).
- **Extraction Methods:** Choose between RAKE and YAKE keyword extraction algorithms.
- **Text Statistics:** Instantly get:
  - Number of words
  - Number of characters
  - Number of characters (excluding spaces)
  - Number of syllables
  - Number of sentences
  - Number of paragraphs
- **Top Keywords:**
  - 1-word, 2-word, and 3-word keywords (n-grams), filtered to exclude common stopwords (prepositions, pronouns, etc.)
- **Modern UI:** Clean, responsive, and user-friendly interface.

## How It Works
1. **Paste text** or **enter a URL** in the web form.
2. Select the extraction method (RAKE or YAKE).
3. Click **Extract Keywords**.
4. The app will display:
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

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage
- Paste any text or provide a news/article URL.
- Select the extraction method (RAKE or YAKE).
- Click **Extract Keywords**.
- View:
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

## Notes
- The app uses NLTK for tokenization, stopword filtering, and text statistics. The first run will download required NLTK data.
- For URLs, the app attempts to extract the main content by collecting all `<p>` tags.
- Top n-gram keywords are filtered to exclude common English stopwords.

## License
This project is for demonstration and educational purposes only.

---

For any issues or suggestions, please open an issue or submit a pull request.
