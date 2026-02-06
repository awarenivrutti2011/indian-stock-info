from flask import Flask, request, jsonify, send_file
import requests
import mysql.connector

app = Flask(__name__)

# 🔥 HOME PAGE
@app.route('/')
def home():
    return send_file("index.html")


# 🔥 STOCK API
@app.route('/stock/<symbol>')
def get_stock(symbol):
    url = "https://real-time-finance-data.p.rapidapi.com/search"
    querystring = {"query": symbol, "language": "en"}

    headers = {
        "x-rapidapi-host": "real-time-finance-data.p.rapidapi.com",
        "x-rapidapi-key": "YOUR_API_KEY"   # <-- put your key
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


# 🔥 SUBSCRIBE API
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json

    try:
        # fresh db connection every request
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root123",
            database="stockdb"
        )

        cursor = db.cursor()

        # auto create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            plan VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # insert data
        sql = "INSERT INTO subscribers (name,email,phone,plan) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(data['name'],data['email'],data['phone'],data['plan']))
        db.commit()

        return jsonify({"msg":"Subscription successful"})

    except Exception as e:
        return jsonify({"error":str(e)})


# 🔥 RUN APP
app.run(host='0.0.0.0', port=5000)

