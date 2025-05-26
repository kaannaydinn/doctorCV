# utils/job_extractor.py

import os
import json
from typing import Optional

def load_job_data(company: str, position: str, location: str) -> Optional[dict]:
    file_name = f"{company.lower()}_{location.lower()}_{position.lower().replace(' ', '_')}.json"
    file_path = os.path.join("data", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def extract_company_block(job_description: str, target_company: str) -> Optional[str]:
    blocks = job_description.split("\n\n")
    for block in blocks:
        if target_company.lower() in block.lower():
            return block.strip()
    return None
