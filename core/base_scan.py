import requests
import re
import random 
import time
from core.logger import get_logger
from core.validator import validator
from utils.helpers import write_result, color_cvss


logger = get_logger(__name__)

class BaseSession(requests.Session):
    def __init__(self, timeout=10):
        super().__init__()
        self._timeout = timeout

    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', self._timeout)
        return super().request(*args, **kwargs)
    
class BaseScan:

    def __init__(self):
        self.session = BaseSession(timeout=random.randint(5,7))
        self.session.headers['User-Agents'] = random.choice(open('data/user-agents.txt','rb').readlines()).rstrip()
        self.session.headers['wordpress_test_cookie'] = 'WP Cookie check'
        
        self.plugins = set()
        self.themes = set()

        self.init()
        
        time.sleep(random.uniform(0.4,0.9))

    
    
    def getResponse(self, path='/'):
        if not self.url:
            raise ValueError("URL not set")
        
        full_url = f'{self.url}/{path}'.strip('/')
        response =  self.session.get(full_url)
        return response
    
    def get_software_version(self, slug):
        if not self.type:
            raise ValueError("self.type not set")
        
        if self.type == 'plugins':
            version_url = f'/wp-content/plugins/{slug}/readme.txt'
            validator_function = self.get_plugin_version
        elif self.type == 'themes':
            version_url = f'/wp-content/themes/{slug}/style.css'
            validator_function = self.get_theme_version
        
        if version_url and validator_function:
            version = validator_function(slug)
            return version
    
    def scan(self):
        try:
            vuln_list = set()
            if self.type == 'plugins':
                data = self.plugins 
            elif self.type == 'themes':
                data = self.themes
            else:
                logger.error(f'DATA NOT SET {self.url}')
                return False 
            
            if not data:
                return False 
            
            max_try = 3
            have_try = 0
            for slug in data:
                version = self.get_software_version(slug)
                
                if have_try >= 3:
                    logger.error(f'Reached {max_try} to get {self.type} version - {self.url}')
                    return False 
                

                if not version:
                    have_try += 1
                    logger.debug(f'can not get {self.type} version ({slug}) {self.url}')
                    continue
                
                result = validator(self.type, slug, version)
                if not result:
                    logger.debug(f'not vulnerable {slug} - {version} {self.url}')
                    continue

                vuln_list.add(slug)
                cvss = result.get('cvss')
                title = result.get('title')
                references = result.get('references')
                logger.critical(f'VULNERABLE ({self.url}) ({slug}) {version}  [{title}] - {color_cvss(cvss)}')
                write_result(
                    self.url,
                    self.type,
                    slug,
                    cvss, 
                    title,
                    references
                )
            
            if not vuln_list:
                logger.error(f'NOTHING FOUND {self.type} {self.url}')

        except requests.exceptions.RequestException:
            logger.error(f"RequestException {self.url}")
    
    def get_theme_version(self, slug):
        style_path = f'/wp-content/themes/{slug}/style.css'
        response = self.getResponse(style_path)
        if response.status_code != 200:
            return False 
    
    def _parse_theme_version(self, txt: str):
        lines = txt.strip().splitlines()
        for line in lines:
            line = line.lower()
            if 'version:' in line:
                return line.split(':')[-1].strip()
            
    def get_plugin_version(self, slug):
        readme_txt = f'/wp-content/plugins/{slug}/readme.txt'
        response = self.getResponse(readme_txt)
        if response.status_code != 200:
            return False 
        return self._parse_plugin_version(response.text)
    
    def _parse_plugin_version(self, txt: str):
        lines = txt.strip().splitlines()
        for line in lines:
            line = line.lower()
            if 'stable tag' in line:
                return line.split(':')[-1].strip()
        
        return False
    
    def init(self):
        response = self.getResponse()
        pattern = r'wp-content/(plugins|themes)/([\w\-\.]+)'
        matches = re.findall(pattern, response.text)
        
        if not matches:
            logger.error(f'Can not get themes/plugins {self.url}')
            return False 
        
        for matched in matches:
            if not matched or len(matched) != 2:
                continue
            software_type, slug = matched
            if software_type == 'plugins':
                self.plugins.add(slug)
            elif software_type == 'themes':
                self.themes.add(slug)
        
        logger.info(f'Get total {len(self.plugins)} plugins and {len(self.themes)} in {self.url}')
        

        return True 

    
        
    
    
