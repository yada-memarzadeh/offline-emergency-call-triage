# src/audio_stress.py

from __future__ import annotations

import numpy as np
import librosa

from .config import AppConfig


def compute_stress_score(cfg: AppConfig, wav_path: str) -> float:
    """
    Simple explainable stress proxy from audio:
    - RMS energy (loudness)
    - Zero-crossing rate (roughness)
    - Spectral centroid (sharpness)
    Output: 0..100
    """
    y, sr = librosa.load(wav_path, sr=cfg.sample_rate, mono=True)

    if len(y) < sr * 0.5:
        return 30.0

    rms = float(np.mean(librosa.feature.rms(y=y)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))

    # Normalize each feature to 0..1 (rough heuristic ranges; stable & explainable)
    rms_n = min(1.0, rms / 0.12)          # typical speech rms ~0.03..0.12
    zcr_n = min(1.0, zcr / 0.12)          # typical zcr ~0.02..0.10
    cen_n = min(1.0, centroid / 3000.0)   # speech centroid often < 3000

    score_0_1 = 0.50 * rms_n + 0.25 * zcr_n + 0.25 * cen_n
    return float(round(score_0_1 * 100.0, 2))