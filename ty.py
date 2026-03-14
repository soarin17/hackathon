import requests
import json as js
import openai as oai
import yfinance as yf

api_key_AI = "sk-ZZh65j-L040DIfJR0l1Owg"
api_key_news = "7013901d945a4d71961a35b20cc62c38"
BASE_URL = "https://hackathonlite-production.up.railway.app"
MODEL    = "gemini-3-flash-preview"

#NEWS DATA, HAS TO BE FILTERED
url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=7013901d945a4d71961a35b20cc62c38')
response = requests.get(url)
print (response.json())

