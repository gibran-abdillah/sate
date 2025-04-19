import logging 
from colorama import Fore, Back, Style
from .config import LOG_LEVEL

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.CYAN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.LIGHTGREEN_EX + Style.BRIGHT
    }

    def format(self, record):
        original_levelname = record.levelname

        if original_levelname in self.COLORS:
            if original_levelname == "CRITICAL":
                display_name = "FOUND\t"
            else:
                display_name = original_levelname
            colored_levelname = f"{self.COLORS[original_levelname]}{display_name}{Style.RESET_ALL}"
            if original_levelname != "CRITICAL":
                colored_levelname += '\t'
            record.levelname = colored_levelname


        result = super().format(record)

        record.levelname = original_levelname
        return result
    
def get_logger(name=__name__):
    
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    formatter = ColorFormatter('%(asctime)s\t%(levelname)s: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger
