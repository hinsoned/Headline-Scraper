#Headline Scraper

import requests
from bs4 import BeautifulSoup

def print_headlines(headlines, url):
    print(f"{len(headlines)} headlines found on {url}")
    for index, headline in enumerate(headlines, 1):
        print(f"{index}. {headline}")

def get_headlines(url):
    print(f"Scraping {url}...")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for headline in soup.find_all(["span"], class_="container__headline-text"):
        headlines.append(headline.text)

    #print_headlines(headlines)
    return headlines

def main():
    CNN_URLs = ["https://www.cnn.com", 
    "https://www.cnn.com/us", 
    "https://www.cnn.com/world", 
    "https://www.cnn.com/business", 
    "https://www.cnn.com/politics", 
    "https://www.cnn.com/health", 
    "https://www.cnn.com/entertainment",
    ]

    for URL in CNN_URLs:
        headlines = get_headlines(URL)
        print_headlines(headlines, URL)
        print("\n")

if __name__ == "__main__":
    main()