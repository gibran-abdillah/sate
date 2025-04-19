from core.base_scan import BaseScan
from core.logger import get_logger

logger = get_logger(__name__)

class WPPlugins(BaseScan):

    def __init__(self, url):
        self.url = url 
        self.type = 'plugins'
        super().__init__()
    


def scan(url):
    w = WPPlugins(url)
    return w.scan()    