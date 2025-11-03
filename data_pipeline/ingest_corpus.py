# backend/ingest_corpus.py
"""
Fetches and cleans Hawai‘i Career Pathways HTML pages.
Produces plain text files for RAG embeddings.
"""

import re, requests
from pathlib import Path
from bs4 import BeautifulSoup

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

URLS = [
    "https://hawaiicareerpathways.org/pathways/programs/IT/artificialintelligence.html",
    "https://hawaiicareerpathways.org/pathways/programs/hospitality_tourism/shtm.html",
]

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def fetch_and_parse(url):
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h1") or soup.find("title")
    title_text = title.get_text(strip=True) if title else "Untitled"
    body_text = " ".join([p.get_text(' ', strip=True) for p in soup.find_all("p")])
    return title_text, clean_text(body_text)

def save_doc(title, url, body):
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", title)[:60]
    out = PROCESSED_DIR / f"{safe}.txt"
    out.write_text(f"TITLE: {title}\nSOURCE: {url}\n\n{body}", encoding="utf-8")
    print(f"Saved {out.name}")

if __name__ == "__main__":
    for url in URLS:
        t, b = fetch_and_parse(url)
        save_doc(t, url, b)
