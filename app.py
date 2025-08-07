# app.py
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DB_PATH = "users.json"

@app.route("/")
def index():
    return "Backend is running!"

@app.route("/register_user", methods=["POST"])
def register_user():
    data = request.json
    email = data.get("email")
    user_id = data.get("user_id")

    if not email or not user_id:
        return jsonify({"error": "Missing fields"}), 400

    # Load or create user db
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            users = json.load(f)
    else:
        users = {}

    users[user_id] = {"email": email}

    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=2)

    return jsonify({"status": "registered", "user_id": user_id})
