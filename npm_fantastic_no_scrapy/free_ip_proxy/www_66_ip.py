import re
import requests
import redis
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup as BSoup

initial_url = 'http://www.66ip.cn/'
client = redis.Redis(host='localhost', port=6379, db=0, password='outlook9423')

def get_details(link):
  r = requests.get(link)
  soup = BSoup(r.text, 'html.parser')
  trs = soup.find_all('table')[2].find_all('tr')
  for (index, tr) in enumerate(trs):
    if index != 0:
      tds = tr.find_all('td')
      ip = tds[0].get_text()
      port = tds[1].get_text()
      result = json.dumps({'ip': ip, 'port': port})
      print(result)
      client.lpush('66ip', result)


def get_ip_lists_from_66():
  r = requests.get(initial_url)
  soup = BSoup(r.text, 'html.parser')
  c = soup.find_all('a', href=re.compile('areaindex'))
  for alink in c:
    c_link = urljoin(initial_url, alink.get('href'))
    get_details(c_link)

# get_ip_lists_from_66()
