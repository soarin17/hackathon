from flask import Flask, render_template, jsonify
import yfinance as yf
import requests
from openai import OpenAI

app = Flask(__name__)

NEWS_API_KEY = "7013901d945a4d71961a35b20cc62c38"

ai_client = OpenAI(
    api_key="sk-ZZh65j-L040DIfJR0l1Owg",
    base_url="https://hackathonlite-production.up.railway.app",
)

@app.route("/")
def home():
    return render_template("website.html")

@app.route("/stock/<symbol>")
def get_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        price = hist["Close"].iloc[-1]
        avg = hist["Close"].mean()

        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&pageSize=5"
        news = requests.get(url, timeout=5).json()
        headlines = [a["title"] for a in news.get("articles", []) if a.get("title")]

        prompt = f"""
You are a stock analyst. Given the following data for {symbol}, provide:
1. A short prediction (Up or Down) with reasoning based on the price vs average.
2. A brief summary of the recent news and how it might affect the stock.
3. A simple recommendation (Buy, Hold, Sell) based on the analysis.
4. A short summary of the stock performance and news headlines.
5. You should not try to make text bold in the analysis, 


Stock: {symbol}
Current Price: ${round(price, 2)}
1-Month Average Price: ${round(avg, 2)}

Recent News Headlines:
{chr(10).join(f"- {h}" for h in headlines)}

Keep your response concise, clear and simple.
        """

        response = ai_client.chat.completions.create(
            model="gemini-3-flash-preview",
            messages=[{"role": "user", "content": prompt}],
        )

        ai_analysis = response.choices[0].message.content

        return jsonify({
            "symbol": symbol,
            "price": round(price, 2),
            "ai_analysis": ai_analysis,
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__": 
    app.run(host="0.0.0.0", debug=True)
