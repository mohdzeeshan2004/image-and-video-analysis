from __future__ import annotations


def build_events(detections: list[dict], transcript_segments: list[dict]) -> list[dict]:
    """Convert raw model outputs into a common evidence timeline."""
    events = []
    for item in detections:
        label = str(item.get("label", "")).lower()
        # These labels indicate objects only. Do not infer violence from an object alone.
        category = "object_detected"
        events.append({
            "start_time": float(item.get("timestamp", 0)),
            "end_time": float(item.get("timestamp", 0)),
            "modality": "visual",
            "category": category,
            "label": label,
            "confidence": float(item.get("confidence", 0)),
            "evidence": item,
        })
    for item in transcript_segments:
        events.append({
            "start_time": float(item.get("start_time", 0)),
            "end_time": float(item.get("end_time", 0)),
            "modality": "audio_text",
            "category": "transcript_available",
            "label": item.get("text", ""),
            "confidence": None,
            "evidence": item,
        })
    return sorted(events, key=lambda e: e["start_time"])
