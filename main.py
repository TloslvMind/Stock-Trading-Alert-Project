import requests
import os
from twilio.rest import Client

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = news_response.json()["Time Series (Daily)"]
data_list = [value for (_, value) in data.items()]
yesterday_day = data_list[0]
yesterday_closing_price = float(yesterday_day["4. close"])

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday["4. close"])

difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(difference / yesterday_closing_price * 100)

if abs(diff_percent) > 5:
    news_api_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_api_params)

    news_data = news_response.json()["articles"]
    three_articles = news_data[:3]

    formatted_articles = [
        f"{STOCK_NAME}{up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles]

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18563475548",
            to="+380000000000",
        )
