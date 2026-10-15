"""NewsAPI helper with timeouts and graceful failures."""
import os
import requests
URL = "https://newsapi.org/v2/everything"
DEFAULT_DOMAINS = "spiegel.de,tagesschau.de,zeit.de,welt.de,faz.net,sueddeutsche.de,focus.de"

def get_current_news(pageSize=5, sortBy="publishedAt", language="de", domains=DEFAULT_DOMAINS):
    key = os.getenv("NEWS_API_KEY")
    if not key:
        print("News unavailable: NEWS_API_KEY is not set.")
        return []
    if sortBy not in {"relevancy", "popularity", "publishedAt"}:
        sortBy = "publishedAt"
    try:
        response = requests.get(URL, params={"domains": domains or DEFAULT_DOMAINS, "language": language, "sortBy": sortBy, "pageSize": max(1, min(int(pageSize), 100)), "apiKey": key}, timeout=12)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            print("News API error:", data.get("message", "Unknown error"))
            return []
        return [a for a in data.get("articles", []) if a.get("title") and a.get("url")]
    except (requests.RequestException, ValueError) as exc:
        print(f"Could not retrieve news: {exc}")
        return []
