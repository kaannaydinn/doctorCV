# agents/improver.py

import openai
from config import OPENAI_API_KEY
from utils.file_handler import extract_text_from_file
from utils.prompts import IMPROVEMENT_PROMPT

openai.api_key = OPENAI_API_KEY

def improve_cv(cv_path, analysis_summary):
    cv_text = extract_text_from_file(cv_path)
    if not cv_text:
        return "CV içeriği okunamadı."

    if not analysis_summary or len(analysis_summary.strip()) < 20:
        return "Analiz yetersiz veya eksik."

    prompt = IMPROVEMENT_PROMPT.format(cv=cv_text, analysis=analysis_summary)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen CV koçusun."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenAI API hatası: {e}"
