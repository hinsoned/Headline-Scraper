# CNN Headline Scraper & Sentiment Analyzer 📰✨

Analyze the mood of the news! This Python project scrapes headlines from CNN, uncovers the most common keywords, and visualizes sentiment trends related to the most common keywords at that time.  

---

## 🔹 Key Features

- Scrapes live headlines from CNN sections.  
- Identifies most frequent keywords.  
- Measures sentiment (polarity & subjectivity) of each headline using TextBlob.  
- Generates charts for:  
  - Word frequency  
  - Polarity & subjectivity distributions
  - Sentiment of top keywords  
- Exports results as **CSV**, **Excel**, and **PNG plots** in organized, timestamped folders.  

---

## 🔹 How It Works

1. Fetch headlines using **BeautifulSoup**.  
2. Clean text and extract keywords.  
3. Analyze sentiment with **TextBlob**.  
4. Visualize results using **Seaborn** and **Matplotlib**.  
5. Save data and plots in a neatly organized and timestamped folder.  

---

## 🔹 Example Output

**Top Keywords by Frequency**  
![word_counts_example](screenshots/word_count_example.png)  

**Sentiment of Headlines**  
![avg_polarity_example](screenshots/subjectivity_example.png)  

*(Screenshots are illustrative; actual outputs vary based on current headlines.)*  

---

