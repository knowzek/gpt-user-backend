
from flask import Flask, request, jsonify
import json
import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")


app = Flask(__name__)
DB_PATH = "users.json"

@app.route("/")
def index():
    return "Backend is running!"

@app.route("/register_user", methods=["POST"])
def register_user():
    data = request.json
    print(f"📩 Incoming user data: {data}")  # ✅ Add this
    email = data.get("email")
    user_id = data.get("user_id")

    if not email or not user_id:
        return jsonify({"error": "Missing fields"}), 400

    payload = {
        "user_id": user_id,
        "email": email
    }

    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json"
    }

    # Send to Supabase
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/users",
        json=payload,
        headers=headers
    )

    if response.status_code >= 400:
        return jsonify({"error": "Failed to write to Supabase", "details": response.text}), 500

    return jsonify({"status": "stored", "user_id": user_id})

