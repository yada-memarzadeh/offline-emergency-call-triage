import os
import whisper
from .config import AppConfig
from .io_utils import ensure_dirs

_MODEL = None

def _get_model(cfg: AppConfig):
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    ensure_dirs(cfg)
    os.environ["XDG_CACHE_HOME"] = cfg.model_cache

    _MODEL = whisper.load_model("tiny", device="cpu")
    return _MODEL

def transcribe(cfg: AppConfig, wav_path: str, language: str = None) -> str:
    model = _get_model(cfg)

    result = model.transcribe(
        wav_path,
        language=language,
        fp16=False
    )

    return result.get("text", "").strip()