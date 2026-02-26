# src/config.py

from dataclasses import dataclass  # این خط: ساخت کلاس تنظیمات ساده و تمیز

@dataclass(frozen=True)  # این خط: تنظیمات را immutable می‌کند (حرفه‌ای‌تر و خطاپذیری کمتر)
class AppConfig:  # این خط: یک جای واحد برای همه تنظیمات
    sample_rate: int = 16000  # این خط: نرخ نمونه‌برداری استاندارد (برای STT و پردازش صوت)
    max_audio_seconds: int = 60  # این خط: محدودیت زمان فایل برای جلوگیری از کندی/کرش
    temp_dir: str = ".cache"  # این خط: محل فایل‌های موقت پروژه
    model_cache: str = ".models"  # این خط: محل ذخیره مدل‌ها/دانلودها