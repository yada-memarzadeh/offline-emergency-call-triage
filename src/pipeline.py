# src/pipeline.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from .config import AppConfig
from .audio_clean import clean_audio
from .stt import transcribe
from .nlp_situation import detect_situation
from .nlp_emotion import detect_emotion
from .urgency import compute_urgency, urgency_level
from .message import generate_message
from .audio_stress import compute_stress_score


@dataclass
class CallResult:
    filename: str
    transcript: str
    situation: str
    s_conf: float
    emotion: str
    e_conf: float
    stress: float
    urgency: int
    level: str
    instruction: str
    explain: Dict[str, Any]
    hits: Dict[str, Any]


def analyze_call(cfg: AppConfig, audio_path: str, filename: str) -> CallResult:
    clean_path = clean_audio(cfg, audio_path)
    transcript = transcribe(cfg, clean_path)

    situation, s_conf, s_hits = detect_situation(cfg, transcript)
    emotion, e_conf, e_hits = detect_emotion(cfg, transcript)

    stress = compute_stress_score(cfg, clean_path)
    urgency, explain = compute_urgency(cfg, situation, emotion, e_conf, stress_score=stress)
    level = urgency_level(urgency)

    instruction = generate_message(cfg, situation, emotion, urgency)

    return CallResult(
        filename=filename,
        transcript=transcript,
        situation=situation,
        s_conf=s_conf,
        emotion=emotion,
        e_conf=e_conf,
        stress=stress,
        urgency=urgency,
        level=level,
        instruction=instruction,
        explain=explain,
        hits={"situation_hits": s_hits, "emotion_hits": e_hits},
    )