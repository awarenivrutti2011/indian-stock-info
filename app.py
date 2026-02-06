from flask import Flask, request, jsonify
import requests
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root123",
    database="stockdb"
)

# 🔥 stock api
@app.route('/stock/<symbol>')
def get_stock(symbol):
    url = "https://real-time-finance-data.p.rapidapi.com/search"

    querystring = {"query": symbol, "language": "en"}

    headers = {
        "x-rapidapi-host": "real-time-finance-data.p.rapidapi.com",
        "x-rapidapi-key": "bd6e08e67dmsh3937cf5cd697c01p1503b2jsn019262bfc7a9"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


# 🔥 subscribe api
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json

    cursor = db.cursor()
    sql = "INSERT INTO subscribers (name,email,phone,plan) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql,(data['name'],data['email'],data['phone'],data['plan']))
    db.commit()

    return jsonify({"msg":"User subscribed"})


@app.route('/')
def home():
    return "Indian Stock Info Running"

app.run(host='0.0.0.0',port=5000)

