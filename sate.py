from utils.parser import get_parser
from modules.wpplugins import scan as scan_plugin
from modules.wpthemes import scan as scan_theme
from concurrent.futures import ThreadPoolExecutor
from utils.helpers import format_url, print_banner
from utils.update_db import download_and_clean

import random

def process(url, scan_methods):
    for method in scan_methods:
        method(format_url(url))

def bulk_process(web_list, scan_methods):
    with open(web_list, 'r') as file:
        urls = set([format_url(line) for line in file if line.strip()])

    with ThreadPoolExecutor(random.randint(10,20)) as worker:
        worker.map(lambda url: process(url, scan_methods), urls)

def main():
    
    (parser, args) = get_parser()

    print_banner()

    if args.update_db:
        return download_and_clean()
    if not any([args.web_list, args.url]) or not any([args.scan_plugins, args.scan_themes]):
        print('URL / Web list not set or you havent choose scanner')
        return parser.print_help()
    
    scan_methods = []

    if args.scan_plugins:
        scan_methods.append(scan_plugin)
    
    if args.scan_themes:
        scan_methods.append(scan_theme)
    
    if args.url:
        return process(args.url, scan_methods)
    
    if args.web_list:
        return bulk_process(args.web_list, scan_methods)
    
    
    

if __name__ == '__main__':
    main()