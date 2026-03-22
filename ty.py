# Hackathon-project. A finance and investing tool to predict the future of specific stocks.
from flask import Flask, render_template, jsonify
import yfinance as yf
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("website.html")

NEWS_API_KEY = "7013901d945a4d71961a35b20cc62c38"

@app.route("/stock/<symbol>")
def get_stock(symbol):
    try:
        # Get stock data
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        price = hist["Close"].iloc[-1]
        avg = hist["Close"].mean()
        prediction = "Likely Up" if price > avg else "Likely Down"
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&pageSize=5"
        news = requests.get(url, timeout=5).json()
        events = []
        for article in news.get("articles", []):
            if article.get("title"):
                events.append(article["title"])
        return jsonify({
            "price": round(price, 2),
            "prediction": prediction,
            "events": events
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
    
    