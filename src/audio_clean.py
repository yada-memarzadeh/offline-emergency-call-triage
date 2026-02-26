import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from .config import AppConfig
from .io_utils import ensure_dirs

def clean_audio(cfg: AppConfig, input_path: str) -> str:
    ensure_dirs(cfg)

    y, sr = librosa.load(input_path, sr=cfg.sample_rate, mono=True)

    max_len = int(cfg.sample_rate * cfg.max_audio_seconds)
    if len(y) > max_len:
        y = y[:max_len]

    peak = float(np.max(np.abs(y)) + 1e-9)
    y = (y / peak) * 0.95
    y = y.astype(np.float32)

    out_path = str(Path(cfg.temp_dir) / (Path(input_path).stem + ".clean.wav"))
    sf.write(out_path, y, cfg.sample_rate, subtype="PCM_16")

    return out_path