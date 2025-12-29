from backend.services.video_processor import extract_frames
import sys

print("Testing frame extraction...", flush=True)
sys.stdout.flush()

paths = extract_frames('data/uploads/LSU-20200624-Label-2.mp4', max_frames=10)
print(f"\n=== RESULT ===", flush=True)
print(f"Number of frames: {len(paths)}", flush=True)
print(f"Frame paths: {paths}", flush=True)
