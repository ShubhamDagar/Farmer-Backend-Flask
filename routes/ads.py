from flask import Blueprint, request, jsonify
from firebase_app import db
from utils.utils import get_uid
from firebase_admin import firestore

ads_bp = Blueprint("ads", __name__)


@ads_bp.get("/")
def get_my_ads():
    uid = get_uid()
    ads = db.collection("ads").where("userId", "==", uid).stream()

    result = []
    for c in ads:
        item = c.to_dict()
        item["id"] = c.id
        result.append(item)

    return jsonify(result)

@ads_bp.post("/")
def create_ads():
    uid = get_uid()
    data = request.json
    data["userId"] = uid
    data["createdAt"] = firestore.SERVER_TIMESTAMP

    ref = db.collection("ads").add(data)[1]

    return jsonify({"id": ref.id, **data})

@ads_bp.delete("/<ads_id>")
def delete_ads(ads_id):
    uid = get_uid()

    doc = db.collection("ads").document(ads_id).get()
    if not doc.exists or doc.to_dict().get("userId") != uid:
        return jsonify({"error": "Unauthorized"}), 403

    db.collection("ads").document(ads_id).delete()
    return jsonify({"success": True})