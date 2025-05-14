# config.py

import os

# Streamlit Cloud, Docker, Production ortamları için
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN")

# Lokal geliştirme için .env dosyasından oku
if not OPENAI_API_KEY or not APIFY_API_TOKEN:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        APIFY_API_TOKEN = APIFY_API_TOKEN or os.getenv("APIFY_API_TOKEN")
    except Exception as e:
        print("❌ .env dosyası yüklenemedi:", e)
