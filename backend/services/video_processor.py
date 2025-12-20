import os 
from werkzeug.utils import secure_filename 
import cv2
import numpy as np

UPLOAD_FOLDER = "data/uploads"
FRAME_FOLDER = "static/frames"
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_video(video_file):
    if not allowed_file(video_file.filename):
        raise ValueError("Unsupported file format")
    
    filename = secure_filename(video_file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    video_file.save(save_path)

    return save_path


def cvt_video_to_frames(video_path, out_frames_dir, stride=3):
    """
    Convert video to frames (from V-FloodNet)
    
    Args:
        video_path: Path to video file
        out_frames_dir: Output directory for frames
        stride: Extract every Nth frame (default: 3)
    
    Returns:
        List of frame paths
    """
    os.makedirs(out_frames_dir, exist_ok=True)
    
    video = cv2.VideoCapture(video_path)
    cnt = 0
    frame_paths = []

    print(f"Converting video to frames: {video_path}")
    print(f"Output directory: {out_frames_dir}")
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        if cnt % stride == 0:
            out_filename = f'{cnt:05}.jpg'
            out_path = os.path.join(out_frames_dir, out_filename)
            cv2.imwrite(out_path, frame)
            frame_paths.append(out_path)

        cnt += 1

    video.release()
    print(f'Extracted {len(frame_paths)} frames from total {cnt} frames')
    
    return frame_paths


def extract_frames(video_path, max_frames=10, save_frames=True):
    """
    Extract frames from video for display in web UI
    
    Args:
        video_path: Path to the video file
        max_frames: Maximum number of frames to extract
        save_frames: Whether to save frames as images
        
    Returns:
        List of frame paths for web display (relative to static folder)
    """
    try:
        print(f"=== Extracting frames for display: {video_path} ===")
        
        # Get video name for folder
        video_basename = os.path.splitext(os.path.basename(video_path))[0]
        frame_dir = os.path.join(FRAME_FOLDER, video_basename)
        
        # Convert video to frames using V-FloodNet method
        stride = 5  # Extract every 5th frame
        all_frame_paths = cvt_video_to_frames(video_path, frame_dir, stride=stride)
        
        # Select evenly distributed frames up to max_frames
        if len(all_frame_paths) > max_frames:
            indices = np.linspace(0, len(all_frame_paths) - 1, max_frames, dtype=int)
            selected_paths = [all_frame_paths[i] for i in indices]
        else:
            selected_paths = all_frame_paths
        
        # Convert to relative paths for Flask static files
        # Template expects: filename='frames/video_name/00001.jpg'
        relative_paths = []
        for path in selected_paths:
            # Normalize path separators to forward slashes
            path = path.replace('\\', '/')
            
            # Extract just the 'video_name/filename.jpg' part after 'frames/'
            if 'frames/' in path:
                rel_path = path.split('frames/')[1]  # e.g., 'video_name/00001.jpg'
                relative_paths.append(rel_path)
                print(f"Frame path: frames/{rel_path}")
            else:
                print(f"Warning: 'frames/' not found in path: {path}")
        
        print(f"Selected {len(relative_paths)} frames for display")
        return relative_paths
        
    except Exception as e:
        print(f"ERROR extracting frames: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


def get_frames_for_prediction(video_path, stride=3):
    """
    Extract frames as numpy arrays for prediction
    Uses V-FloodNet's video-to-frames approach
    
    Args:
        video_path: Path to video file
        stride: Extract every Nth frame
        
    Returns:
        List of numpy arrays (BGR images)
    """
    try:
        print(f"=== Extracting frames for prediction: {video_path} ===")
        
        frames = []
        video = cv2.VideoCapture(video_path)
        
        if not video.isOpened():
            print(f"ERROR: Could not open video: {video_path}")
            return frames
        
        cnt = 0
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            if cnt % stride == 0:
                frames.append(frame)

            cnt += 1
            
            # Limit to avoid memory issues
            if len(frames) >= 50:
                break

        video.release()
        print(f'Extracted {len(frames)} frames for prediction (from {cnt} total frames)')
        
        return frames
        
    except Exception as e:
        print(f"ERROR in get_frames_for_prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return []