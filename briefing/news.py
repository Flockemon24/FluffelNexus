import requests
import os

def get_current_news(pageSize=5, sortBy="popularity", language="de", domains="spiegel.de,tagesschau.de,zeit.de,welt.de,faz.net,sueddeutsche.de,focus.de"):
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    if not NEWS_API_KEY:
        print("Error: No API-Key found.")
        return []

    # Wir nutzen den /everything-Endpunkt und suchen nach aktuellen Top-Themen
    url = "https://newsapi.org/v2/everything"
    
    params = {
        # q ist bei /everything zwingend erforderlich. 
        # Durch den Platzhalter '*' suchen wir nach ALLEN Artikeln der Top-Quellen.
        'q': '*', 

        # Hier definierst du, welche großen deutschen Medien abgefragt werden:
        'domains': domains,

        'language': language,
        'sortBy': sortBy, # Oder 'publishedAt' für die neuesten Artikel
        'pageSize': pageSize,
        'apiKey': NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        for idx, art in enumerate(articles, 1):
            print(f"[{idx}] {art['title']} ({art['source']['name']})")
        return articles
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
