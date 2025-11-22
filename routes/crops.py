from flask import Blueprint, request, jsonify
from firebase_app import db
from utils.utils import get_uid, resolve_references_one_level
import traceback

crop_bp = Blueprint("user", __name__)


@crop_bp.post("/signup")
def signup():
    try:
        data = request.json
        uid = data.get("uid")

        user_data = {
            "name": data.get("name"),
            "phone": data.get("number"),
            "aadharNumber": data.get("aadhar"),
            "address": data.get("address"),
            "type": data.get("type"),
        }


        db.collection("users").document(uid).set(user_data)

        return jsonify({"message": "Signup successful", "user": {**user_data, "uid": uid}})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

