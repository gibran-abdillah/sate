import argparse

def get_parser():

    parser = argparse.ArgumentParser(description='SATE - Scanner Automation Tool Exploit for WordPress',
                                     usage='%(prog)s [-u URL | --web-list FILE] [--scan-plugins] | [--scan-themes]')
    parser.add_argument("-u", "--url", type=str, dest="url", help="URL to scan", metavar="http://target.com")
    parser.add_argument("-w", "--web-list", type=str, dest="web_list", help="Scan sites from txt file")
    parser.add_argument('--scan-plugins', action='store_true',dest="scan_plugins", help="Enable plugin scanning for vulnerabilities (recommended)")
    parser.add_argument('--scan-themes', action='store_true', dest="scan_themes", help="Enable theme scanning for vulnerabilities")
    
    parser.add_argument("--update-db", action="store_true", dest="update_db", help="Update Vulnerabilities Databse")

    return (
        parser, 
        parser.parse_args()
    )
