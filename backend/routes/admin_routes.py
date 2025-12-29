from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os 

from backend.database import db
from backend.models import Street, Video, FloodPrediction, Alert
from backend.services.video_processor import save_uploaded_video, get_frames_for_prediction # Admin Video Upload Method
from backend.services.flood_predictor import predict_water_level  # Admin Run Prediction Method
from backend.services.video_processor import extract_frames 
from backend.services.time_series_forecaster import get_forecast_summary
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
        # Clear previous session data
        import sys
        print("=== NEW VIDEO UPLOAD STARTED ===", flush=True)
        sys.stdout.flush()
        session.pop("latest_video_id", None)
        session.pop("frame_paths", None)
        print("Session cleared", flush=True)
        
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
        print("Latest video ID stored in session:", session['latest_video_id'], flush=True)
        
        # Extract frames immediately after upload
        print(f"Extracting frames from uploaded video: {saved_path}", flush=True)
        frame_paths = extract_frames(saved_path, max_frames=10, save_frames=True)
        print(f"Extracted {len(frame_paths)} frames: {frame_paths}", flush=True)
        
        # Store frame paths in session for display
        session["frame_paths"] = frame_paths

        return jsonify({
            "message": "Video uploaded sucessfully",
            "video_id": new_video.video_id,
            "path": saved_path,
            "frames_extracted": len(frame_paths)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/prediction_page")
@admin_required
def prediction_page():
    import sys
    video_id = session.get("latest_video_id")
    frame_paths = session.get("frame_paths", [])
    
    print(f"=== PREDICTION PAGE DEBUG ===", flush=True)
    sys.stdout.flush()
    print(f"Video ID from session: {video_id}", flush=True)
    print(f"Frame paths from session: {frame_paths}", flush=True)
    print(f"Number of frames: {len(frame_paths)}", flush=True)

    if not video_id:
        print("No video_id in session")
        return render_template("admin/flood_prediction.html", frames=[], video_id=None)
    
    video = Video.query.get(video_id)
    
    if not video:
        print("Video not found in database")
        return render_template("admin/flood_prediction.html", frames=[], video_id=None)
    
    # If frames weren't extracted during upload, extract them now
    if not frame_paths:
        print(f"Extracting frames on prediction page for video: {video.video_path}")
        frame_paths = extract_frames(video.video_path, max_frames=10, save_frames=True)
        session["frame_paths"] = frame_paths
        print(f"Extracted {len(frame_paths)} frames")
    
    print(f"Passing {len(frame_paths)} frames to template")
    print(f"Frame paths: {frame_paths}")

    return render_template("admin/flood_prediction.html", frames=frame_paths, video_id=video_id)


@admin_bp.route("/run_prediction", methods=["POST"])
def run_prediction():
    try:
        import sys
        print("=== RUN PREDICTION STARTED ===", flush=True)
        sys.stdout.flush()
        
        # Sends video_id after upload
        video_id = request.json.get("video_id")
        print(f"Video ID: {video_id}", flush=True)
        
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400
        
        # Fetch video from DB
        video = Video.query.get(video_id)
        print(f"Video found: {video}", flush=True)
        
        if not video:
            return jsonify({"error": "Video not found"}), 404
        
        street_id = video.street_id 
        print(f"Video path: {video.video_path}", flush=True)

        # Extract frames for prediction (numpy arrays)
        frames = get_frames_for_prediction(video.video_path)
        print(f"Frames extracted: {len(frames)}", flush=True)
        
        if not frames or len(frames) == 0:
            return jsonify({"error": "Could not extract frames from video"}), 400

        # Run ML Model
        print("Running water level prediction...", flush=True)
        water_level = predict_water_level(frames)
        print(f"Water level result: {water_level}", flush=True)

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
        import sys
        print(f"=== PREDICTION ERROR ===", flush=True)
        print(f"Error: {str(e)}", flush=True)
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
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


# Time Series Forecasting Page
@admin_bp.route("/forecast", methods=["GET"])
@admin_required
def forecast_page():
    """
    Display time series forecasting page for flood predictions
    """
    streets = Street.query.all()
    street_id = request.args.get('street_id', type=int)
    
    return render_template("admin/forecast.html", streets=streets, selected_street_id=street_id)


# API endpoint for forecast data
@admin_bp.route("/api/forecast", methods=["GET"])
@admin_required
def get_forecast():
    """
    Get forecast data for display
    """
    try:
        street_id = request.args.get('street_id', type=int)
        history_days = request.args.get('history_days', 30, type=int)
        forecast_days = request.args.get('forecast_days', 7, type=int)
        
        # Get forecast summary
        summary = get_forecast_summary(street_id, history_days, forecast_days)
        
        # Format timestamps for JSON
        for item in summary['historical']:
            item['timestamp'] = item['timestamp'].isoformat() if item['timestamp'] else None
        
        for item in summary['forecast']:
            item['timestamp'] = item['timestamp'].isoformat() if item['timestamp'] else None
        
        return jsonify(summary)
    
    except Exception as e:
        print(f"Forecast error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
