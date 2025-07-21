import os
from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask 서버가 작동 중입니다!"

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()

    try:
        res = supabase.table("attendees") \
            .select("*") \
            .eq("name", name) \
            .ilike("email", email) \
            .execute()

        if len(res.data) == 0:
            return jsonify({"status": "not_found", "message": "참가자 정보가 없습니다."}), 404

        user = res.data[0]
        return jsonify({
            "status": "matched",
            "name": user["name"],
            "affiliation": user["affiliation"],
            "position": user["position"]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
