from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from rake_nltk import Rake
import yake

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
    keywords = extract_keywords(text, method=method)
    return jsonify({'keywords': keywords})

if __name__ == '__main__':
    app.run(debug=True)
