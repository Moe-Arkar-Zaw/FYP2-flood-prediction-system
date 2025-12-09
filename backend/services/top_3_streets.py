from backend.models import FloodPrediction, Street 
from backend.database import db 
from datetime import datetime, timedelta 
from sqlalchemy import func, desc 

# get top 3 flooded streets from mysql 
def get_top_flooded_streets(limit=3):
    """
    Return top 3 streets based on highest water level
    """

    # Get max water level per street
    subquery = (
        db.session.query(
            FloodPrediction.street_id,
            func.max(FloodPrediction.water_level).label("peak_water_level")
        )
        .group_by(FloodPrediction.street_id)
        .subquery()
    )

    # Join Street table for street names 
    results = (
        db.session.query(
            Street.street_id,
            Street.street_name,
            subquery.c.peak_water_level
        )
        .join(subquery, Street.street_id == subquery.c.street_id)
        .order_by(desc(subquery.c.peak_water_level))
        .limit(limit)
        .all()
    )

    streets = [
        {
            "street_id": r.street_id,
            "street_name": r.street_name,
            "peak_water_level": float(r.peak_water_level)
        } for r in results
    ]

    return streets

def get_flood_trend(street_id):
    """
    Return trend data for a specific street(depends on user select):
    - line chart (last 7 days)
    - last water level (current)
    -Trend (based on last two predictions)
    """
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    predictions = (
        db.session.query(FloodPrediction)
        .filter(
            FloodPrediction.street_id == street_id,
            FloodPrediction.prediction_time >= seven_days_ago
        )
        .order_by(FloodPrediction.prediction_time.asc())
        .all()
    )

    if not predictions:
        return {"error": "No predictions for this street in last 7 days."}
    
    # Line chart data
    chart = [
        {
            "time": p.prediction_time.isoformat(),
            "value": p.water_level
        } for p in predictions
    ]

    # latest prediction for current water level
    current_level = predictions[-1].water_level

    # Trend
    if len(predictions) >= 2:
        last = predictions[-1].water_level
        prev = predictions[-2].water_level
        if last > prev:
            trend = "increasing"
        elif last < prev:
            trend = "decreasing"
        else:
             trend = "stable"
    else:
        trend = "stable"

    street_name = predictions[-1].street.street_name

    return {
        "street_id": street_id,
        "street_name": street_name,
        "current_level": current_level,
        "trend": trend,
        "chart": chart
    }
