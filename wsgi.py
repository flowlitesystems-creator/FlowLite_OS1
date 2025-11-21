from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "FlowLite OS1 funcionando en Render."

# ===== WEBHOOK GREENAPI =====
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("WEBHOOK RECIBIDO:", data)  # Para ver el JSON en Render Logs
    return jsonify({"status": "ok"})
