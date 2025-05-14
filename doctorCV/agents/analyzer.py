# agents/analyzer.py

import openai
from config import OPENAI_API_KEY
from utils.file_handler import extract_text_from_file
from utils.prompts import CONTEXTUAL_ANALYSIS_PROMPT

openai.api_key = OPENAI_API_KEY

def analyze_cv(cv_path, job_data=None, position="Pozisyon belirtilmedi", company="Şirket belirtilmedi"):
    """CV analizini OpenAI ile gerçekleştirir, Apify verisiyle desteklenmiş şekilde"""

    cv_text = extract_text_from_file(cv_path)
    if not cv_text:
        return "⚠️ CV metni okunamadı."

    job_data_str = ", ".join(job_data.get("skills", [])) if job_data else "Veri bulunamadı"

    prompt = CONTEXTUAL_ANALYSIS_PROMPT.format(
        cv=cv_text,
        position=position,
        company=company,
        job_data=job_data_str
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen deneyimli bir insan kaynakları uzmanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ OpenAI API hatası: {e}"
