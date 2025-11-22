from flask_cors import CORS
from flask import Flask, request, jsonify
from firebase_app import db, auth
import traceback
from firebase_admin import firestore
from utils.utils import get_uid

app = Flask(__name__)
app.url_map.strict_slashes = False

CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:3000"}},
    supports_credentials=True
)


@app.post("/signup")
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


@app.get("/profile")
def profile():
    uid = get_uid()

    user = db.collection("users").document(uid).get()
    return jsonify({"user": resolve_references_one_level(user.to_dict())})


@app.post("/check-user")
def check_user():
    phone = request.json.get("phone")
    query = db.collection("users").where("phone", "==", phone).get()

    if query:
        return jsonify({"exists": True})
    return jsonify({"exists": False})



def resolve_references_one_level(data):
    for key, value in data.items():
        if isinstance(value, firestore.DocumentReference):
            data[key] = value.path
        
        elif isinstance(value, list) and value and \
                isinstance(value[0], firestore.DocumentReference):
            
            data[key] = [ref.path for ref in value]
    
    return data


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)