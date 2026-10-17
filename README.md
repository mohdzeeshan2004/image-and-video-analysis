# AI-Powered Multimodal Video Content Moderation Engine

India-first portfolio prototype for pre-publication analysis of uploaded videos. It extracts frames and audio, runs baseline visual/audio analysis, and applies a configurable policy profile. It is a demo—not a legal compliance guarantee or a production moderation service.

## Features
- Streamlit upload interface
- FFmpeg/OpenCV video preprocessing
- Optional pretrained object detection using Ultralytics YOLO
- Optional speech transcription using faster-whisper
- Configurable policy rules in YAML
- Timestamped moderation events and JSON report export
- Clear separation between model detections and policy decisions

## Requirements
- Python 3.10–3.12 recommended
- FFmpeg installed and available on PATH
- Optional: GPU for faster model inference; CPU works more slowly
- Use only media you have permission to process

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Install FFmpeg separately and ensure `ffmpeg` and `ffprobe` are on PATH.

## Run
```powershell
streamlit run app.py
```
Upload an MP4/MOV/MKV file, choose destination country, then click **Analyze video**. Model weights may download the first time YOLO is used. Speech transcription is optional and can be slow on CPU.

## Project structure
- `app.py`: Streamlit interface
- `preprocessing/`: metadata, frames, audio extraction
- `models/`: optional object detection and speech transcription
- `moderation/`: evidence fusion and policy engine
- `config/policies/`: demonstration policy profiles
- `tests/`: unit tests
- `reports/`: generated reports (created at runtime)

## Important limitations
- Object detection is not violence detection. Detecting a knife does not establish that a scene is objectionable.
- The default policy is a demonstration configuration, not a statement of Indian law.
- The included baseline does not guarantee detection of violence, threats, explicit content, or policy violations.
- Transcription may be inaccurate, particularly with noisy audio, code-switching, accents, or unsupported languages.
- This version analyzes uploaded videos only; it does not publish to social platforms or moderate live streams.
- Review legal obligations, platform rules, data rights, retention, and privacy before real deployment.

## Suggested next steps
1. Add a rights-cleared, human-labelled evaluation dataset.
2. Evaluate precision, recall, false negatives, timestamp accuracy and review rate.
3. Add a dedicated violence/action classifier rather than relying on object labels.
4. Add PostgreSQL persistence and background jobs.
5. Introduce Kafka/PySpark only when workload and benchmarks justify distributed processing.
