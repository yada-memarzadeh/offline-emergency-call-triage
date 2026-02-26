# src/nlp_emotion.py

from __future__ import annotations

from typing import Dict, List, Tuple

from .config import AppConfig

EMOTION_RULES: Dict[str, List[str]] = {
    "PANIC": ["help!", "please", "panic", "terrified", "emergency", "immediately"],
    "FEAR": ["scared", "afraid", "fear", "worried", "shaking"],
    "CALM": ["calm", "okay", "fine", "under control"],
}

NEGATIONS = ["not", "don't", "do not", "no"]


def detect_emotion(cfg: AppConfig, text: str) -> Tuple[str, float, Dict[str, List[str]]]:
    t = (text or "").lower().strip()

    hits: Dict[str, List[str]] = {}
    scores: Dict[str, int] = {}

    for label, kws in EMOTION_RULES.items():
        matched = [k for k in kws if k in t]
        if matched:
            hits[label] = matched
            scores[label] = len(matched)

    if not scores:
        return "NEUTRAL", 0.55, {}

    best = max(scores, key=scores.get)
    raw = scores[best]
    conf = min(0.95, 0.60 + 0.12 * raw)
    return best, conf, hits