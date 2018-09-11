import csv
import requests
import re
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}

url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='

with open('citation.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        # print(', '.join(row))
        # print(row[3])
        id = row[0]
        article = row[3]

        print("Processing id: " + id + ", article: " + article)

        parsedKey = urllib.parse.quote(article)
        url_key = parsedKey.replace("%20", "+")
        url = url_pre + url_key + url_post
        print("Parsed URL: " + url)

        r = requests.get(url, headers)
        print("Http status: " + str(r.status_code))

        matches = re.findall(r'(?<=Cited by )([\d]+)' ,r.text)
        print("Match count: " + str(len(matches)))

        m = re.search(r'(?<=Cited by )([\d]+)' ,r.text)
        if m:
           print("#1 Cited By: " + m.group())
        else:
           print("no match")
