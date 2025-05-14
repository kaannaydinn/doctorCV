# utils/skill_matcher.py

import re
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def extract_skills_from_text(text):
    """CV metninden olası teknik becerileri çıkar (kelime temelli)"""
    text = text.lower()
    words = re.findall(r"\b[a-zA-ZöçşıüğÖÇŞİĞ0-9\+\#]+\b", text)
    return list(set(words))  # tekrarları at

def compare_skills(cv_skills, reference_skills):
    """Referans becerilere göre CV’de eksik olanları döndürür"""
    cv_set = set([s.lower() for s in cv_skills])
    ref_set = set([s.lower() for s in reference_skills])
    return sorted(list(ref_set - cv_set))

def extract_skills_from_job_description(description):
    """OpenAI ile job_description içinden teknik beceri listesi çıkarır"""

    if isinstance(description, list):
        description = " ".join(description)

    if not isinstance(description, str) or len(description.strip()) < 30:
        return []


    prompt = f"""
Aşağıdaki iş ilanı açıklamasından yalnızca teknik becerileri, araçları ve teknolojileri çıkar ve listele.
Sadece bir liste ver, açıklama yapma.

--- İlan Açıklaması ---
{description}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen teknik insan kaynakları uzmanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        output = response["choices"][0]["message"]["content"]
        lines = [line.strip("•- ").strip() for line in output.strip().split("\n") if line.strip()]
        return list(set(lines))

    except Exception as e:
        print(f"❌ OpenAI skill extraction hatası: {e}")
        return []
