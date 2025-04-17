from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask_cors import CORS

# Initialize Firebase Admin SDK
cred = credentials.Certificate("backend/firebase-admin-key.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = "Yukeshwaran@07"  # For session management
CORS(app)

# Serve the Login page
@app.route("/login")
def login():
    return render_template("login.html")

# Serve the Signup page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Serve the Dashboard page after successful login
@app.route("/dashboard")
def dashboard():
    if "user_email" in session:
        return render_template("dashboard.html", email=session["user_email"])
    else:
        return redirect(url_for("login"))

# Verify the Firebase ID Token and Create Session
@app.route("/verify-token", methods=["POST"])
def verify_token():
    data = request.get_json()
    id_token = data.get("idToken")

    if not id_token:
        return jsonify({"error": "ID Token is missing"}), 400

    try:
        # Verify the ID token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        user_email = decoded_token.get("email")
        session["user_email"] = user_email  # Store email in session
        return jsonify({"message": "Token verified", "email": user_email})
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401

# Signup Route (Register new user)
@app.route("/register", methods=["POST"])
def register():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not username or not email or not password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Check if user already exists
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )
        return jsonify({"message": "User registered successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Chat Route for creating a chat room between users
@app.route("/create-chat", methods=["POST"])
def create_chat():
    data = request.get_json()
    user_email = session.get("user_email")
    friend_email = data.get("friend_email")

    if not user_email or not friend_email:
        return jsonify({"error": "User and friend emails are required"}), 400

    # Check if both users exist in the database
    user_ref = firestore.client().collection("users").document(user_email)
    friend_ref = firestore.client().collection("users").document(friend_email)

    user_doc = user_ref.get()
    friend_doc = friend_ref.get()

    if not user_doc.exists or not friend_doc.exists:
        return jsonify({"error": "One or both users do not exist"}), 400

    # Create a new chat room
    chat_ref = firestore.client().collection("chats").document()
    chat_ref.set({
        "participants": [user_email, friend_email],
        "messages": []
    })

    return jsonify({"message": "Chat created", "chat_id": chat_ref.id})

if __name__ == "__main__":
    app.run(debug=True)
