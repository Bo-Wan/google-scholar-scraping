from subprocess import call
import re
import time
import subprocess
import requests
import urllib.parse
import csv


global proxy
url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='



r = requests.get('https://gimmeproxy.com/api/getProxy')
proxyResult = r.json()
type = proxyResult['type']
if type != 'http':
    print('no proxy')
else:
    ip = proxyResult['curl']
    proxy = ip
    print(proxy)
