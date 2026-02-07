from flask import Flask, request, jsonify, send_file, render_template
import requests
import mysql.connector
import os

app = Flask(__name__)

# ---------------- DB CONNECTION ----------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "mysql"),
    user="root",
    password="root123",
    database="stockdb"
)

# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return send_file("index.html")

# ---------------- ADMIN PAGE ----------------
@app.route('/admin')
def admin():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM subscribers ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template("admin.html", users=data)

# ---------------- SUBSCRIBE ----------------
@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json
        cursor = db.cursor()

        sql = """INSERT INTO subscribers (name,email,phone,plan)
                 VALUES (%s,%s,%s,%s)"""

        cursor.execute(sql, (
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('plan')
        ))

        db.commit()
        return jsonify({"msg": "Subscribed successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- PRICE SHOCKERS ----------------
@app.route('/price')
def price():
    try:
        url = "https://real-time-finance-data.p.rapidapi.com/stock-price-shockers"
        headers = {
            "x-rapidapi-host": "real-time-finance-data.p.rapidapi.com",
            "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
        }

        res = requests.get(url, headers=headers, timeout=20)
        return jsonify(res.json())

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------- IPO DATA ----------------
@app.route('/ipo')
def ipo():
    try:
        url = "https://indian-stock-exchange-api2.p.rapidapi.com/ipo"
        headers = {
            "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
            "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
        }

        res = requests.get(url, headers=headers, timeout=20)
        return jsonify(res.json())

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------- MARKET NEWS ----------------
@app.route('/news')
def news():
    try:
        url = "https://share-market-news-api-india.p.rapidapi.com/marketNews"
        headers = {
            "x-rapidapi-host": "share-market-news-api-india.p.rapidapi.com",
            "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
        }

        res = requests.get(url, headers=headers, timeout=20)

        if res.status_code != 200:
            return jsonify({"error": "News API failed", "text": res.text})

        try:
            return jsonify(res.json())
        except:
            return jsonify({"error": "Invalid JSON from news API", "text": res.text})

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------- SEARCH STOCK (NEW FEATURE) ----------------
@app.route('/search/<stock>')
def search_stock(stock):
    try:
        url = f"https://indian-stock-exchange-api2.p.rapidapi.com/stock?name={stock}"

        headers = {
            "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
            "x-rapidapi-key": "2c482e59eemsh84b3ee988562f35p1da2bfjsn9d541cf8e4f8"
        }

        res = requests.get(url, headers=headers, timeout=20)

        if res.status_code != 200:
            return jsonify({"error": "Stock API failed", "text": res.text})

        return jsonify(res.json())

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------- RUN ----------------
app.run(host='0.0.0.0', port=5000)
