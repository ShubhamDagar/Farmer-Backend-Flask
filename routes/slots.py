from flask import Blueprint, request, jsonify
from firebase_app import db
from utils.utils import get_uid

slot_bp = Blueprint("slot", __name__)


@slot_bp.get("/")
def get_my_crops():
    uid = get_uid()
    slots = db.collection("slots").where("userId", "==", uid).stream()

    result = []
    for c in slots:
        item = c.to_dict()
        item["id"] = c.id
        result.append(item)

    return jsonify(result)

@slot_bp.post("/")
def create_slot():
    uid = get_uid()
    data = request.json
    data["userId"] = uid

    if not data or "user_id" not in data or "slot_time" not in data:
        return jsonify({"error": "user_id and slot_time required"}), 400

    ref = db.collection("slots").add(data)[1]

    return jsonify({"id": ref.id, **data})

@slot_bp.delete("/<slot_id>")
def delete_slot(slot_id):
    uid = get_uid()

    doc = db.collection("slots").document(slot_id).get()
    if not doc.exists or doc.to_dict().get("userId") != uid:
        return jsonify({"error": "Unauthorized"}), 403

    db.collection("slots").document(slot_id).delete()
    return jsonify({"success": True})