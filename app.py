from flask import Flask, request, jsonify, send_from_directory, redirect
import json
import random
import string
import os

app = Flask(__name__)

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def generate_code():
    characters = string.ascii_letters + string.digits

    while True:
        code = "".join(random.choice(characters) for _ in range(6))

        if code not in load_data():
            return code


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


@app.route("/shorten", methods=["POST"])
def shorten():
    data = load_data()
    body = request.get_json()

    url = body.get("url", "").strip()
    alias = body.get("alias", "").strip()

    if not url:
        return jsonify({"error": "Please enter a URL."}), 400

    if alias:
        code = alias

        if code in data:
            return jsonify({"error": "Alias already exists."}), 400

    else:
        code = None

        for saved_code, saved_url in data.items():
            if saved_url == url:
                code = saved_code
                break

        if code is None:
            code = generate_code()

    data[code] = url
    save_data(data)

    return jsonify({
        "code": code,
        "url": url
    })
@app.route("/<code>")
def redirect_url(code):
    data = load_data()

    if code not in data:
        return "Short URL not found.", 404

    return redirect(data[code])
if __name__ == "__main__":
    app.run(debug=True)