from backend.database import db 
from datetime import datetime 
from sqlalchemy import Numeric

# User table 
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(50), nullable=True)
    profile_image_url = db.Column(db.String(500), nullable=True)

# Areas table
class Area(db.Model):
    __tablename__ = "areas"

    area_id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(255), nullable=False)
    center_lat = db.Column(db.Numeric(21, 18))
    center_lon = db.Column(db.Numeric(21, 18))
    radius = db.Column(db.Float)
    severity_level = db.Column(db.Enum('normal', 'alert', 'severe'), default='normal')
    
    streets = db.relationship("Street", backref="area", lazy=True)

# Streets table
class Street(db.Model):
    __tablename__ = "streets"

    street_id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(255), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.area_id"), nullable=False)
    street_start_lat = db.Column(db.Numeric(21, 18))
    street_start_lon = db.Column(db.Numeric(21, 18))
    street_end_lat = db.Column(db.Numeric(21, 18))
    street_end_lon = db.Column(db.Numeric(21, 18))
    current_severity = db.Column(db.Enum('normal', 'alert', 'severe'), default='normal')

    routes_start = db.relationship("Route", backref="start_street", lazy=True, foreign_keys="Route.start_street_id")
    routes_end = db.relationship("Route", backref="end_street", lazy=True, foreign_keys="Route.end_street_id")
    videos = db.relationship("Video", backref="street", lazy=True)


# Routes table
class Route(db.Model):
    __tablename__ = "routes"

    route_id = db.Column(db.Integer, primary_key=True)
    start_street_id = db.Column(db.Integer, db.ForeignKey("streets.street_id"), nullable=False)
    end_street_id = db.Column(db.Integer, db.ForeignKey("streets.street_id"), nullable=False)
    distance = db.Column(db.Double)
    #weight = db.Column(db.Float)
    route_start_lat = db.Column(db.Numeric(21, 18))
    route_start_lon = db.Column(db.Numeric(21, 18))
    route_end_lat = db.Column(db.Numeric(21, 18))
    route_end_lon = db.Column(db.Numeric(21, 18))

# Shelters table
class Shelter(db.Model):
    __tablename__ = "shelters"

    shelter_id = db.Column(db.Integer, primary_key=True)
    shelter_name = db.Column(db.String(255), nullable=False)
    shelter_lat = db.Column(db.Numeric(21, 18))
    shelter_lon = db.Column(db.Numeric(21, 18))
    address = db.Column(db.String(255))
    capacity = db.Column(db.Integer)

# Video table
class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer, primary_key=True)
    street_id = db.Column(db.Integer, db.ForeignKey("streets.street_id"), nullable=False)
    video_path = db.Column(db.String(255), nullable=False)
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    predictions = db.relationship("FloodPrediction", backref="video", lazy=True)

# Flood Prediction table
class FloodPrediction(db.Model):
    __tablename__ = "flood_predictions"

    prediction_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("streets.street_id"), nullable=False)
    water_level = db.Column(db.Float)
    severity = db.Column(db.Enum('normal', 'alert', 'severe'), default='normal')
    prediction_time = db.Column(db.DateTime, default=datetime.utcnow)

    alerts = db.relationship("Alert", backref="prediction", lazy=True)
    street = db.relationship("Street", backref="predictions", lazy=True)

# Alert table
class Alert(db.Model):
    __tablename__ = "alerts"

    alert_id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey("flood_predictions.prediction_id"), nullable=False)
    alert_message = db.Column(db.String(255))


