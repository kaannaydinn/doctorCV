# agents/analyzer.py

import openai
from config import OPENAI_API_KEY
from utils.file_handler import extract_text_from_file
from utils.prompts import ANALYSIS_PROMPT

openai.api_key = OPENAI_API_KEY

def analyze_cv(cv_path):
    """CV dosyasını analiz eder ve eksik yönleri döner."""

    cv_text = extract_text_from_file(cv_path)
    if not cv_text:
        return "⚠️ CV dosyası okunamadı veya boş."

    prompt = ANALYSIS_PROMPT.format(cv=cv_text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen deneyimli bir insan kaynakları uzmanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=750
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ OpenAI API hatası: {e}"
