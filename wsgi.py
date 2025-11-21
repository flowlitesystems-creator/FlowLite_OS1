from flask import Flask, request, jsonify
from os import getenv
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "FlowLite OS1 funcionando en Render."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json

        print("📩 WEBHOOK RECIBIDO:")
        print(json.dumps(data, indent=4, ensure_ascii=False))

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("❌ ERROR WEBHOOK:", e)
        return jsonify({"error": str(e)}), 500
