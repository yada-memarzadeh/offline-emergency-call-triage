# Deliverables – Emergency AI Project (Challenge 12 + 15)

## Project Overview
Offline AI system for:
- Emergency call prioritization (Challenge 12)
- Speaker status detection + emergency instruction generation (Challenge 15)

Fully CPU-based. No internet dependency.

---

## What is Implemented

- Speech-to-text (Whisper tiny, offline)
- Situation detection (rule-based NLP)
- Emotion detection
- Audio-based stress score (signal processing)
- Urgency fusion score (0–100)
- Priority level classification (LOW / MEDIUM / HIGH / CRITICAL)
- Batch call queue prioritization
- CSV export
- Explainability (keyword hits + scoring breakdown)
- Manual review flagging

---

## How to Run (Windows)

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py

---

## 60-Second Demo Script

1. Open "Call Queue (Batch)" tab
2. Upload 3 audio files
3. Show sorted priority ranking
4. Expand Top 3 calls
5. Download CSV report