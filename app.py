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


def get_url(entry):
    if isinstance(entry, dict):
        return entry.get("url", "")
    return entry


def get_clicks(entry):
    if isinstance(entry, dict):
        return entry.get("clicks", 0)
    return 0


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
    body = request.get_json() or {}

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

        for saved_code, saved_entry in data.items():
            if get_url(saved_entry) == url:
                code = saved_code
                break

        if code is None:
            code = generate_code()

    data[code] = {
        "url": url,
        "clicks": get_clicks(data.get(code, {}))
    }

    save_data(data)

    return jsonify({
        "code": code,
        "url": url
    })


@app.route("/links")
def get_links():
    data = load_data()

    recent = list(data.items())[-8:]
    recent.reverse()

    return jsonify([
        {
            "code": code,
            "url": get_url(entry),
            "clicks": get_clicks(entry)
        }
        for code, entry in recent
    ])


@app.route("/<code>")
def redirect_url(code):
    data = load_data()

    if code not in data:
        return "Short URL not found.", 404

    entry = data[code]

    # Support both old and new data formats
    if isinstance(entry, dict):
        entry["clicks"] = entry.get("clicks", 0) + 1
        destination = entry.get("url", "")
    else:
        destination = entry
        data[code] = {
            "url": destination,
            "clicks": 1
        }

    save_data(data)

    return redirect(destination)


if __name__ == "__main__":
    app.run(debug=True)