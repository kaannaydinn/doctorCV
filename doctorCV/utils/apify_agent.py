
import os
import json
from apify_client import ApifyClient
from config import APIFY_API_TOKEN

def fetch_linkedin_data(job_title, company_name=None, location="Türkiye"):
    if not APIFY_API_TOKEN:
        print("❌ APIFY_API_TOKEN eksik.")
        return {"job_description": "", "all_jobs": []}

    base_name = f"{job_title.lower().replace(' ', '_')}_{location.lower().replace(' ', '_')}"
    filename = f"{base_name}.json"
    filepath = os.path.join("data", filename)

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
            "start_jobs": 0
        }

        print(f"🌐 Apify aktörü çalıştırılıyor: {job_title} @ {location}")
        run = client.actor("JkfTWxtpgfvcRQn3p").call(run_input=run_input)

        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

        all_descriptions = []
        for item in dataset_items:
            company = item.get("company_name", "").strip()  # fixed key
            title = item.get("title", "").strip()
            desc = item.get("job_description", "").strip()
            print(f"🔍 {title} @ {company} | Desc len: {len(desc)}")

            if not desc:
                continue

            all_descriptions.append({
                "company_name": company,
                "title": title,
                "description": desc
            })

        extracted = {
            "job_description": "\n\n".join([entry["description"] for entry in all_descriptions[:10]]),
            "all_jobs": all_descriptions
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(extracted, f, ensure_ascii=False, indent=2)

        print(f"✅ Apify verisi kaydedildi: {filename}")
        return extracted

    except Exception as e:
        print(f"❌ Apify aktör hatası: {e}")
        return {"job_description": "", "all_jobs": []}
