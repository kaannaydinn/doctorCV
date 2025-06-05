
# agents/improver.py

import openai
from config import OPENAI_API_KEY
from utils.file_handler import extract_text_from_file

openai.api_key = OPENAI_API_KEY

def improve_cv(cv_path, analysis_summary, job_data=None, position="Pozisyon belirtilmedi", company="Şirket belirtilmedi", seniority=None, industry=None):
    """OpenAI ile sadece mevcut bilgilere dayalı CV yeniden yazımı"""

    cv_text = extract_text_from_file(cv_path)
    if not cv_text:
        return "⚠️ CV içeriği okunamadı."

    job_data_str = ", ".join(job_data.get("skills", [])) if job_data and job_data.get("skills") else "Veri bulunamadı"

    # Ek bağlamlar
    context_parts = []
    if seniority:
        context_parts.append(f"Kıdem seviyesi: {seniority}")
    if industry:
        context_parts.append(f"Sektör: {industry}")
    extra_context = "\n".join(context_parts)

    prompt = f"""
Below are a candidate's resume text, an analysis summary, and the actual skills required for the target position.

Your task is to:

Rewrite the CV using only the information the candidate already possesses
Improve the formatting (make it organized, clear, and impactful)
Reduce unnecessary repetition
Do not invent any new skills
Point out missing skills
Produce a text that expresses the candidate’s existing qualifications in the best possible way
--- CV METNİ ---
{cv_text}

--- ANALİZ ÖZETİ ---
{analysis_summary}

--- HEDEF POZİSYON ---
{position} @ {company}

--- BAĞLAM ---
{extra_context}

--- POZİSYONA AİT GERÇEK LINKEDIN BECERİLERİ ---
{job_data_str}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional CV Consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ OpenAI API hatası: {e}"
