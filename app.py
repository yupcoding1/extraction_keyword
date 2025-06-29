from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from rake_nltk import Rake
import yake
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string
from keybert import KeyBERT
from langdetect import detect
try:
    from textrank4zh import TextRank4Keyword
except ImportError:
    TextRank4Keyword = None

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Supported languages for stopwords
SUPPORTED_LANGS = {
    'en': 'english',
    'hi': 'hindi',
    'mr': 'marathi',
    'ar': 'arabic'
}

# Helper to extract text from URL
def extract_text_from_url(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Try to get main content
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
        return text.strip()
    except Exception as e:
        return ''

# Text statistics
def get_text_stats(text):
    words = nltk.word_tokenize(text)
    chars = len(text)
    chars_no_space = len(text.replace(' ', ''))
    sentences = nltk.sent_tokenize(text)
    paragraphs = [p for p in text.split('\n') if p.strip()]
    syllables = sum(count_syllables(word) for word in words if word.isalpha())
    return {
        'words': len(words),
        'characters': chars,
        'characters_no_space': chars_no_space,
        'syllables': syllables,
        'sentences': len(sentences),
        'paragraphs': len(paragraphs)
    }

def count_syllables(word):
    word = word.lower()
    # Simple syllable count: count groups of vowels
    return len(re.findall(r'[aeiouy]+', word)) or 1

# Keyword extraction using RAKE and YAKE
def extract_keywords(text, method='rake', max_keywords=15):
    if method == 'rake':
        rake = Rake()
        rake.extract_keywords_from_text(text)
        return rake.get_ranked_phrases()[:max_keywords]
    elif method == 'yake':
        kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=max_keywords)
        keywords = kw_extractor.extract_keywords(text)
        return [kw for kw, score in keywords]
    elif method == 'keybert':
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', top_n=max_keywords)
        return [kw for kw, score in keywords]
    elif method == 'textrank' and TextRank4Keyword is not None:
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=text, lower=True, window=2)
        return [kw.word for kw in tr4w.get_keywords(num=max_keywords, word_min_len=1)]
    else:
        return []

def ngram_keywords(text, n=1, top_n=10, lang='en'):
    lang_code = SUPPORTED_LANGS.get(lang, 'english')
    try:
        stop_words = set(stopwords.words(lang_code))
    except:
        stop_words = set(stopwords.words('english'))
    words = [w.lower() for w in nltk.word_tokenize(text)
             if w.isalpha() and w.lower() not in stop_words]
    ngrams = zip(*[words[i:] for i in range(n)])
    ngram_list = [' '.join(ng) for ng in ngrams]
    counter = Counter(ngram_list)
    return [kw for kw, _ in counter.most_common(top_n) if not any(w in stop_words for w in kw.split())]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    text = data.get('text', '').strip()
    url = data.get('url', '').strip()
    method = data.get('method', 'rake')
    lang = data.get('lang')
    if url:
        text = extract_text_from_url(url)
    if not text:
        return jsonify({'error': 'No text found.'}), 400
    # Auto-detect language if not provided
    if not lang or lang == 'auto':
        try:
            detected = detect(text)
            lang = detected if detected in SUPPORTED_LANGS else 'en'
        except:
            lang = 'en'
    stats = get_text_stats(text)
    keywords = extract_keywords(text, method=method)
    top1 = ngram_keywords(text, n=1, top_n=10, lang=lang)
    top2 = ngram_keywords(text, n=2, top_n=10, lang=lang)
    top3 = ngram_keywords(text, n=3, top_n=10, lang=lang)
    return jsonify({
        'keywords': keywords,
        'stats': stats,
        'top_keywords': {
            '1_word': top1,
            '2_word': top2,
            '3_word': top3
        },
        'detected_lang': lang
    })

if __name__ == '__main__':
    app.run(debug=True)
