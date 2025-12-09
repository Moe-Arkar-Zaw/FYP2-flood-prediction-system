from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os 

from backend.database import db
from backend.models import Street, Video, FloodPrediction, Alert
from backend.services.video_processor import save_uploaded_video # Admin Video Upload Method
from backend.services.flood_predictor import predict_water_level  # Admin Run Prediction Method
from backend.services.video_processor import extract_frames 
from backend.auth.auth_routes import admin_required

admin_bp = Blueprint("admin", __name__)

# Helper function for severity in prediction and current_severity in streets table
from sqlalchemy import desc 
def update_street_severity():
    streets = Street.query.all()
    for street in streets:
        latest_pred = FloodPrediction.query.filter_by(street_id=street.street_id)\
            .order_by(FloodPrediction.prediction_time.desc())\
            .first()
        if latest_pred:
            street.current_severity = latest_pred.severity
    db.session.commit()


@admin_bp.route("/upload_video", methods=["POST", "GET"])
@admin_required
def upload_video():
    
    if request.method == "GET":
        streets = Street.query.all()
        return render_template("admin/upload_video.html", streets=streets)

    try:
        # Extract from data
        street_name = request.form.get("street_name")
        timestamp = request.form.get("timestamp")
        video_file = request.files.get("video")

        # Validate input 
        if not street_name or not video_file or not timestamp:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Validate street exists
        street = Street.query.filter_by(street_name=street_name).first()
        if not street:
            return jsonify({"error": "Street not found"}), 404
        

        # Save video file
        saved_path = save_uploaded_video(video_file)

        dt = datetime.fromisoformat(timestamp)

        # Insert into DB
        new_video = Video(
            street_id=street.street_id,
            video_path=saved_path,
            upload_timestamp=dt
        )

        db.session.add(new_video)
        db.session.commit()

        session["latest_video_id"] = new_video.video_id
        print("Latest video ID stored in session:", session['latest_video_id'])

        return jsonify({
            "message": "Video uploaded sucessfully",
            "video_id": new_video.video_id,
            "path": saved_path
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/prediction_page")
@admin_required
def prediction_page():
    video_id = session.get("latest_video_id")

    if not video_id:
        return render_template("admin/flood_prediction.html", frames=[], video_id=None)
    
    video = Video.query.get(video_id)
    
    if not video:
        return render_template("admin/flood_prediction.html", frames=[], video_id=None)
    
    frames = extract_frames(video.video_path)

    return render_template("admin/flood_prediction.html", frames=frames, video_id=video_id)


@admin_bp.route("/run_prediction", methods=["POST"])
def run_prediction():
    try:
        # Sends video_id after upload
        video_id = request.json.get("video_id")
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400
        
        # Fetch video from DB
        video = Video.query.get(video_id)
        if not video:
            return jsonify({"error": "Video not found"}), 404
        
        street_id = video.street_id 

        # Extract frames
        frames = extract_frames(video.video_path)

        # Run ML Model
        water_level =predict_water_level(frames)

        # Determin severity 
        if water_level < 0.3:
            severity = 'normal'
        elif water_level < 0.6:
            severity = 'alert'
        else:
            severity = 'severe'

        my_time = datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).replace(tzinfo=None)

        # Store prediction in DB
        new_pred = FloodPrediction(
            video_id = video_id,
            street_id = street_id,
            water_level = water_level,
            severity = severity,
            prediction_time = my_time
        )

        db.session.add(new_pred)
        db.session.commit()

        update_street_severity()

        return jsonify({
            "message": "Prediction completed sucessfully",
            "prediction_id": new_pred.prediction_id,
            "video_id": video_id,
            "street_id": street_id,
            "water_level": water_level,
            "severity": severity
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 5
    
# List all flood predictions from FloodPrediction table
@admin_bp.route("/prediction", methods=['GET'])
def list_predictions():
    predictions = FloodPrediction.query.order_by(FloodPrediction.prediction_time.desc()).all()

    result = []
    for p in predictions:
        result.append({
            "prediction_id": p.prediction_id,
            "video_id": p.video_id,
            "street_id": p.street_id,
            "water_level": p.water_level,
            "severity": p.severity,
            "prediction_time": p.prediction_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({"predictions": result})

# To publish alerts from admin panel to public dashboard (Admin Creates Alert)
@admin_bp.route("/publish_alert", methods=['POST'])
def publish_alert():
    data = request.get_json()

    prediction_id = data.get("prediction_id")
    alert_message = data.get("alert_message")

    if not prediction_id:
        return jsonify({"error": "prediction_id is required"}), 400

    if not alert_message:
        return jsonify({"error": "alert_message is required"}), 400
    
    prediction = FloodPrediction.query.get(prediction_id)
    if not prediction:
        return jsonify({"error": "Prediction not found"}), 404
    
    new_alert = Alert(
        prediction_id = prediction.prediction_id,
        alert_message = alert_message
    )

    db.session.add(new_alert)
    db.session.commit()

    return jsonify({
        "success": True,
        "alert_id": new_alert.alert_id,
        "prediction_id": prediction.prediction_id,
        "street_id": prediction.street_id,
        "severity": prediction.severity,
        "message": alert_message
    }), 200

# Alert render
@admin_bp.route("/alerts", methods=["GET"])
@admin_required
def admin_alerts_page():
    seven_days_ago = datetime.now() - timedelta(days=7)

    predictions = FloodPrediction.query \
        .filter(FloodPrediction.prediction_time >= seven_days_ago) \
        .order_by(FloodPrediction.prediction_time.desc()) \
        .all()
    
    formatted_predictions = []
    for p in predictions:
        formatted_predictions.append({
            "prediction_id": p.prediction_id,
            "street_name": p.street.street_name if p.street else "Unknown",
            "water_level": p.water_level,
            "severity": p.severity,
            "timestamp": p.prediction_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return render_template("admin/alerts.html", predictions=formatted_predictions)