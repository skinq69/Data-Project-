from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client
import os

app = Flask(__name__, static_folder='static')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

ADMIN_NAME = os.environ.get("ADMIN_NAME")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

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

    # Admin code — delete all data and reset ID counter
    if name == ADMIN_NAME and email == ADMIN_EMAIL:
        supabase.table("Data").delete().neq("id", 0).execute()
        supabase.rpc("reset_data_id_sequence").execute()
        return jsonify({"message": "All data deleted and ID reset."}), 200

    try:
        supabase.table("Data").insert({"Name": name, "Gmail": email}).execute()
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
