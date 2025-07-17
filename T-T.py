import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import jieba

def fetch_article(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all('p')
    text = '\n'.join([p.text.strip() for p in paragraphs if len(p.text.strip()) > 20])
    return text

def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("chinese"))
    summarizer = TextRankSummarizer()
    summarizer.stop_words = set()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

if __name__ == "__main__":
    url = input("請輸入新聞網址：")
    article = fetch_article(url)
    print("\n【原文前300字】\n", article[:300])
    summary = summarize_text(article)
    print("\n【自動大綱】")
    for s in summary:
        print("🔹", s)