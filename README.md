# Introduction

This code sample demonstrates how to convert a video to text using FFmpeg and the OpenAI Whisper model. If no GPU is available, the CPU will be used, but transcription will be slower."

# Installation
- Setup virtual environment: ```python -m venv .venv```
- Active virtual environment: ```source .venv/bin/activate```
- Setup libraries: ```pip install -r requirements.txt```
- Ceate three folders: ```mkdir audio_output samples_videos transcript```

# How to use
- To convert video files to audio, see [video_to_audio.py](video_to_audio.py)
- To use OpenAI Whisper Model, see [transcript.py](transcript.py)