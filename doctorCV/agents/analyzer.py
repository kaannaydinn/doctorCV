
# agents/analyzer.py

import openai
from config import OPENAI_API_KEY
from utils.file_handler import extract_text_from_file
from utils.prompts import CONTEXTUAL_ANALYSIS_PROMPT

openai.api_key = OPENAI_API_KEY

def analyze_cv(cv_path, job_data=None, position="Pozisyon belirtilmedi", company="Şirket belirtilmedi", seniority=None, industry=None):
    """CV analizini OpenAI ile gerçekleştirir, Apify verisiyle ve bağlamsal bilgilerle desteklenmiş şekilde"""

    cv_text = extract_text_from_file(cv_path)
    if not cv_text:
        return "⚠️ CV metni okunamadı."

    job_data_str = ", ".join(job_data.get("skills", [])) if job_data and job_data.get("skills") else "Veri bulunamadı"

    # Ek bağlamları dahil et
    context_parts = []
    if seniority:
        context_parts.append(f"Kıdem seviyesi: {seniority}")
    if industry:
        context_parts.append(f"Sektör: {industry}")
    extra_context = "\n".join(context_parts)

    prompt = CONTEXTUAL_ANALYSIS_PROMPT.format(
        cv=cv_text,
        position=position,
        company=company,
        job_data=job_data_str,
        extra_context=extra_context
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
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
