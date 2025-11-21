from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

GREEN_ID = "7107368022"
GREEN_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a17646509e43169a"

@app.route("/")
def home():
    return "FlowLite OS1 funcionando en Render."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json

        print("📩 WEBHOOK RECIBIDO:")
        print(json.dumps(data, indent=4, ensure_ascii=False))

        # 🔥 DESACTIVAMOS LA RESPUESTA AUTOMÁTICA PARA PROBAR
        return jsonify({"status": "ok"}), 200

        # --- EL RESTO DEL CÓDIGO SE SALTA TEMPORALMENTE ---
        # message = data.get("messageData", {})
        # text_data = message.get("textMessageData", {})
        # incoming_msg = text_data.get("textMessage")

        # chat_id = data.get("senderData", {}).get("chatId")

        # if incoming_msg and chat_id:
        #     respuesta = f"Recibí tu mensaje: {incoming_msg}"
        #     send_message(chat_id, respuesta)

        # return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("❌ ERROR WEBHOOK:", e)
        return jsonify({"error": str(e)}), 500


def send_message(chat_id, message):
    url = f"https://7107.api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("📤 RESPUESTA GREENAPI:")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)


if __name__ == "__main__":
    app.run()
