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
import seaborn as sns
from textblob import TextBlob
import os
import platform
import subprocess

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

# Create counter
def create_counter(all_words):
    print(f"Total words: {len(all_words)}")
    print(f"Unique words: {len(set(all_words))}")
    #Counter returns a list of tuples with keys that are the words and values that are the count of the words
    word_counts = Counter(all_words)
    print(f"Most common words: {word_counts.most_common(15)}")

    return word_counts

# Create plot
def plot_word_counts(word_counts, timestamp):
    words = []
    counts = []

    for word, count in word_counts.most_common(15):
        words.append(word)
        counts.append(count)

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 8))#This makes the canvas for the plot
    sns.barplot(x=list(words), y=list(counts), palette="Blues_d")#seaborn finds the active plt.figure() and plots the barplot on it
    plt.title(f"Top 15 Most Common Words in CNN Headlines {timestamp}")
    plt.ylabel("Frequency")
    plt.xlabel("Words")
    plt.savefig("word_counts.png")#This saves the plot to a file
    open_image("word_counts.png")
    plt.close()

# Sentiment analysis
def analyze_sentiment(df):
    polarities = []
    subjectivities = []
    for headline in df["headline"]:
        blob = TextBlob(headline)
        polarities.append(blob.sentiment.polarity)
        subjectivities.append(blob.sentiment.subjectivity)
    df["polarity"] = polarities
    df["subjectivity"] = subjectivities
    return df

# Create plot for sentiment
def plot_sentiment(df, timestamp):
    #Polarity Histogram
    plt.figure(figsize=(12, 8))
    sns.histplot(df["polarity"], bins=20, kde=True)
    plt.title(f"Polarity of CNN Headlines {timestamp}")
    plt.xlabel("Polarity")
    plt.ylabel("Frequency")
    plt.savefig("sentiment.png")
    open_image("sentiment.png")
    plt.close()

    #Subjectivity Histogram
    plt.figure(figsize=(12, 8))
    sns.histplot(df["subjectivity"], bins=20, kde=True)
    plt.title(f"Subjectivity of CNN Headlines {timestamp}")
    plt.xlabel("Subjectivity")
    plt.ylabel("Frequency")
    plt.savefig("subjectivity.png")
    open_image("subjectivity.png")
    plt.close()

# Open image
def open_image(path):
    system = platform.system()#This gets the operating system
    if system == "Darwin":  # macOS
        subprocess.call(["open", path])#This opens the image on macOS
    elif system == "Windows":
        os.startfile(path)#This opens the image on Windows
    else:  # Linux
        subprocess.call(["xdg-open", path])#This opens the image on Linux
    

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

    # Create dataframe
    df = pd.DataFrame(all_data)

    # Sentiment analysis
    df = analyze_sentiment(df)
    # Create plot for sentiment
    plot_sentiment(df, timestamp)

    # Save dataframe to csv
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f"cnn_headlines_{timestamp}.csv", index=False)
    print(f"Data saved to cnn_headlines_{timestamp}.csv")

    # Count words
    all_words = count_words(df)
    # Create counter
    word_counts = create_counter(all_words)
    # Create plot for word counts
    plot_word_counts(word_counts, timestamp)


if __name__ == "__main__":
    main()