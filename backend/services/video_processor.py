import os 
from werkzeug.utils import secure_filename 
import random 

UPLOAD_FOLDER = "data/uploads"
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

def extract_frames(video_path):
    # Dummy 5 frames first
    frames = [f"frame_{i}" for i in range(5)]
    return frames