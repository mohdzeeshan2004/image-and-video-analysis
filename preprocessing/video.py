from __future__ import annotations

import subprocess
from pathlib import Path
import cv2


def get_video_metadata(video_path: str | Path) -> dict:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError("Could not open video. Check that the file is valid and FFmpeg/codecs are installed.")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    duration = frame_count / fps if fps > 0 else None
    return {
        "fps": round(fps, 3),
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration_seconds": round(duration, 3) if duration is not None else None,
    }


def extract_frames(video_path: str | Path, output_dir: str | Path, interval_seconds: int = 3) -> list[dict]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError("Could not open video.")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
    if fps <= 0:
        cap.release()
        raise ValueError("Video FPS is unavailable.")
    stride = max(1, int(fps * interval_seconds))
    frames, index = [], 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if index % stride == 0:
            timestamp = index / fps
            path = output_dir / f"frame_{timestamp:09.3f}.jpg"
            if cv2.imwrite(str(path), frame):
                frames.append({"timestamp": round(timestamp, 3), "path": str(path)})
        index += 1
    cap.release()
    return frames


def extract_audio(video_path: str | Path, output_path: str | Path) -> bool:
    """Extract mono 16 kHz WAV using FFmpeg. Returns False if extraction fails/no audio."""
    command = [
        "ffmpeg", "-y", "-i", str(video_path), "-vn", "-ac", "1",
        "-ar", "16000", "-acodec", "pcm_s16le", str(output_path)
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=600)
        return result.returncode == 0 and Path(output_path).exists() and Path(output_path).stat().st_size > 44
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
