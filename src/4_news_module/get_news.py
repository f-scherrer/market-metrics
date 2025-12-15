##################################################
# Module D - News Fetcher (Finnhub)
# Author: Yanick Meier
# Python version: 3.13.2
#
# Description:
# Fetches company news from Finnhub for a ticker and a date range.
# Returns a list of dictionaries with:
# title, publisher, summary, link, published
#
# Requirements:
# - pip install requests
# - FINNHUB_API_KEY must be set as environment variable
##################################################

import os
import requests
from datetime import datetime


def fetch_news(ticker, start_date, end_date, max_items=50):

    print("Starting Finnhub news fetch process")

    # Check date format
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error - invalid date format, please use YYYY-MM-DD")
        return []

    # Read API key from environment
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        print("Error - FINNHUB_API_KEY not set")
        return []

    # Build request
    url = "https://finnhub.io/api/v1/company-news"
    params = {
        "symbol": ticker,
        "from": start_date,
        "to": end_date,
        "token": api_key
    }

    # Call API
    try:
        response = requests.get(url, params=params, timeout=10)
    except Exception as e:
        print("Error - request failed:", e)
        return []

    # Check status code
    if response.status_code != 200:
        print("Error - API returned status:", response.status_code)
        return []

    # Parse JSON
    raw_news = response.json() or []
    print("Found", len(raw_news), "raw news items")

    articles = []

    # Convert and keep only max_items
    for item in raw_news[:max_items]:

        # Finnhub returns datetime as Unix timestamp in seconds
        ts = item.get("datetime")
        if ts:
            published_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        else:
            published_str = "Unknown date"

        article = {
            "title": item.get("headline") or "No title available",
            "publisher": item.get("source") or "Unknown publisher",
            "summary": item.get("summary") or "No summary available",
            "link": item.get("url") or "No link available",
            "published": published_str
        }

        articles.append(article)

    print("Finnhub finished, returning", len(articles), "items")
    return articles


##################################################
# Simple test block
##################################################

if __name__ == "__main__":

    print("Running simple test for Module D with Finnhub")

    test_ticker = "AAPL"
    test_start = "2023-01-01"
    test_end = "2025-01-01"

    result = fetch_news(test_ticker, test_start, test_end, max_items=5)

    print("\nTest results:")
    for a in result:
        print(a["published"], "|", a["publisher"], "|", a["title"])
