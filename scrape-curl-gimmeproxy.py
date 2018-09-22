import csv
import requests
import re
import urllib.parse
import pymysql
# from random import randint
from time import sleep
import subprocess
# from subprocess import call

# Exclusive!
previous_pos = 11141
sleep_interval = 1
max_attempt = 10

proxy = ''
url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='
proxy_count = 0
proxy_life = 5

no_citation_key = 'Sort by relevance'


# Get Mariadb cursor
conn = pymysql.connect(host='localhost', user='root', database='citation', autocommit=True)
cursor = conn.cursor()

def getnewProxy():
    global proxy
    global proxy_count
    proxy_count += 1
    print("current proxy_count: " + str(proxy_count))

    # r = requests.get('https://gimmeproxy.com/api/getProxy')
    # r = requests.get('https://gimmeproxy.com/api/getProxy?protocol=http&country=AU&websites=google&api_key=539aad0a-f164-4b9c-96e2-98eec91dbac3')
    r = requests.get('https://gimmeproxy.com/api/getProxy?protocol=http&api_key=539aad0a-f164-4b9c-96e2-98eec91dbac3')

    try:
        proxyResult = r.json()
        type = proxyResult['type']
        if type != 'http':
            getnewProxy()
        else:
            proxy = proxyResult['curl']
            print('New proxy get: ' + proxy)
    except:
        getnewProxy()



getnewProxy()
with open('citation.csv', newline='') as csvfile:
    csv_lines = csv.reader(csvfile, delimiter=',', quotechar='"')
    proxy_use = 0

    # Skip first line
    next(csv_lines)
    for row in csv_lines:
        if int(row[0]) <= previous_pos:
            continue

        # Main logic
        id = row[0]
        journal = row[1]
        dates = row[2]
        title = row[3]
        author = row[4]

        dataFileName = 'html-data/' + id + '.html'
        success = False

        # Proxy + cURL until gets citation
        while not success:
            print("Processing id: [" + id + "], title: [" + title + "]")

            parsedKey = urllib.parse.quote(title)
            url_key = parsedKey.replace("%20", "+")
            url = url_pre + url_key + url_post
            print("Parsed URL: " + url)

            # # debug 1
            # f = open('test.html', 'r')
            # print("old file: " + f.read())
            # f.close()

            # Try to Erase test.html
            try:
                f = open(dataFileName, 'w')
                f.close()
                print('Cleaned existing data file')
            except:
                print('No existing data file')
            # # debug 2
            # f = open('test.html', 'r')
            # print("erased file: " + f.read())
            # f.close()


            # cURL
            handle = open(dataFileName, 'w')
            curl_command = "curl '" + url + "' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers' --proxy " + proxy
            print('curl comnad is: ' + curl_command)
            out = subprocess.Popen(curl_command, shell=True, stdout=handle)

            # Proxy life
            proxy_use += 1
            print('proxy_use = ' + str(proxy_use))
            if proxy_use >= proxy_life:
                print('proxy_life limit reached. Getting new proxy')
                getnewProxy()
                proxy_use = 0

            # Check file ready
            html_done = False
            line_prev = 0
            attempt = 0
            attempt_fail = False
            while not html_done:
                sleep(sleep_interval)
                line_new = sum(1 for line in open(dataFileName))

                # debug 3
                print('Line count: ' + str(line_new))

                if(line_prev != 0 and line_new != 0 and line_new == line_prev):
                    html_done = True
                else:
                    line_prev = line_new

                attempt += 1
                if attempt > max_attempt:
                    break

            if attempt_fail:
                getnewProxy()
                continue

            # Read
            f = open(dataFileName, 'r')
            html = f.read()
            f.close()

            # print("Get HTML: " + html)
            print("HTML get√")
            matches = re.findall(r'(?<=Cited by )([\d]+)', html)
            print("Match count: " + str(len(matches)))

            m = re.search(r'(?<=Cited by )([\d]+)', html)

            citation = 0
            if m:
                citation = m.group()
                print("#1 Cited By: " + citation + ". Success!")
                success = True
            else:
                citation = -1
                print('no match (-1).')
                print('html: ' + html)

                # Check if this is nocitation article
                no_citation_key_index = html.find(no_citation_key)
                if no_citation_key_index == -1:
                    print('nocitation key not found too. Running with new proxy')
                    getnewProxy()
                else:
                    print('This article has no citation. Go next')
                    success = True
                    citation = 0



        #     # debug - start
        #     success = True;
        # break
        # # debug - end

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

        # query = "insert into article (id, journal, dates, title, author, citation, http_code) values ('" + id + "', '" + journal + "', '" + dates + "', '" + title + "', '" + author + "', '" + citation + "', '" + http_code + "');"
        query = "insert into article (id, journal, dates, title, author, citation) values ('" + id + "', '" + journal + "', '" + dates + "', '" + title + "', '" + author + "', '" + citation + "');"
        print("exec: " + query)

        cursor.execute(query)
        print("==============================================================")
