"""
Water Level Estimator using simple color-based water detection
"""
import cv2
import numpy as np


def detect_water_mask(frame):
    """
    Simple water detection using color thresholding
    
    Args:
        frame: BGR image
        
    Returns:
        mask: Binary mask where water is white (255)
    """
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Water typically appears in blue/gray tones
    # Adjust these ranges based on your videos
    lower_blue = np.array([90, 30, 30])
    upper_blue = np.array([130, 255, 255])
    
    # Also detect darker water (murky/muddy)
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 80])
    
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_dark = cv2.inRange(hsv, lower_dark, upper_dark)
    
    # Combine masks
    mask = cv2.bitwise_or(mask_blue, mask_dark)
    
    # Clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    return mask


def estimate_water_level_from_mask(frame, mask):
    """
    Estimate water level based on water mask
    
    Args:
        frame: Original BGR frame
        mask: Binary water mask
        
    Returns:
        water_level: Normalized water level (0.0 to 1.0)
    """
    h, w = mask.shape
    
    # Find the highest water point (smallest y coordinate)
    water_pixels = np.where(mask > 0)
    
    if len(water_pixels[0]) == 0:
        # No water detected
        return 0.0
    
    # Get the topmost water line
    water_top_y = np.min(water_pixels[0])
    
    # Normalize: water at bottom = 0, water at top = 1
    water_level = 1.0 - (water_top_y / h)
    
    # Also consider water coverage area
    water_area = np.sum(mask > 0) / (h * w)
    
    # Combine both metrics
    final_level = (water_level * 0.6) + (water_area * 0.4)
    
    return min(1.0, max(0.0, final_level))


def predict_water_level(frames):
    """
    Predict water level from video frames
    
    Args:
        frames: List of numpy arrays (BGR images)
        
    Returns:
        water_level: Average water level across all frames (0.0 to 1.0)
    """
    if not frames or len(frames) == 0:
        return 0.0
    
    water_levels = []
    
    for frame in frames:
        # Detect water in frame
        mask = detect_water_mask(frame)
        
        # Estimate water level
        level = estimate_water_level_from_mask(frame, mask)
        water_levels.append(level)
    
    # Return average water level
    avg_level = np.mean(water_levels)
    
    print(f"Detected water levels per frame: {water_levels}")
    print(f"Average water level: {avg_level:.3f}")
    
    return float(avg_level)
