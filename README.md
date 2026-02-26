# Offline Emergency Call Triage & Guidance (Challenge 12 + 15)

An **offline CPU-safe** AI system that:
1) **Prioritizes emergency calls** by urgency score (Challenge 12)
2) **Detects speaker status/emotion** and generates **context-aware emergency instructions** (Challenge 15)

## Key Features
- ✅ Offline on CPU (no internet dependency)
- ✅ Speech-to-text using Whisper (tiny)
- ✅ Situation & Emotion detection (explainable rules)
- ✅ Audio-based stress score (signal features)
- ✅ Urgency fusion score (0–100) + level (LOW/MED/HIGH/CRITICAL)
- ✅ Batch call queue prioritization + CSV export
- ✅ Explainability: keyword hits + scoring breakdown

## Architecture
**Audio → Clean (16k mono) → Whisper STT → Situation/Emotion → Stress (audio) → Urgency fusion → Instruction**

## How to Run (Windows)
```bash
cd D:\AIProjects\emergency_ai
.venv\Scripts\activate
python -m streamlit run app.py
