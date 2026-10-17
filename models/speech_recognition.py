from __future__ import annotations

from pathlib import Path


def transcribe_audio(audio_path: str | Path, model_size: str = "base") -> list[dict]:
    """Optional Whisper-based transcription. Requires faster-whisper and may download weights."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return []

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), vad_filter=True)
    output = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            output.append({
                "start_time": round(float(segment.start), 3),
                "end_time": round(float(segment.end), 3),
                "text": text,
                "language": info.language,
                "model": f"faster-whisper-{model_size}"
            })
    return output
