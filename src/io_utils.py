# src/io_utils.py

import os  # برای کار با مسیرها
import tempfile  # برای ساخت فایل موقت امن
from pathlib import Path  # مسیرها را تمیزتر مدیریت می‌کند

from .config import AppConfig  # تنظیمات پروژه را می‌خوانیم

def ensure_dirs(cfg: AppConfig) -> None:  # تابع: پوشه‌های لازم را می‌سازد
    Path(cfg.temp_dir).mkdir(parents=True, exist_ok=True)  # این خط: ساخت cache اگر نبود
    Path(cfg.model_cache).mkdir(parents=True, exist_ok=True)  # این خط: ساخت محل مدل‌ها

def save_bytes_to_temp(cfg: AppConfig, data: bytes, suffix: str) -> str:  # تابع: بایت‌ها را به فایل temp می‌نویسد
    ensure_dirs(cfg)  # این خط: مطمئن می‌شود پوشه‌ها وجود دارند
    with tempfile.NamedTemporaryFile(delete=False, dir=cfg.temp_dir, suffix=suffix) as f:  # این خط: ساخت فایل temp امن
        f.write(data)  # این خط: نوشتن فایل
        return f.name  # این خط: مسیر فایل را برمی‌گرداند

def safe_remove(path: str) -> None:  # تابع: حذف امن فایل
    try:  # این خط: جلوگیری از کرش
        if path and os.path.exists(path):  # این خط: اگر فایل وجود داشت
            os.remove(path)  # این خط: حذف فایل
    except Exception:  # این خط: اگر حذف خطا داد
        pass  # این خط: بی‌خیال (نباید برنامه بخاطر حذف فایل کرش کند)