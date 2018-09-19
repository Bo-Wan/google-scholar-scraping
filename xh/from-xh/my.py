from subprocess import call
import re
import time
import subprocess
import requests
import urllib.parse
import csv


proxy = ''
url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='


def getnewProxies():
    global proxy
    r = requests.get('https://gimmeproxy.com/api/getProxy')
    proxyResult = r.json()
    type = proxyResult['type']
    if type != 'http':
        getnewProxies()
    else:
        ip = proxyResult['curl']
        proxy = ip




firstline = True
with open('citation.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # Skip first line
    next(spamreader)
    for row in spamreader:
        if int(row[0]) <= 77:
            continue

        # Main logic
        id = row[0]
        journal = row[1]
        dates = row[2]
        title = row[3]
        author = row[4]

        print("Processing id: [" + id + "], title: [" + title + "]")

        parsedKey = urllib.parse.quote(title)
        url_key = parsedKey.replace("%20", "+")
        urlz = url_pre + url_key + url_post
        print("Parsed URL: " + url)

        handle = open('test.html', 'w')
        url = "curl " + urlz + " -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers' --proxy " + proxy
        out = subprocess.Popen(url, shell=True, stdout=handle)
        time.sleep(2)
        f = open('test.html', 'r')
        html = f.read()
        f.close()
        matches = re.findall(r'(?<=Cited by )([\d]+)', html)
        print("Match count: " + str(len(matches)))

        m = re.search(r'(?<=Cited by )([\d]+)', html)

        citation = 0
        if m:
            citation = m.group()
            print("#1 Cited By: " + citation)
            print('有')
        else:
            citation = -1
            print("no match (-1)")
            getnewProxies()
            print('没有')
