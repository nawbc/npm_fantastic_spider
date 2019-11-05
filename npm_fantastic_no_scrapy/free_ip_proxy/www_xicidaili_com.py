import re
import time
import json
import redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

initial_url = 'https://www.xicidaili.com'
client = redis.Redis(host='localhost', port=6379, db=0, password='outlook9423')

# proxy_url = ['http://' + json.loads(str(ip, encoding="utf-8"))['ip'] + ':' + json.loads(str(ip, encoding="utf-8"))['port'] for ip in client.lrange('66ip', 0, 100)]

def recursive_url(chrome, url):
  chrome.get(url)
  ip_list = chrome.find_element_by_id('ip_list')
  next_page = chrome.find_elements_by_class_name('next_page')[0]
  href = next_page.get_attribute('href')

  for (index, ele) in enumerate(ip_list.find_elements_by_tag_name('tr')):
    if index != 0:
      tds = ele.find_elements_by_tag_name('td')
      ip = tds[1].text
      port = tds[2].text
      result = json.dumps({'ip': ip, 'port': port})
      live_time = tds[8].text
      isMinite = re.search('分钟', live_time) is None
      if not isMinite:
        print('{} \033[31mnot pass'.format(result))
      if isMinite:
        print('{} \033[32mpass'.format(result))
        client.lpush('xicidaili', result)

  if next_page is not None:
    recursive_url(chrome, urljoin(initial_url, href))


def start_browser():
  # count = 0
  driver_path = '/home/sewer/Desktop/chromedriver/chromedriver'
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  # chrome_options.add_argument('--proxy-server=http://222.128.9.235:33428')

  chrome = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

  chrome.implicitly_wait(10)
  recursive_url(chrome, urljoin(initial_url, '/nn'))

  time.sleep(1000)


start_browser()
