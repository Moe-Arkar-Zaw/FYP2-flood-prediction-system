import cv2
import numpy as np
from backend.services.flood_predictor import predict_water_level

# Load a test frame
frame_path = 'static/frames/LSU-20200624-Label-2/00000.jpg'
frame = cv2.imread(frame_path)

if frame is None:
    print(f"ERROR: Could not load frame from {frame_path}")
else:
    print(f"Loaded frame: {frame.shape}")
    
    # Test with single frame
    frames = [frame]
    
    print("\nRunning water level prediction...")
    water_level = predict_water_level(frames)
    
    print(f"\n=== RESULT ===")
    print(f"Water level: {water_level:.3f}")
    
    # Determine severity
    if water_level < 0.3:
        severity = 'normal'
    elif water_level < 0.6:
        severity = 'alert'
    else:
        severity = 'severe'
    
    print(f"Severity: {severity}")
