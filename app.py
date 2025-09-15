#Headline Scraper

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt

# Download stopwords
nltk.download("stopwords")
stopwords = set(stopwords.words("english"))

# CNN URLs and topics
CNN_URLs = [
        {"url": "https://www.cnn.com", "topic": "General"},
        {"url": "https://www.cnn.com/us", "topic": "US"},
        {"url": "https://www.cnn.com/world", "topic": "World"},
        {"url": "https://www.cnn.com/business", "topic": "Business"},
        {"url": "https://www.cnn.com/politics", "topic": "Politics"},
        {"url": "https://www.cnn.com/health", "topic": "Health"},
        {"url": "https://www.cnn.com/entertainment", "topic": "Entertainment"},
    ]

# Print headlines
def print_headlines(headlines, url):
    print(f"{len(headlines)} headlines found on {url}")
    for index, headline in enumerate(headlines, 1):
        print(f"{index}. {headline}")

# Get headlines
def get_headlines(url):
    print(f"Scraping {url}...")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for headline in soup.find_all(["span"], class_="container__headline-text"):
        headlines.append(headline.text)

    return headlines

# Count words
def count_words(df):
    all_words = []
    for headline in df["headline"]:
        all_words.extend(clean_text(headline))
    return all_words

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    words = text.split()
    filtered_words = []
    for w in words:
        if w not in stopwords:
            filtered_words.append(w)
    return filtered_words

# Main function
def main():
    all_data = []

    for entry in CNN_URLs:
        url = entry["url"]
        topic = entry["topic"]

        headlines = get_headlines(url)
        print_headlines(headlines, url)
        print("\n")

        timestamp = datetime.now()
        for headline in headlines:
            all_data.append({
                "timestamp": timestamp,
                "headline": headline,
                "url": url,
                "topic": topic
            })

    df = pd.DataFrame(all_data)
    df.to_csv("cnn_headlines.csv", index=False)
    print(f"Data saved to cnn_headlines.csv")

    all_words = count_words(df)
    print(f"Total words: {len(all_words)}")
    print(f"Unique words: {len(set(all_words))}")
    #Counter returns a list of tuples with keys that are the words and values that are the count of the words
    word_counts = Counter(all_words)
    print(f"Most common words: {word_counts.most_common(10)}")

if __name__ == "__main__":
    main()