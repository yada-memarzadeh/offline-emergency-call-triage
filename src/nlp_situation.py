# src/nlp_situation.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .config import AppConfig

@dataclass
class MatchResult:
    label: str
    confidence: float
    hits: Dict[str, List[str]]  # category -> matched keywords


# قوانین وضعیت (قابل توسعه)
SITUATION_RULES: Dict[str, List[str]] = {
    "TRAPPED": ["trapped", "under rubble", "can't move", "stuck", "buried"],
    "BLEEDING": ["bleeding", "blood", "cut", "wound"],
    "FIRE_SMOKE": ["fire", "smoke", "burning", "flames"],
    "COLLAPSE": ["collapsed", "building fell", "ruin", "falling debris"],
    "INJURY": ["injured", "hurt", "broken", "pain"],
}

SAFE_RULES = ["we are safe", "i'm safe", "no injuries", "safe now"]


def detect_situation(cfg: AppConfig, text: str) -> Tuple[str, float, Dict[str, List[str]]]:
    t = (text or "").lower().strip()

    hits: Dict[str, List[str]] = {}
    scores: Dict[str, int] = {}

    # SAFE check
    safe_hits = [k for k in SAFE_RULES if k in t]
    if safe_hits:
        return "SAFE", 0.70, {"SAFE": safe_hits}

    # match rules
    for label, kws in SITUATION_RULES.items():
        matched = [k for k in kws if k in t]
        if matched:
            hits[label] = matched
            scores[label] = len(matched)

    if not scores:
        return "UNKNOWN", 0.40, {}

    # choose best label by count of matched keywords
    best = max(scores, key=scores.get)
    raw = scores[best]

    # confidence: simple + explainable
    conf = min(0.95, 0.55 + 0.15 * raw)
    return best, conf, hits