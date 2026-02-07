from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# ================================
# 🔥 YOUR RAPIDAPI KEY (already added)
# ================================
NEWS_API_URL = "https://share-market-news-api-india.p.rapidapi.com/marketNews"
HEADERS = {
    "x-rapidapi-host": "share-market-news-api-india.p.rapidapi.com",
    "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
}

# ================================
# 🔥 STORE SUBSCRIBERS (memory)
# ================================
subscribers = []

# ================================
# HOME PAGE
# ================================
@app.route("/")
def home():
    return render_template("index.html")

# ================================
# ADMIN PAGE
# ================================
@app.route("/admin")
def admin():
    return render_template("admin.html")

# ================================
# GET MARKET NEWS
# ================================
@app.route("/get_news")
def get_news():
    try:
        res = requests.get(NEWS_API_URL, headers=HEADERS, timeout=10)
        data = res.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

# ================================
# SUBSCRIBE API
# ================================
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    email = data.get("email")

    if email and email not in subscribers:
        subscribers.append(email)

    return jsonify({"status": "subscribed", "total": len(subscribers)})

# ================================
# GET SUBSCRIBERS (ADMIN)
# ================================
@app.route("/get_subscribers")
def get_subscribers():
    return jsonify(subscribers)

# ================================
# RUN
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

