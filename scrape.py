import csv
import requests
import re
import urllib.parse
import pymysql
from random import randint
from time import sleep

# HTTP req and scraping
headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
    # 'cache-control': 'max-age=0',
    # 'dnt': '1',
    # 'referer': 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q=Awarding+Price%2C+Contract+Performance%2C+and+Bids+Screening%3A+Evidence+from+Procurement+Auctions&btnG=',
    # 'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0',
    # 'x-client-data': 'CIq2yQEIo7bJAQjBtskBCKmdygEIsp3KAQjXncoBCNqdygEIqKPKAQifp8oBGIOYygE=',
    # 'cookie': 'S4L4pn1QvyKJJ07ROBgiU22ph9NcFOlRSrHozwY6g1Ea7WSeaGpXapGwMfwNe6U73yljCjNS_ebben1aMcBkCMM'

    # Firefox
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'scholar.google.com.au',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0',
}

proxy_ip = '13.58.94.178'
starting_pos = 351
http_proxy = 'http://' + proxy_ip + ':8889'
print('http_proxy = ' + http_proxy)
print('starting_pos = ' + str(starting_pos))


url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='

# Get Mariadb cursor
conn = pymysql.connect(host='localhost', user='root', database='citation', autocommit=True)
cursor = conn.cursor()

# E.g.: Read
# query = 'SELECT * FROM article';
# cursor.execute(query);
# result = cursor.fetchall()
# for row in result:
#        print(row)

# E.g.: Create
# query = "insert into article (id, title, citation) values (-1000, 'test test test test test', -5000);"
# result = cursor.execute(query)
# print(result)

firstline = True
with open('citation.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # Skip first line
    next(spamreader)
    for row in spamreader:
        if int(row[0]) <= starting_pos:
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
        url = url_pre + url_key + url_post
        print("Parsed URL: " + url)

        # r = requests.get(url, headers)
        r = requests.get(url,headers=headers,proxies = {'http': http_proxy},verify=False)

        print("Http status: " + str(r.status_code))
        http_code = r.status_code

        matches = re.findall(r'(?<=Cited by )([\d]+)' ,r.text)
        print("Match count: " + str(len(matches)))

        m = re.search(r'(?<=Cited by )([\d]+)' ,r.text)

        citation = 0
        if m:
            citation = m.group()
            print("#1 Cited By: " + citation)

        else:
            citation = -1
            print("no match (-1)")
            print(r.text)
            break

        id = str(id)
        journal = str(journal)
        journal = journal.replace('\'', '')
        journal = journal.replace('"', '')

        dates = str(dates)
        dates = dates.replace('\'', '')
        dates = dates.replace('"', '')

        title = str(title)
        title = title.replace('\'', '')
        title = title.replace('"', '')

        author = str(author)
        author = author.replace('\'', '')
        author = author.replace('"', '')

        citation = str(citation)
        http_code = str(http_code)

        query = "insert into article (id, journal, dates, title, author, citation, http_code) values ('" + id + "', '" + journal + "', '" + dates + "', '" + title + "', '" + author + "', '" + citation + "', '" + http_code + "');"
        print("exec: " + query)
        if http_code != '200':
            print(r.text)
            print("Execution stopping.")
            break

        cursor.execute(query)
        print("==============================================================")

        # # Random sleep
        value = randint(60,70)
        print("planning to sleep: " + str(value))
        sleep(value)
        print("hey! I woke up")
