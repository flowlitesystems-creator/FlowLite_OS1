from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ID y Token
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

        # Extraer mensaje entrante
        message = data.get("messageData", {})
        text_data = message.get("textMessageData", {})
        incoming_msg = text_data.get("textMessage")

        # Extraer chatId (destino)
        chat_id = data.get("senderData", {}).get("chatId")

        # DEBUG: verificar si entra aquí
        print(f"➡️ incoming_msg = {incoming_msg}")
        print(f"➡️ chat_id = {chat_id}")

        # Si hay mensaje → responder
        if incoming_msg and chat_id:
            print("➡️ ENTRÓ AL BLOQUE DE RESPUESTA")   # ***DEBUG IMPORTANTÍSIMO***
            respuesta = f"Recibí tu mensaje: {incoming_msg}"
            send_message(chat_id, respuesta)
        else:
            print("⚠️ No hay mensaje o chatId — NO responde")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("❌ ERROR WEBHOOK:", e)
        return jsonify({"error": str(e)}), 500



def send_message(chat_id, message):
    print(f"➡️ Enviando mensaje a {chat_id}: {message}")  # ***DEBUG***

    url = f"https://7107.api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("📤 RESPUESTA GREENAPI:", response.text)   # ***DEBUG***
    return response.text



if __name__ == "__main__":
    app.run()
