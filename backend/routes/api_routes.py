from flask import Blueprint, jsonify, render_template
from backend.services.top_3_streets import get_top_flooded_streets, get_flood_trend
from backend.models import Shelter
from backend.auth.auth_routes import login_required

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/top-flooded-streets-page", methods=["GET"])
@login_required
def top_flooded_streets_page():
    return render_template("user/top_flooded.html")

@api_bp.route("/top-flooded-streets", methods=['GET'])
def top_flooded_streets():
    streets = get_top_flooded_streets()
    return jsonify({"streets": streets})


@api_bp.route("/flood-trend/<int:street_id>", methods=['GET'])
def flood_trend(street_id):
    trend_data = get_flood_trend(street_id)
    return jsonify(trend_data)


@api_bp.route("/emergency", methods=["GET"])
@login_required 
def emergency_page():
    return render_template("user/emergency.html")

# Emergency Contacts
@api_bp.route("/emergency/contacts", methods=["GET"])
def get_emergency_contacts():
    contacts = [
        {"type": "Police", "number": "+999"},
        {"type": "Emergency Medical Services", "number": "+998"},
        {"type": "Fire & Rescue Department", "number": "+994"},
        {"type": "Civil Defence Hotline", "number": "+993"},
        {"type": "Flood Response Unit", "number": "+997"},
        {"type": "Disaster Management Command Center", "number": "+995"},
    ]
    return jsonify({"contacts": contacts})


# Emergency Shelters
@api_bp.route("/emergency/shelters", methods=["GET"])
def get_shelters():
    shelters = Shelter.query.all()

    result = []
    for s in shelters:
        result.append({
            "shelter_id": s.shelter_id,
            "name": s.shelter_name,
            "address": s.address,
            "capacity": s.capacity
        })

    return jsonify({"shelters": result})


 
# Safety Information
@api_bp.route("/emergency/safety-info", methods=["GET"])
def get_safety_info():
    safety_info = {
        "before_flood": [
            "Prepare an emergency kit with food, water, flashlight, and medicine.",
            "Know evacuation routes and the nearest shelters.",
            "Store important documents in waterproof bags.",
            "Keep power banks charged in advance."
        ],
        "during_flood": [
            "Move to higher ground immediately.",
            "Do not walk or drive through floodwaters.",
            "Turn off electricity before evacuating.",
            "Follow official alerts and announcements."
        ],
        "after_flood": [
            "Return home only when authorities declare it safe.",
            "Avoid contaminated water and damaged electrical systems.",
            "Document damages for insurance claims.",
            "Clean and disinfect items exposed to floodwater."
        ]
    }
    return jsonify({"tips": safety_info})

