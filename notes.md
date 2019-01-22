curl -c - 'https://scholar.google.com.au/'
curl -s --proxy http://18.191.31.14:8889  -c - 'https://scholar.google.com.au/'

r = requests.get(url,headers=headers,proxies = {'http': 'http://18.191.31.14:8889'},verify=False)

curl 'https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q=Physician+Payment+Reform+and+Hospital+Referrals&btnG=' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers' --proxy http://18.217.253.111:8889
