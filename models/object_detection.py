from __future__ import annotations

from pathlib import Path


def detect_objects(frames: list[dict], model_name: str = "yolov8n.pt") -> list[dict]:
    """
    Optional baseline object detector. The model detects common objects; it does NOT
    determine whether a video is violent or objectionable. First use may download weights.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        return [{
            "timestamp": f["timestamp"], "label": "object_detector_unavailable",
            "confidence": 0.0, "note": "Install ultralytics to enable object detection."
        } for f in []]

    model = YOLO(model_name)
    results_out = []
    for frame in frames:
        result = model.predict(source=frame["path"], verbose=False)[0]
        names = result.names
        if result.boxes is None:
            continue
        for box in result.boxes:
            cls_id = int(box.cls.item())
            confidence = float(box.conf.item())
            xyxy = [round(float(x), 2) for x in box.xyxy[0].tolist()]
            results_out.append({
                "timestamp": frame["timestamp"],
                "label": str(names.get(cls_id, cls_id)),
                "confidence": round(confidence, 4),
                "bbox_xyxy": xyxy,
                "model": model_name
            })
    return results_out
