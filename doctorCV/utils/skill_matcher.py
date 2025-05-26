# utils/skill_matcher.py

import re
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def extract_skills_from_text(cv_text):
    """
    OpenAI API ile CV metninden teknik becerileri çıkartır.
    CV'nin yalnızca içeriğine dayanarak yazılım araçları, diller, veri teknolojileri gibi
    unsurları listeler.
    """
    if not isinstance(cv_text, str) or len(cv_text.strip()) < 30:
        return []

    prompt = f"""
Aşağıda bir adayın özgeçmiş metni bulunmaktadır. Bu özgeçmişten yalnızca teknik becerileri, yazılım araçlarını, programlama dillerini, veri teknolojilerini ve geliştirme ortamlarını çıkar.

- Sadece özgeçmiş içeriğine dayan, halüsinasyon yapma.
- Gereksiz açıklama ekleme, sadece liste üret.
- En sık ve dikkat çeken 10 beceriyi seç.
- Her becerinin yanında parantez içinde adayın bu beceriyi kullanma seviyesiyle ilgili kısa bir not ekle (örnek: "iyi", "temel", "ileri").

Format şu şekilde olmalı:
  - Python (ileri)
  - Excel (temel)
  - SQL (iyi)

CV METNİ:
{cv_text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen bir teknik insan kaynakları uzmanısın. Özgeçmişlerden teknik beceri çıkarımı yapıyorsun."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        output = response["choices"][0]["message"]["content"]

        lines = [
            re.sub(r"[\-\•●]\s*", "", line).strip()
            for line in output.strip().split("\n")
            if line.strip()
        ]

        return list(set(lines))

    except Exception as e:
        print(f"❌ OpenAI CV skill extraction hatası: {e}")
        return []

def compare_skills(cv_skills, reference_skills):
    """
    CV'deki becerilere göre eksik olanları döndürür.
    Eğer beceriler 'Python (iyi)' gibi geldiyse sadece skill ismini karşılaştırır.
    """
    def normalize(skill):
        return skill.split("(")[0].strip().lower()

    cv_set = set([normalize(s) for s in cv_skills])
    ref_set = set([normalize(s) for s in reference_skills])
    return sorted(list(ref_set - cv_set))

def extract_skills_from_job_description(description):
    """
    OpenAI API kullanarak iş ilanı açıklamasından en çok geçen teknik becerileri çıkarır.
    Liste madde halinde ve yüzdelik tahminli döner.
    """

    if isinstance(description, list):
        description = " ".join(str(x) for x in description if isinstance(x, str))

    if not isinstance(description, str) or len(description.strip()) < 30:
        return []

    prompt = f"""
Aşağıda, iş ilanı açıklamaları bulunmaktadır. Lütfen bu metne dayanarak yalnızca teknik becerileri, yazılım araçlarını, programlama dillerini ve teknolojileri çıkar.

- Yalnızca açıklamaya dayan. Tahmin yapma.
- En sık geçen 10 beceriyi listele.
- Her birinin yanında kaç ilanda geçtiğini yüzde olarak belirt (örnek: %75).
- Sadece madde listesi döndür.

İLAN AÇIKLAMASI:
{description}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen teknik işe alım uzmanısın. İş ilanlarından teknik beceriler ayıklıyorsun."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        output = response["choices"][0]["message"]["content"]

        lines = [
            re.sub(r"[\-\•●]\s*", "", line).strip()
            for line in output.strip().split("\n")
            if line.strip()
        ]

        return list(set(lines))

    except Exception as e:
        print(f"❌ OpenAI job_description skill extraction hatası: {e}")
        return []
