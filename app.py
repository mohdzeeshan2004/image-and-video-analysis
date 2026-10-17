from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

from preprocessing.video import get_video_metadata, extract_frames, extract_audio
from models.object_detection import detect_objects
from models.speech_recognition import transcribe_audio
from moderation.policy_engine import load_policy, evaluate_events
from moderation.evidence_fusion import build_events

st.set_page_config(page_title="Video Moderation Engine", page_icon="🎬", layout="wide")
st.title("🎬 Multimodal Video Content Moderation Engine")
st.caption("Portfolio prototype • Uploaded videos • India-first configurable policy profiles")

with st.sidebar:
    st.header("Analysis settings")
    country = st.selectbox("Destination policy", ["IN", "US", "BD", "CUSTOM"], index=0)
    sample_interval = st.slider("Frame sampling interval (seconds)", 1, 10, 3)
    run_object_detection = st.checkbox("Run pretrained object detection", value=True)
    run_transcription = st.checkbox("Transcribe audio (optional)", value=False)
    st.warning("This demo does not determine legal compliance. Findings are recommendations for review.")

uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "mkv", "avi", "webm"])

if uploaded:
    st.video(uploaded)
    st.write(f"**File:** {uploaded.name} · **Size:** {uploaded.size / (1024 * 1024):.2f} MB")
    if st.button("Analyze video", type="primary"):
        with tempfile.TemporaryDirectory(prefix="moderation_") as tmp:
            tmpdir = Path(tmp)
            suffix = Path(uploaded.name).suffix or ".mp4"
            video_path = tmpdir / f"input{suffix}"
            video_path.write_bytes(uploaded.getvalue())

            with st.status("Analyzing video…", expanded=True) as status:
                metadata = get_video_metadata(video_path)
                st.write("Video metadata extracted.")
                frames_dir = tmpdir / "frames"
                frames = extract_frames(video_path, frames_dir, sample_interval)
                st.write(f"Extracted {len(frames)} sampled frames.")
                audio_path = tmpdir / "audio.wav"
                audio_ok = extract_audio(video_path, audio_path)
                st.write("Audio extracted." if audio_ok else "Audio extraction unavailable.")

                detections = []
                if run_object_detection:
                    detections = detect_objects(frames)
                    st.write(f"Object detector returned {len(detections)} detections.")
                transcript_segments = []
                if run_transcription and audio_ok:
                    transcript_segments = transcribe_audio(audio_path)
                    st.write(f"Transcription returned {len(transcript_segments)} segments.")

                raw_events = build_events(detections, transcript_segments)
                policy = load_policy(country)
                decision = evaluate_events(raw_events, policy)
                status.update(label="Analysis complete", state="complete")

            st.subheader("Video metadata")
            st.json(metadata)

            col1, col2, col3 = st.columns(3)
            col1.metric("Frames sampled", len(frames))
            col2.metric("Visual detections", len(detections))
            col3.metric("Speech segments", len(transcript_segments))

            st.subheader("Publication recommendation")
            st.info(f"**{decision['decision'].replace('_', ' ').title()}**")
            st.write(decision["summary"])
            st.subheader("Evidence timeline")
            if raw_events:
                st.dataframe(raw_events, use_container_width=True)
            else:
                st.success("No configured categories were detected by the enabled baseline modules. This is not proof that the video is safe.")
            report = {
                "video": uploaded.name,
                "destination_country": country,
                "metadata": metadata,
                "events": raw_events,
                "decision": decision,
                "disclaimer": "Prototype result; not legal advice and not a guarantee of safe content."
            }
            st.download_button(
                "Download JSON report",
                data=json.dumps(report, indent=2, ensure_ascii=False),
                file_name="moderation_report.json",
                mime="application/json",
            )
            if detections:
                st.subheader("Sampled frame detections")
                st.dataframe(detections, use_container_width=True)
