import requests
import json , os 
from core import config
def db_clean():

    with open(config.DB_FILE,"r", errors='ignore') as file:

        contents = json.load(file)
        
        plugins = {}
        themes = {}

        for id_vulnerability in contents:
            tmp_data = {}
            data = contents[id_vulnerability]
            
            title = data.get('title')
            cvss_score = data.get('cvss').get('score')
            references = "\n".join(data.get('references',['NO REFERENCES']))
            _software = data['software']
            
            # get information from software object json 
            _software_information = _software[0]
            _software_type = _software_information['type']
            _software_slug = _software_information['slug']
            affected_versions = _software_information['affected_versions']
            
            
            for version in affected_versions:
                from_version = affected_versions[version]['from_version']
                to_version = affected_versions[version]['to_version']

                if from_version.strip() == '*':
                    from_version = "0"
                
                tmp_data['from_version'] = from_version
                tmp_data['to_version'] = to_version
            
            tmp_data['title'] = title 
            tmp_data['cvss'] = cvss_score
            tmp_data['references'] = references

            if _software_type == 'plugin':
                to_add = plugins
            elif _software_type == 'themes':
                to_add = themes
            
            if not to_add.get(_software_slug):
                to_add[_software_slug] = [tmp_data]
            else:
                to_add[_software_slug].append(tmp_data)
    
    with open('data/cleaned.json','w') as writer:

        combined = {
            "plugins":plugins, 
            "themes":themes
        }
        combined = json.dumps(combined, indent=4)
        writer.write(combined)

def download_db():
    download_url = "https://www.wordfence.com//api/intelligence/v2/vulnerabilities/production"

    try:
        print('[+] Downloading the database....')
        response = requests.get(download_url, timeout=15)
        response.raise_for_status() 


        os.makedirs(os.path.dirname(config.DB_FILE), exist_ok=True)

        with open(config.DB_FILE, 'w', encoding='utf-8') as f:
            f.write(response.text)

        print(f"[✓] Vulnerability DB downloaded and saved to: {config.DB_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to download DB: {e}")

def download_and_clean():
    download_db()
    return db_clean()
