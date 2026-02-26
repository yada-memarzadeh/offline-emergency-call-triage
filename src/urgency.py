# src/urgency.py

from __future__ import annotations

from typing import Dict, Tuple

from .config import AppConfig

SITUATION_WEIGHT = {
    "TRAPPED": 45,
    "FIRE_SMOKE": 40,
    "BLEEDING": 35,
    "COLLAPSE": 30,
    "INJURY": 22,
    "SAFE": -10,
    "UNKNOWN": 0,
}

EMOTION_WEIGHT = {
    "PANIC": 20,
    "FEAR": 12,
    "CALM": -5,
    "NEUTRAL": 0,
}

def compute_urgency(
    cfg: AppConfig,
    situation: str,
    emotion: str,
    emotion_conf: float,
    stress_score: float = 30.0
) -> Tuple[int, Dict[str, float]]:
    base = 10.0

    s_w = float(SITUATION_WEIGHT.get(situation, 0))
    e_w = float(EMOTION_WEIGHT.get(emotion, 0))

    # emotion confidence gates emotion weight (explainable)
    e_term = e_w * float(max(0.0, min(1.0, emotion_conf)))

    # stress contributes up to +25
    stress_term = (max(0.0, min(100.0, stress_score)) / 100.0) * 25.0

    score = base + s_w + e_term + stress_term
    score = int(max(0, min(100, round(score))))

    explain = {
        "base": base,
        "situation_weight": s_w,
        "emotion_weight": e_w,
        "emotion_confidence": float(emotion_conf),
        "emotion_term": e_term,
        "stress_score": float(stress_score),
        "stress_term": stress_term,
    }
    return score, explain


def urgency_level(score: int) -> str:
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"