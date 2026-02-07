from flask import Flask, request, jsonify, render_template
import requests
import mysql.connector
import os

app = Flask(__name__)

# ---------- MySQL connection ----------
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root123",
    database="stockdb"
)

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- SEARCH STOCK ----------
@app.route("/search/<name>")
def search(name):
    url = f"https://indian-stock-exchange-api2.p.rapidapi.com/stock?name={name}"

    headers = {
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
        "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------- PRICE SHOCKERS ----------
@app.route("/price")
def price():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/price_shockers"

    headers = {
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
        "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------- IPO ----------
@app.route("/ipo")
def ipo():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/ipo"

    headers = {
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
        "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------- NEWS ----------
@app.route("/news")
def news():
    url = "https://share-market-news-api-india.p.rapidapi.com/marketNews"

    headers = {
        "x-rapidapi-host": "share-market-news-api-india.p.rapidapi.com",
        "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------- SUBSCRIBE ----------
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    cursor = db.cursor()

    sql = "INSERT INTO subscribers (name,email,phone,plan) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql,(data['name'],data['email'],data['phone'],data['plan']))
    db.commit()

    return jsonify({"msg":"Subscribed successfully"})

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    cursor = db.cursor(dictionary=True)
    cursor.execute("select * from subscribers")
    data = cursor.fetchall()
    return render_template("admin.html", data=data)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
