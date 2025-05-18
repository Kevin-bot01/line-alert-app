from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def alert():
    # ThingSpeak JSON 中應有 PM10 數值，例如 field1
    thingspeak_url = os.environ.get("THINGSPEAK_URL")
    r = requests.get(thingspeak_url)
    data = r.json()
    pm10 = data.get("field1", "未知")

    message = f"【PM10警示】偵測PM10為 {pm10} μg/m3，已超過標準值，請小心注意。"

    headers = {
        "Authorization": f"Bearer {os.environ.get('LINE_TOKEN')}",
        "Content-Type": "application/json"
    }
    body = {
        "to": os.environ.get("LINE_USER_ID"),
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=body)
    return {"status": res.status_code}, res.status_code

@app.route("/")
def home():
    return "LINE Alert Webhook Running", 200

if __name__ == "__main__":
    app.run()
