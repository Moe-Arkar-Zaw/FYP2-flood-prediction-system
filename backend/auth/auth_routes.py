from flask import Blueprint, request, jsonify, session, render_template, url_for
from backend.database import db 
from backend.models import User 
from backend.auth.auth_service import hash_password, verify_password 
from functools import wraps 

auth_bp = Blueprint("auth", __name__)

# Decorators 
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated 

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        if session.get("role") != "admin":
            return jsonify({"error": "Accessed Denied"}), 403

        return f(*args, **kwargs)
    return decorated 


# Signup page
@auth_bp.route("/signup-page", methods=["GET"])
def signup_page():
    return render_template("signup.html")

# Signup
@auth_bp.post("/signup")
def signup():
    data = request.json 
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing field"}), 400

    # Email exists?
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exist"}), 400

    # Username exists?
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Create user
    new_user = User(
        username = username,
        email = email,
        password_hash = hash_password(password),
        user_role = "public"
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Signup successful. You may now log in."
    }), 201

#login page
@auth_bp.route("/login-page", methods=["GET"])
def login_page():
    return render_template("login.html")

# Login
@auth_bp.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create session
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["role"] = user.user_role.lower() 
    
    # Redirect based on role
    return jsonify({
        "message": "Login successful",
        "role": session["role"]
    })

# Logout
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out"})

# Session status 
@auth_bp.get("/session")
def session_status():
    if "user_id" not in session:
        return jsonify({"logged_in": False})
    
    return jsonify({
        "logged_in": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "role": session["role"]
    })
 