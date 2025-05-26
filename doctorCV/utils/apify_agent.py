
import os
import json
from apify_client import ApifyClient
from config import APIFY_API_TOKEN

def fetch_linkedin_data(job_title, company_name=None, location="Türkiye", seniority_level=None, industries=None, job_function=None):
    if not APIFY_API_TOKEN:
        print("❌ APIFY_API_TOKEN eksik.")
        return {"job_description": ""}

    # Dosya adı
    base_name = f"{job_title.lower().replace(' ', '_')}_{location.lower().replace(' ', '_')}"
    filename = f"{base_name}.json"
    filepath = os.path.join("data", filename)

    # Cache kontrolü
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            print(f"📁 Apify cache'den okundu: {filename}")
            return json.load(f)

    try:
        client = ApifyClient(APIFY_API_TOKEN)

        run_input = {
            "job_title": job_title,
            "location": location,
            "jobs_entries": 100,
            "start_jobs": 0,
        }

        if company_name:
            run_input["company_name"] = company_name
        if seniority_level:
            run_input["seniority_level"] = seniority_level
        if industries:
            run_input["industries"] = industries
        if job_function:
            run_input["job_function"] = job_function

        print("🌐 Apify aktörü çalıştırılıyor...")
        run = client.actor("JkfTWxtpgfvcRQn3p").call(run_input=run_input)

        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

        cleaned_descriptions = []
        for item in dataset_items:
            desc = item.get("description") or item.get("job_description") or ""
            if isinstance(desc, list):
                desc = " ".join(str(x) for x in desc if isinstance(x, str))
            if not isinstance(desc, str) or len(desc.strip()) < 30:
                continue
            cleaned_descriptions.append(desc.strip())

        combined = "\n\n".join(cleaned_descriptions[:10])

        extracted = {
            "job_description": combined
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(extracted, f, ensure_ascii=False, indent=2)

        print(f"✅ Apify verisi kaydedildi: {filename}")
        return extracted

    except Exception as e:
        print(f"❌ Apify aktör hatası: {e}")
        return {"job_description": ""}
