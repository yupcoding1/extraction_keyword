from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from rake_nltk import Rake
import yake
import re
import nltk
from collections import Counter

nltk.download('punkt')

app = Flask(__name__)

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
    else:
        return []

def ngram_keywords(text, n=1, top_n=10):
    words = [w.lower() for w in nltk.word_tokenize(text) if w.isalpha()]
    ngrams = zip(*[words[i:] for i in range(n)])
    ngram_list = [' '.join(ng) for ng in ngrams]
    counter = Counter(ngram_list)
    return [kw for kw, _ in counter.most_common(top_n)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    text = data.get('text', '').strip()
    url = data.get('url', '').strip()
    method = data.get('method', 'rake')
    if url:
        text = extract_text_from_url(url)
    if not text:
        return jsonify({'error': 'No text found.'}), 400
    stats = get_text_stats(text)
    keywords = extract_keywords(text, method=method)
    top1 = ngram_keywords(text, n=1, top_n=10)
    top2 = ngram_keywords(text, n=2, top_n=10)
    top3 = ngram_keywords(text, n=3, top_n=10)
    return jsonify({
        'keywords': keywords,
        'stats': stats,
        'top_keywords': {
            '1_word': top1,
            '2_word': top2,
            '3_word': top3
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
