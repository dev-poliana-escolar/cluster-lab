from flask import Flask, request, send_file
import os

app = Flask(__name__)

STORAGE = "/app/storage"

os.makedirs(STORAGE, exist_ok=True)


@app.route("/store", methods=["POST"])
def store():
    filename = request.headers.get("X-Filename")

    if not filename:
        return {"error": "Filename não informado"}, 400

    path = os.path.join(STORAGE, filename)

    with open(path, "wb") as file:
        file.write(request.data)

    return {
        "message": "Arquivo armazenado",
        "node": os.getenv("HOSTNAME"),
        "file": filename
    }


@app.route("/file/<filename>", methods=["GET"])
def get_file(filename):
    path = os.path.join(STORAGE, filename)

    if not os.path.exists(path):
        return {"error": "Arquivo não encontrado"}, 404

    return send_file(path)


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "online",
        "node": os.getenv("HOSTNAME")
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)