"""
Flood Water Level Predictor
Integrates V-FloodNet for water level estimation
"""
from backend.services.vfloodnet.water_level_estimator import predict_water_level

# Export the function directly - it's already implemented in water_level_estimator
__all__ = ['predict_water_level']