from flask import Blueprint, request, jsonify, session, render_template, url_for
from backend.database import db 
from backend.models import User 
from backend.auth.auth_routes import login_required
import os 
from werkzeug.utils import secure_filename 
from backend.auth.auth_service import verify_password, hash_password

profile_bp = Blueprint("user-profile", __name__)

UPLOAD_FOLDER = "static/profile_image_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Profile page 
@profile_bp.route("/profile", methods=["GET"])
@login_required
def profile_page():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    return render_template("user/profile.html", user=user)


@profile_bp.route("/upload-profile-image", methods=["POST"])
@login_required
def upload_profile_image():

    # No file uploaded
    if "profile_image" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["profile_image"]

    if file.filename == "":
        return jsonify({"success": False, "error": "Empty file name"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(save_path)

    # Build correct URL
    image_url = "/" + save_path.replace("\\", "/")

    # Update DB
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    user.profile_image_url = image_url
    db.session.commit()

    return jsonify({"success": True, "image_url": image_url})


# Edit profile Page
@profile_bp.route("/edit-profile", methods=["GET"])
@login_required
def edit_profile_page():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    return render_template("user/edit_profile.html", user=user)

# Edit profile (username)
@profile_bp.route("/update-profile", methods=["POST"])
@login_required
def update_profile():
    data = request.json
    new_name = data.get("full_name")

    if not new_name:
        return jsonify({"success": False, "error": "Name cannot be empty"}), 400

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    user.username = new_name
    db.session.commit()

    return jsonify({"success": True, "message": "Profile updated successfully"})

# Change password page
@profile_bp.route("/change-password", methods=["GET"])
@login_required
def change_password_page():
    return render_template("user/change_password.html")

# Change password
@profile_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.json

    old_pw = data.get("old_password")
    new_pw = data.get("new_password")

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    # Check current password
    if not verify_password(user.password_hash, old_pw):
        return jsonify({"success": False, "error": "Incorrect current password"}), 400

    # Update password
    user.password_hash = hash_password(new_pw)
    db.session.commit()

    return jsonify({"success": True, "message": "Password updated successfully"})



