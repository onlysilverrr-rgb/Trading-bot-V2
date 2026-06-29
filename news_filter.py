import requests

NEWS_KEYWORDS = [
    "fed", "interest rate", "inflation", "cpi",
    "nfp", "non farm", "jobs report",
    "war", "attack", "crisis",
    "bitcoin etf", "crypto ban",
    "bank collapse", "recession"
]


def get_news_headlines():

    try:
        url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=20"

        response = requests.get(url, timeout=10)
        data = response.json()

        if "articles" not in data:
            return []

        return [
            a["title"].lower()
            for a in data["articles"]
            if a.get("title")
        ]

    except:
        return []


def is_high_impact_news_time():

    headlines = get_news_headlines()

    triggered = []

    for h in headlines:
        for k in NEWS_KEYWORDS:
            if k in h:
                triggered.append(h)
                break

    return len(triggered) >= 2, triggered