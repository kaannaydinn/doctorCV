
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
Aşağıda bir adayın özgeçmiş metni, bir analiz özeti, ve hedeflediği pozisyona ait gerçek beceriler yer alıyor.

Senin görevin:
- Bu CV'yi yalnızca adayın **zaten sahip olduğu** bilgilerle yeniden yazmak
- Biçimsel olarak iyileştirmek (düzenli, açık, etkileyici)
- Gereksiz tekrarları azaltmak
- Hiçbir yeni beceri uydurma
- Eksik becerileri belirtme
- Sadece adayın mevcut niteliklerini en iyi şekilde ifade eden bir metin üret

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
                {"role": "system", "content": "Sen profesyonel bir CV danışmanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ OpenAI API hatası: {e}"
