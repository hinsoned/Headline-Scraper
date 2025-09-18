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
def plot_word_counts(word_counts, timestamp, folder_name):
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
    plt.savefig(os.path.join(folder_name, f"word_counts{timestamp}.png"))#This saves the plot to a file in the report folder
    open_image(os.path.join(folder_name, f"word_counts{timestamp}.png"))
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
def plot_sentiment(df, timestamp, folder_name):
    #Polarity Histogram
    plt.figure(figsize=(12, 8))
    sns.histplot(df["polarity"], bins=20, kde=True)
    plt.title(f"Polarity of CNN Headlines {timestamp}")
    plt.xlabel("Polarity")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(folder_name, f"sentiment{timestamp}.png"))
    open_image(os.path.join(folder_name, f"sentiment{timestamp}.png"))
    plt.close()

    print(f"Saved sentiment{timestamp}.png")

    #Subjectivity Histogram
    plt.figure(figsize=(12, 8))
    sns.histplot(df["subjectivity"], bins=20, kde=True)
    plt.title(f"Subjectivity of CNN Headlines {timestamp}")
    plt.xlabel("Subjectivity")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(folder_name, f"subjectivity{timestamp}.png"))
    open_image(os.path.join(folder_name, f"subjectivity{timestamp}.png"))
    plt.close()

    print(f"Saved subjectivity{timestamp}.png")

# Most subjective and polar headlines
def most_subjective_headlines(df):
    subjective_df = df.sort_values(by="subjectivity", ascending=False)
    print(f"Most subjective headlines: \n")
    for index, row in subjective_df.head(10).iterrows():
        print(f"{index}. {row['headline']} | Subjectivity: {row['subjectivity']} | Topic: {row['topic']}")
    print("\n")

    print(f"Least subjective headlines: \n")
    for index, row in subjective_df.tail(10).iterrows():
        print(f"{index}. {row['headline']} | Subjectivity: {row['subjectivity']} | Topic: {row['topic']}")
    print("\n")

    print(f"Average subjectivity: {subjective_df['subjectivity'].mean()}")
    print("\n")

    return subjective_df

def most_polar_headlines(df):
    polar_df = df.sort_values(by="polarity", ascending=False)
    print(f"Most polar headlines: \n")
    for index, row in polar_df.head(10).iterrows():
        print(f"{index}. {row['headline']} | Polarity: {row['polarity']} | Topic: {row['topic']}")  
    print("\n")

    print(f"Least polar headlines: \n")
    for index, row in polar_df.tail(10).iterrows():
        print(f"{index}. {row['headline']} | Polarity: {row['polarity']} | Topic: {row['topic']}")
    print("\n")

    print(f"Average polarity: {polar_df['polarity'].mean()}")
    print("\n")

    return polar_df

# Get top keywords
def get_top_keywords(word_counts):
    top_keyword_tuples = word_counts.most_common(10)# This returns a list of tuples with the word and the count
    top_keywords = []
    for tuple in top_keyword_tuples:
        word = tuple[0]
        top_keywords.append(word)
    return top_keywords

# Average sentiment for top keywords
def avg_sentiment_for_top_keywords(df, word_counts):

    top_keywords = get_top_keywords(word_counts)

    avg_data = []
    for word in top_keywords:
        relevant_rows = df[df["keywords"].apply(lambda kws: word in kws)]
        avg_polarity = relevant_rows['polarity'].mean()
        avg_subjectivity = relevant_rows['subjectivity'].mean()
        avg_data.append({
            "word": word,
            "avg_polarity": avg_polarity,
            "avg_subjectivity": avg_subjectivity
        })
        print(f"Average sentiment for {word}: {avg_polarity}")
        print(f"Average subjectivity for {word}: {avg_subjectivity}")
        print("\n")
        
    avg_df = pd.DataFrame(avg_data)
    return avg_df

# Add keywords to dataframe
def add_keywords(df):
    df["keywords"] = df["headline"].apply(clean_text)
    return df

# Create plot for average sentiment
def plot_avg_sentiment(avg_df, timestamp, folder_name):
    plt.figure(figsize=(12, 8))
    sns.barplot(x="word", y="avg_polarity", data=avg_df)
    plt.title(f"Average Polarity of Top Keywords {timestamp}")
    plt.xlabel("Word")
    plt.ylabel("Average Polarity")
    plt.savefig(os.path.join(folder_name, f"avg_polarity{timestamp}.png"))
    open_image(os.path.join(folder_name, f"avg_polarity{timestamp}.png"))
    plt.close()

    print(f"Saved avg_polarity{timestamp}.png")

    plt.figure(figsize=(12, 8))
    sns.barplot(x="word", y="avg_subjectivity", data=avg_df)
    plt.title(f"Average Subjectivity of Top Keywords {timestamp}")
    plt.xlabel("Word")
    plt.ylabel("Average Subjectivity")
    plt.savefig(os.path.join(folder_name, f"avg_subjectivity{timestamp}.png"))
    open_image(os.path.join(folder_name, f"avg_subjectivity{timestamp}.png"))
    plt.close()

    print(f"Saved avg_subjectivity{timestamp}.png")

# Open image    
def open_image(path):
    system = platform.system()#This gets the operating system
    if system == "Darwin":  # macOS
        subprocess.call(["open", path])#This opens the image on macOS
    elif system == "Windows":
        os.startfile(path)#This opens the image on Windows
    else:  # Linux
        subprocess.call(["xdg-open", path])#This opens the image on Linux

def save_to_excel(df, timestamp, folder_name):
    filename = f"cnn_report_{timestamp}.xlsx"
    path = os.path.join(folder_name, filename)
    
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Headlines", index=False)
        # Add top words
        #all_words = [word for kws in df["keywords"] for word in kws]
        #word_counts = Counter(all_words).most_common(20)
        #pd.DataFrame(word_counts, columns=["Word", "Count"]).to_excel(writer, sheet_name="Top Words", index=False)
    print(f"Saved Excel: {path}")

def save_to_csv(df, timestamp, folder_name):
    csv_filename = f"cnn_headlines_{timestamp}.csv"
    csv_path = os.path.join(folder_name, csv_filename)
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
# The pipeline
def main():
    all_data = []
    # Loop through the CNN URLs and get the headlines
    for entry in CNN_URLs:
        url = entry["url"]
        topic = entry["topic"]

        headlines = get_headlines(url)#This returns a list of headlines
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
    df = analyze_sentiment(df) #This adds the polarity and subjectivity columns to the dataframe

    # Add keywords to dataframe
    df = add_keywords(df)# This adds the keywords column to the dataframe

    # Create folder name for the report
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"cnn_reports_{timestamp}"

    # Create folder for the report
    os.makedirs(folder_name, exist_ok=True)

    # Create a list of all the words in the headlines after cleaning
    all_words = count_words(df)
    # Create counter to count the frequency of each word
    word_counts = create_counter(all_words)

    # Create plot for word counts to visualize the most common words
    plot_word_counts(word_counts, timestamp, folder_name)

    # Create plot for sentiment
    plot_sentiment(df, timestamp, folder_name) 

    #Most subjective and polar headlines
    subjective_df = most_subjective_headlines(df)
    polar_df = most_polar_headlines(df)

    # Get average sentiment for top keywords
    avg_df = avg_sentiment_for_top_keywords(df, word_counts)
    plot_avg_sentiment(avg_df, timestamp, folder_name)

    # Save dataframe to excel
    save_to_excel(df, timestamp, folder_name)

    # Save dataframe to csv
    save_to_csv(df, timestamp, folder_name)

if __name__ == "__main__":
    main()