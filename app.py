from flask import Flask, request, jsonify, render_template, send_file
import requests
import mysql.connector
import os

app = Flask(__name__)

# ---------------- DB CONNECTION ----------------
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user="root",
        password="root123",
        database="stockdb"
    )
    print("✅ MySQL Connected")
except Exception as e:
    print("❌ DB ERROR:", e)

# ---------------- HOME ----------------
@app.route('/')
def home():
    try:
        return render_template("index.html")
    except:
        return "index.html not found inside container"

# ---------------- PRICE SHOCKERS ----------------
@app.route('/price')
def price():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/price_shockers"
    headers = {
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
        "x-rapidapi-key": "YOUR_API_KEY"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print("PRICE API ERROR:", e)
        return {"error":"price api failed"}

# ---------------- IPO ----------------
@app.route('/ipo')
def ipo():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/ipo"
    headers = {
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
        "x-rapidapi-key": "YOUR_API_KEY"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print("IPO API ERROR:", e)
        return {"error":"ipo api failed"}

# ---------------- MARKET NEWS (FIXED) ----------------
@app.route('/news')
def news():
    url = "https://share-market-news-api-india.p.rapidapi.com/marketNews"
    headers = {
        "x-rapidapi-host":"share-market-news-api-india.p.rapidapi.com",
        "x-rapidapi-key":"YOUR_API_KEY"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("❌ NEWS API ERROR:", response.text)
            return {"error":"API limit reached or invalid key"}

        return response.json()

    except Exception as e:
        print("NEWS ERROR:", e)
        return {"error":"news api failed"}

# ---------------- SUBSCRIBE ----------------
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json

    try:
        cursor = db.cursor()
        sql = "INSERT INTO subscribers (name,email,phone,plan) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(data['name'],data['email'],data['phone'],data['plan']))
        db.commit()
        print("✅ Data inserted")
        return jsonify({"msg":"Subscribed successfully"})
    except Exception as e:
        print("DB INSERT ERROR:", e)
        return jsonify({"error":"db error"})

# ---------------- ADMIN DASHBOARD (FIXED) ----------------
@app.route('/admin')
def admin():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM subscribers ORDER BY id DESC")
        users = cursor.fetchall()
        print("ADMIN DATA:", users)
        return render_template("admin.html", users=users)
    except Exception as e:
        print("ADMIN ERROR:", e)
        return str(e)

# ---------------- START ----------------
app.run(host='0.0.0.0', port=5000)

