# app.py
from flask import Flask, request, jsonify
from scraper import get_valorant_stats

app = Flask(__name__)

@app.route("/stats")
def stats():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Missing ?username=..."}), 400

    try:
        data = get_valorant_stats(username)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
