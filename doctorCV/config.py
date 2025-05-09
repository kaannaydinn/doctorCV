import os

# Streamlit Cloud ortamı için en güvenilir yöntem
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Yerel geliştirme için fallback
if OPENAI_API_KEY is None:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    except:
        pass
