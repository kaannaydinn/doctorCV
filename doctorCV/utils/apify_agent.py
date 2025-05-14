# utils/apify_agent.py

import os
import json
from apify_client import ApifyClient
from config import APIFY_API_TOKEN

def fetch_linkedin_data(job_title, company_name=None, location="Türkiye"):
    """
    Pozisyon ve ülkeye göre Apify'dan LinkedIn verisi çeker.
    Veriler önceden çekildiyse cache'den okur.
    """

    if not APIFY_API_TOKEN:
        print("❌ APIFY_API_TOKEN eksik.")
        return {"job_description": []}

    # Dosya adlandırması (şirket opsiyonel)
    base_name = f"{job_title.lower().replace(' ', '_')}_{location.lower().replace(' ', '_')}"
    filename = f"{base_name}.json"
    filepath = os.path.join("data", filename)

    # Eğer daha önce çekildiyse cache'den oku
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            print(f"📁 Apify cache'den okundu: {filename}")
            return json.load(f)

    # Aktörü başlat
    try:
        client = ApifyClient(APIFY_API_TOKEN)
        run_input = {
            "job_title": job_title,
            "location": location,
        }

        print("🌐 Apify aktörü çalıştırılıyor...")
        run = client.actor("JkfTWxtpgfvcRQn3p").call(run_input=run_input)

        # Çıktıları veri kümesinden al
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

        # 'skills' alanını ayıkla
        job_description = []
        for item in dataset_items:
            job_description.extend(item.get("job_description", []))

        extracted = {
            "job_description": list(sorted(set(job_description)))
        }

        # Cache olarak kaydet
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(extracted, f, ensure_ascii=False, indent=2)

        print(f"✅ Apify verisi kaydedildi: {filename}")
        return extracted

    except Exception as e:
        print(f"❌ Apify aktör hatası: {e}")
        return {"skills": []}
