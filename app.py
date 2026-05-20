from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client
import os

app = Flask(__name__, static_folder='static')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400

    try:
        supabase.table("Data").insert({"name": name, "email": email}).execute()
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
