from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("firebase-admin-key.json")
firebase_admin.initialize_app(cred)

@app.route("/api/send-message", methods=["POST"])
def send_message():
    try:
        id_token = request.headers.get("Authorization").split(" ")[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]

        data = request.get_json()
        message = data.get("message")

        # You can store this in a DB like Firestore or SQLite
        print(f"User {uid} says: {message}")

        return jsonify({"status": "success", "message": "Message received"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 401
if __name__ == '__main__':
    app.run(debug=True)