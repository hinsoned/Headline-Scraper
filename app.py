#Headline Scraper

import requests
from bs4 import BeautifulSoup

url = "https://www.cnn.com/us"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

headlines = []
for headline in soup.find_all(["span"], class_="container__headline-text"):
    headlines.append(headline.text)

#print(headlines)
print(f"{len(headlines)} headlines found on CNN.com")
for index, headline in enumerate(headlines, 1):
    print(f"{index}. {headline}")
    #print(headline)

#print(soup.prettify())