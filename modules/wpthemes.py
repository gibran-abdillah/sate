from core.base_scan import BaseScan
from core.logger import get_logger

logger = get_logger(__name__)

class WPThemes(BaseScan):

    def __init__(self, url):
        self.url = url 
        self.type = 'themes'
        super().__init__()
    
def scan(url):
    w = WPThemes(url)
    return w.scan()    