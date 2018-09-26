import csv
import requests
import re
import urllib.parse
import pymysql
# from random import randint
from time import sleep
import subprocess
# from subprocess import call
from time import strftime

# Exclusive!
previous_pos = 0
ending_pos = 4229
sleep_interval = 1
max_attempt = 10

proxy = ''
url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='
proxy_count = 0
proxy_life = 5

no_citation_key1 = 'Sort by relevance'
no_citation_key2 = 'Sort by date'
no_citation_key3 = 'Since 2018'

robot_key1 = 'Please show you&#39;re not a robot'

# Get Mariadb cursor
conn = pymysql.connect(host='localhost', user='root', database='citation', autocommit=True)
cursor = conn.cursor()

def getnewProxy():
    global proxy
    global proxy_count
    proxy_count += 1
    print("current proxy_count: " + str(proxy_count))


    try:
        # r = requests.get('https://gimmeproxy.com/api/getProxy')
        # r = requests.get('https://gimmeproxy.com/api/getProxy?protocol=http&country=AU&websites=google&api_key=539aad0a-f164-4b9c-96e2-98eec91dbac3')
        r = requests.get('https://gimmeproxy.com/api/getProxy?protocol=http&api_key=539aad0a-f164-4b9c-96e2-98eec91dbac3')

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
        if int(row[0]) > ending_pos:
            exit()

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
            print(strftime("%Y-%m-%d %H:%M:%S"))
            print("Processing id: [" + id + "], title: [" + title + "]" )

            parsedKey = urllib.parse.quote(title)
            url_key = parsedKey.replace("%20", "+")
            url = url_pre + url_key + url_post
            print("Parsed URL: " + url)

            # Try to Erase existing data file
            try:
                f = open(dataFileName, 'w')
                f.close()
                print('Cleaned existing data file')
            except:
                print('No existing data file')

            # cURL
            handle = open(dataFileName, 'w')
            curl_command = "curl '" + url + "' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers' --proxy " + proxy
            print('curl comnad is: ' + curl_command)
            out = subprocess.Popen(curl_command, shell=True, stdout=handle)

            # Proxy recycling
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

            if line_prev > 0:
                print("HTML get √")
            else:
                print("no HTML get :(")

            matches = re.findall(r'(?<=Cited by )([\d]+)', html)
            print("Match count: " + str(len(matches)))

            m = re.search(r'(?<=Cited by )([\d]+)', html)

            citation = -100
            if m:
                citation = m.group()
                print("#1 Cited By: " + citation + ". Success!")
                success = True
            else:
                citation = -1
                print('no match (-1).')
                print('html: ' + html)

                # Check if this is nocitation article
                no_citation_key_index1 = html.find(no_citation_key1)
                no_citation_key_index2 = html.find(no_citation_key2)
                no_citation_key_index3 = html.find(no_citation_key3)
                robot_key_index1 = html.find(robot_key1)

                no_citation_flag1 = no_citation_key_index1 != -1
                no_citation_flag2 = no_citation_key_index2 != -1
                no_citation_flag3 = no_citation_key_index3 != -1

                # debug
                print("no_citation_key_index1 = " + str(no_citation_key_index1))
                print("no_citation_key_index2 = " + str(no_citation_key_index2))
                print("no_citation_key_index3 = " + str(no_citation_key_index3))
                print("no_citation_flag1 = " + str(no_citation_flag1))
                print("no_citation_flag2 = " + str(no_citation_flag2))
                print("no_citation_flag3 = " + str(no_citation_flag3))

                if robot_key_index1 != -1:
                    print('robot key found. Running with new proxy')
                    getnewProxy()

                elif no_citation_flag1 != no_citation_flag2 or no_citation_flag2 != no_citation_flag3:
                    print('nocitation keys are not consistent. Running with new proxy')
                    getnewProxy()

                elif no_citation_key_index1 == -1:
                    print('no nocitation keys not found. Running with new proxy')
                    getnewProxy()
                else:
                    print('This article has no citation. Go next')
                    success = True
                    citation = 0

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
