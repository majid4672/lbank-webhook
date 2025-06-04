
from flask import Flask, request, jsonify
import hmac, hashlib, time, requests

app = Flask(__name__)

API_KEY = "YOUR_LBANK_API_KEY"
API_SECRET = "YOUR_LBANK_SECRET"

def place_order(symbol, side, amount, price):
    endpoint = "https://api.lbank.info/v2/supplement/create_order.do"
    ts = str(int(time.time() * 1000))

    params = {
        "api_key": API_KEY,
        "symbol": symbol.lower(),
        "type": "buy" if side == "BUY" else "sell",
        "price": price,
        "amount": amount,
        "timestamp": ts
    }

    sign = make_sign(params)
    params["sign"] = sign

    response = requests.post(endpoint, data=params)
    return response.json()

def make_sign(params):
    sorted_params = sorted(params.items())
    sign_str = ""
    for k, v in sorted_params:
        sign_str += k + "=" + str(v) + "&"
    sign_str += "secret_key=" + API_SECRET
    return hashlib.md5(sign_str.encode()).hexdigest().upper()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    symbol = data.get("symbol", "eth_usdt")
    side = data.get("side", "BUY")
    price = float(data.get("price", 0))
    amount = 10 / price  # مقدار دلاری ثابت (۱۰ دلار)

    response = place_order(symbol, side, amount, price)
    return jsonify({"status": "executed", "exchange_response": response})

@app.route("/", methods=["GET"])
def home():
    return "LBank Webhook is running!", 200
