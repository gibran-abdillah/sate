import json 
from packaging.version import Version
from utils.update_db import download_db, db_clean
import os 

if not os.path.exists('data/cleaned.json'):
    if not os.path.exists('data/vulnerabilities.production.json'):
        download_db()
        db_clean()
    else:
        print('[+] cleaning ')
        db_clean()
    
with open('data/cleaned.json','r') as file:
    vuln_db = json.load(file)

def validator(software_type, slug, version):
    data = vuln_db.get(software_type) or False 
    if not data:
        return False 
    
    items = data.get(slug)
    current_version = Version(version)

    for item in items:
        from_version = Version(item['from_version'])
        to_version = Version(item['to_version'])

        if from_version <= current_version < to_version:
            return item


