import requests
import re
import urllib.parse

headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'
}

url_pre = 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q='
url_post = '&btnG='

# key = 'Reliability and predictive validity of the Motivated Strategies for Learning Questionnaire (MSLQ)'
article = 'sport key1 key2 key3'
parsedKey = urllib.parse.quote(article)
url_key = parsedKey.replace("%20", "+")

url = url_pre + url_key + url_post

print("Target keyword: " + key)
print("Parsed URL: " + url)

r = requests.get(url, headers)
print("Http status: " + str(r.status_code))
# print(r.text)

matches = re.findall(r'(?<=Cited by )([\d]+)' ,r.text)
print("Match count: " + str(len(matches)))

m = re.search(r'(?<=Cited by )([\d]+)' ,r.text)
if m:
   print("#1 Cited By: " + m.group())
else:
   print("no match")
