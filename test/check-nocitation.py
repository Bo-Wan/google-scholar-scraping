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
robot_key = 'Please show you&#39;re not a robot'

f = open('../html-data/38138.html', 'r')
html = f.read()
no_citation_key_index = html.find(no_citation_key)
print(no_citation_key_index)
if no_citation_key_index == -1:
    print('nocitation key not found')
else:
    print('nocitation key found! ' + str(no_citation_key_index))

robot_key_index = html.find(robot_key)
print(robot_key_index)
if robot_key_index == -1:
    print('robot key not found')
else:
    print('robot key found! ' + str(no_citation_key_index))


f.close()
