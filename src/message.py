# src/message.py

from __future__ import annotations

from .config import AppConfig

def generate_message(cfg: AppConfig, situation: str, emotion: str, urgency: int) -> str:
    if urgency >= 80:
        return (
            "CRITICAL: Stay calm. If trapped, conserve air, tap on pipes/walls, and share your exact location. "
            "If bleeding, apply firm pressure with cloth. Do not use elevators. Await rescue."
        )
    if urgency >= 60:
        return (
            "HIGH: Move to a safer area if possible. Check injuries, turn off gas/electricity if safe, "
            "and follow local emergency instructions."
        )
    if urgency >= 30:
        return (
            "MEDIUM: Avoid damaged structures. Keep phone battery, prepare essentials, and monitor official updates."
        )
    return "LOW: Remain alert. Stay away from unstable areas and be ready for aftershocks."