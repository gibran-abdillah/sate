from urllib.parse import urlparse
from core import config
from colorama import Fore, Style


def format_url(url):
    url = url.strip().rstrip().strip('/')
    if '://' not in url:
        return f'http://{url}'
    return url 

def write_result(url, software_type, slug, cvss, title, references):
    with open(config.SAVE_FILE,'a') as writer:
        writer.write(f'{url}|{software_type}|{slug}|{title}|cvss score: {cvss}|{references}\n')

def color_cvss(cvss_score):
    try:
        score = float(cvss_score)
    except ValueError:
        return cvss_score  # Kalau gak bisa di-cast, return as-is

    if score == 0.0:
        color = Fore.LIGHTBLACK_EX
    elif score <= 3.9:
        color = Fore.BLUE
    elif score <= 6.9:
        color = Fore.YELLOW
    elif score <= 8.9:
        color = Fore.LIGHTMAGENTA_EX
    else:
        color = Fore.LIGHTRED_EX

    return f"{color}{score}{Style.RESET_ALL}"
def print_banner():

    banner = f"""
    {Fore.RED}
\t.d8888.  .d8b.  d888888b d88888b 
\t88'  YP d8' `8b `~~88~~' 88'     
\t`8bo.   88ooo88    88    88ooooo 
\t  `Y8b. 88~~~88    88    88~~~~~ 
\tdb   8D 88   88    88    88.     
\t`8888Y' YP   YP    YP    Y88888P 
                                 
                                 

    {Style.RESET_ALL}
            {Fore.YELLOW}SATE - Scanner Automation Tool for wordprEss
                Target: WordPress only 🔍
    {Style.RESET_ALL}
    """

    print(banner)
