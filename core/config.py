import time , os 


BASEPATH = os.getcwd()

SAVE_FORMAT = time.strftime('%Y-%m-%d.txt')
SAVE_FILE = os.path.join(BASEPATH, 'data', 'result', SAVE_FORMAT)

DB_FILE = os.path.join(BASEPATH, 'data', 'vuln.json')
LOG_LEVEL = 20
