import csv
import requests
import re
import urllib.parse
import pymysql
from random import randint
from time import sleep

# HTTP req and scraping
headers = {
    # Firefox
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'scholar.google.com.au',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0',
}

proxy_ip = '18.217.253.111'
http_proxy = 'http://' + proxy_ip + ':8889'
print('http_proxy = ' + http_proxy)


url = 'http://checkip.dyndns.org/'

# r = requests.get(url, headers)
r = requests.get(url,headers=headers,proxies = {'http': http_proxy},verify=False)

print("Http status: " + str(r.status_code))
print("HTML: " + r.text)
