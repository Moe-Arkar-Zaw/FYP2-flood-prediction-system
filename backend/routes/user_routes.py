from flask import Blueprint, jsonify, request, render_template
from backend.models import Alert, Street, Shelter, Area, Video, FloodPrediction
from backend.database import db
from datetime import datetime, timedelta
from backend.services.route_optimizer import find_safest_route
from backend.auth.auth_routes import login_required

user_bp = Blueprint("user_bp", __name__)

# Publish dashboard page
@user_bp.route("/public_dashboard", methods=["GET"])
@login_required
def dashboard_page():
    return render_template("user/dashboard.html")


@user_bp.route("/dashboard-data", methods=["GET"])
def dashboard_data():
    """
    Return JSON data for public dashboard:
    - Latest alerts (past 7 days)
    - Top 3 areas by severity
    - Streets for map (safe/flooded)
    - Shelters
    """
    try:
        #update_street_severity()
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)
        twenty_four_hours_ago = now - timedelta(hours=24)

        # 1) Latest alerts from past 7 days
        alerts_query = (
            Alert.query
            .join(Alert.prediction)
            .filter(FloodPrediction.prediction_time >= seven_days_ago)
            .order_by(Alert.alert_id.desc())
            .all()
        )

        alerts = [{
            "alert_id": alert.alert_id,
            "prediction_id": alert.prediction_id,
            "street_id": alert.prediction.street_id,
            "street_name": alert.prediction.street.street_name if alert.prediction.street else "Unknown",
            "water_level": alert.prediction.water_level,
            "severity": alert.prediction.severity,
            "prediction_time": alert.prediction.prediction_time.strftime("%Y-%m-%d %H:%M:%S"),
            "alert_message": alert.alert_message
        } for alert in alerts_query]

        # 2) Top 3 areas by severity
        areas_query = Area.query.order_by(Area.severity_level.desc()).limit(3).all()
        areas = [{
            "area_id": area.area_id,
            "area_name": area.area_name,
            "severity_level": area.severity_level,
            "lat": float(area.center_lat),
            "lon": float(area.center_lon)
        } for area in areas_query]

        # 3) Streets for map (last 24 hours)

        streets_query = Street.query.join(Street.videos).join(Video.predictions)\
            .filter(Street.current_severity.isnot(None))\
            .filter(FloodPrediction.prediction_time >= twenty_four_hours_ago)\
            .all()

        safe_routes = []
        flooded_routes = []

        for street in streets_query:
            coords = [
                [float(street.street_start_lat), float(street.street_start_lon)],
                [float(street.street_end_lat), float(street.street_end_lon)]
            ]
            if street.current_severity in ["alert", "severe"]:
                flooded_routes.append({
                    "coords": coords,
                    "severity": street.current_severity
                })
            else:
                safe_routes.append({"coords": coords})


        # 4) Shelters
        shelters_query = Shelter.query.all()
        shelters = [{
            "lat": float(sh.shelter_lat),
            "lon": float(sh.shelter_lon),
            "name": sh.shelter_name
        } for sh in shelters_query]

        return jsonify({
            "alerts": alerts,
            "areas": areas,
            "safe_routes": safe_routes,
            "flooded_routes": flooded_routes,
            "shelters": shelters
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

''' 
@user_bp.route("/api/route-finder", methods=["GET"])
@login_required
def route_finder():
    return render_template("user/route_finder.html")'''

@user_bp.route("/api/route-finder")
@login_required
def route_finder():
    streets = Street.query.all()

    # Filter unique street names without segment suffix (_1, _2, etc.)
    unique_streets = []
    seen = set()
    for s in streets:
        base_name = s.street_name.rsplit("_", 1)[0] if "_" in s.street_name and s.street_name.split("_")[-1].isdigit() else s.street_name
        if base_name not in seen:
            seen.add(base_name)
            unique_streets.append(base_name)

    return render_template("user/route_finder.html", streets=unique_streets)


@user_bp.route("/api/find-safest-route", methods=["POST"])
#@login_required
def find_safest_route_api():
    data = request.json 
    start = data.get("start")
    end = data.get("end")
    return jsonify(find_safest_route(start, end))
