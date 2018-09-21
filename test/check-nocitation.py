import csv
import requests
import re
import urllib.parse
import pymysql
# from random import randint
from time import sleep
import subprocess
# from subprocess import call

no_citation_key = 'Sort by relevance'

f = open('data/4230-fake.html', 'r')
html = f.read()
no_citation_key_index = html.find(no_citation_key)
print(no_citation_key_index)
if no_citation_key_index == -1:
    print('not found')
else:
    print('found! ' + str(no_citation_key_index))

f.close()
