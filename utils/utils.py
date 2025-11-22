from firebase_admin import auth
from flask import request, abort

def get_uid():
    header = request.headers.get("Authorization")
    if not header:
        abort(401, description="Missing Authorization header")
    token = header.split(" ")[1]

    try:
        decoded = auth.verify_id_token(token)
        return decoded["uid"]
    except:
        abort(401, description="Invalid or expired token")