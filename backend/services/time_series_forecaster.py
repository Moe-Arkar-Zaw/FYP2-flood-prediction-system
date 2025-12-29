"""
Time Series Forecasting for Flood Water Levels
Uses simple moving average and trend analysis
"""
import numpy as np
from datetime import datetime, timedelta
from backend.models import FloodPrediction


def get_historical_data(street_id=None, days=30):
    """
    Get historical flood predictions
    
    Args:
        street_id: Filter by specific street (optional)
        days: Number of days of history to retrieve
        
    Returns:
        List of (timestamp, water_level) tuples
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    query = FloodPrediction.query.filter(
        FloodPrediction.prediction_time >= cutoff_date
    )
    
    if street_id:
        query = query.filter(FloodPrediction.street_id == street_id)
    
    predictions = query.order_by(FloodPrediction.prediction_time.asc()).all()
    
    data = []
    for pred in predictions:
        data.append({
            'timestamp': pred.prediction_time,
            'water_level': float(pred.water_level),
            'severity': pred.severity,
            'street_id': pred.street_id
        })
    
    return data


def forecast_water_levels(historical_data, forecast_days=7):
    """
    Forecast future water levels using moving average and trend
    
    Args:
        historical_data: List of historical data points
        forecast_days: Number of days to forecast
        
    Returns:
        List of forecasted values with timestamps
    """
    if len(historical_data) < 3:
        return []
    
    # Extract water levels and timestamps
    water_levels = np.array([d['water_level'] for d in historical_data])
    timestamps = [d['timestamp'] for d in historical_data]
    
    # Calculate moving average (last 7 days)
    window_size = min(7, len(water_levels))
    moving_avg = np.mean(water_levels[-window_size:])
    
    # Calculate trend (simple linear regression)
    if len(water_levels) >= 5:
        # Use last 5 points to calculate trend
        recent_levels = water_levels[-5:]
        x = np.arange(len(recent_levels))
        
        # Calculate slope
        trend = np.polyfit(x, recent_levels, 1)[0]
    else:
        trend = 0
    
    # Generate forecast
    last_timestamp = timestamps[-1] if timestamps else datetime.now()
    forecasts = []
    
    for i in range(1, forecast_days + 1):
        forecast_timestamp = last_timestamp + timedelta(days=i)
        
        # Forecast = moving average + trend * days ahead
        forecast_value = moving_avg + (trend * i)
        
        # Add some bounds (water level can't be negative or > 1.0)
        forecast_value = max(0.0, min(1.0, forecast_value))
        
        # Determine severity
        if forecast_value < 0.3:
            severity = 'normal'
        elif forecast_value < 0.6:
            severity = 'alert'
        else:
            severity = 'severe'
        
        forecasts.append({
            'timestamp': forecast_timestamp,
            'water_level': round(forecast_value, 3),
            'severity': severity,
            'type': 'forecast'
        })
    
    return forecasts


def calculate_statistics(historical_data):
    """
    Calculate statistics from historical data
    
    Args:
        historical_data: List of historical data points
        
    Returns:
        Dictionary with statistics
    """
    if not historical_data:
        return {
            'mean': 0,
            'max': 0,
            'min': 0,
            'std': 0,
            'trend': 'stable'
        }
    
    water_levels = np.array([d['water_level'] for d in historical_data])
    
    stats = {
        'mean': round(float(np.mean(water_levels)), 3),
        'max': round(float(np.max(water_levels)), 3),
        'min': round(float(np.min(water_levels)), 3),
        'std': round(float(np.std(water_levels)), 3),
        'count': len(water_levels)
    }
    
    # Determine trend
    if len(water_levels) >= 5:
        recent_levels = water_levels[-5:]
        x = np.arange(len(recent_levels))
        slope = np.polyfit(x, recent_levels, 1)[0]
        
        if slope > 0.05:
            stats['trend'] = 'increasing'
        elif slope < -0.05:
            stats['trend'] = 'decreasing'
        else:
            stats['trend'] = 'stable'
    else:
        stats['trend'] = 'insufficient_data'
    
    return stats


def get_forecast_summary(street_id=None, history_days=30, forecast_days=7):
    """
    Get complete forecast summary with historical data and predictions
    
    Args:
        street_id: Filter by street (optional)
        history_days: Days of historical data
        forecast_days: Days to forecast
        
    Returns:
        Dictionary with historical data, forecasts, and statistics
    """
    # Get historical data
    historical = get_historical_data(street_id, history_days)
    
    # Generate forecast
    forecast = forecast_water_levels(historical, forecast_days)
    
    # Calculate statistics
    stats = calculate_statistics(historical)
    
    return {
        'historical': historical[-30:],  # Last 30 points for display
        'forecast': forecast,
        'statistics': stats,
        'street_id': street_id
    }
