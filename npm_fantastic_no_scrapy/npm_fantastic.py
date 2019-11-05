#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql
import logging
import requests
from json import dumps
from re import compile, search
from bs4 import BeautifulSoup as BSoup
from urllib.parse import urljoin, urlparse
# from

# sys.argv
# print(sys.argv)

host = 'https://www.npmjs.com'
github_api = 'https://api.github.com'

con = pymysql.connect('localhost', 'root', 'outlook9423', 'npm_fantastic')

user_agents = [
  'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
]

headers = {
  'Connection': 'keep-alive',
  'Sec-Fetch-Mode': 'no-cors'
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def save_to_mysql(*data):
  db = con.cursor()
  sql = 'INSERT INTO `npm_info`' \
        '(`pkg_name`,' \
        '`pkg_link`,' \
        '`pkg_version`,' \
        '`pkg_author`,' \
        '`pkg_license`,' \
        '`pkg_homepage`,' \
        '`pkg_last_update`,' \
        '`pkg_judge`,' \
        '`pkg_collaborator`,' \
        '`pkg_repo`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
  try:
    db.execute(sql, data)
    con.commit()
  except Exception as e:
    print(e)
    con.rollback()
  db.close()

# def get_proxy_from_redis():


def sub_keywords(keywords_stack, val):
  try:
    keywords_stack.index(val)
  except ValueError as e:
    if e:
      keywords_stack.append(val)


def handle_author_info(link):
  name = search('(?<=/~)(.)+', link).group(0)
  lk = urljoin(host, link)
  return {
    'name': name,
    'homepage': lk
  }


def handle_pqm(item):
  wrapper = item.find('div', attrs={'class': compile('fr justify-between flex flex-column-reverse mt3 mb2 ml2 pb0')})
  slider = wrapper.find_all('div', attrs={'class': compile('flex flex-row-reverse relative')})
  popularity = int(search('\d+', slider[0]['title']).group(0))
  quality = int(search('\d+', slider[1]['title']).group(0))
  maintenance = int(search('\d+', slider[2]['title']).group(0))
  return {
    'm': maintenance,
    'q': quality,
    'p': popularity
  }


def satisfy_filter_range(a, b, c):
  if a > 30 and b > 30 and c > 40:
    return True
  else:
    return False


def gen_search_url(keywords):
  return urljoin(host, 'search?q=keywords:{}'.format(keywords))


def get_pkg_details(url, info, hs):
  r = requests.get(url, headers=hs)
  soup = BSoup(r.text, 'html.parser')
  p_tags = soup.find_all('p', attrs={'class': compile('fw6 mb3 mt2 truncate black-80 f4')})
  ul_tag = soup.find('ul', attrs={'class': 'list pl0 cf'})
  repo_link = p_tags[3].a['href']
  repo_api_link = urljoin(github_api, urlparse(repo_link).path)
  pkg_name = soup.find('span', attrs={'class': compile('truncate flex-auto')})['title']
  pkg_version = p_tags[0].text
  pkg_license = p_tags[1].text
  pkg_homepage = p_tags[2].a['href']
  pkg_repo = {'main': repo_link, 'api': repo_api_link}
  pkg_collaborator = [handle_author_info(a['href']) for a in ul_tag.find_all('a')]
  pkg_last_update = soup.find('time').text

  logger.info('Package: ' + pkg_name + ' --- ' + info['pkg_link'])

  save_to_mysql(
    pkg_name,
    info['pkg_link'],
    pkg_version,
    dumps(info['pkg_author']),
    pkg_license,
    pkg_homepage,
    pkg_last_update,
    dumps(info['pkg_judge']),
    dumps(pkg_collaborator),
    dumps(pkg_repo)
  )


def get_each_page_by_keywords(k_url, keywords_stack, count=None):
  if count < len(user_agents):
    count += 1
  else:
    count = 0

  headers['User-Agent'] = user_agents[count]
  r = requests.get(k_url, headers=headers)
  soup = BSoup(r.text, 'html.parser')
  item_list = soup.find_all('section',
                            attrs={'class': compile('flex flex-row-reverse pl1-ns pt3 pb2 ph1 bb b--black-10')})

  keywords_list = soup.find_all('a',
                                attrs={'class': compile('black-90 bg-black-05 hover-bg-black-10 br2 hover-black')})

  for keyword in keywords_list:
    sub_keywords(keywords_stack, keyword.text)

  for item in item_list:
    pqm = handle_pqm(item)
    pkg_link = urljoin(host, item.find('a', href=compile('/package'))['href'])
    info = {
      'pkg_author': handle_author_info(
        item.find('a', attrs={'class': compile('pl2 pr2 black-70 fw6 db hover-black no-underline')})['href']),
      'pkg_judge': pqm,
      'pkg_link': pkg_link
    }
    if satisfy_filter_range(pqm['p'], pqm['q'], pqm['m']):
      url = urljoin(host, pkg_link)
      try:
        get_pkg_details(url, info, headers)
      except Exception as e:
        logger.error('Error: ' + e)
        continue

  next_page = soup \
    .find_all('div', attrs={"class": compile("fl tl tr-l pt3-l pb1-l mb3")})[0] \
    .find_all('a')
  next_btn = next_page[len(next_page) - 1]
  is_next = next_btn.text[1:2] is '»'
  next_href = urljoin(host, next_btn['href'])

  if is_next:
    get_each_page_by_keywords(next_href, keywords_stack, count)
  elif len(keywords_stack) == 0:
    return True
  else:
    next_keyword_url = gen_search_url(keywords_stack.pop())
    get_each_page_by_keywords(gen_search_url(next_keyword_url), keywords_stack, count)


def npm_fantastic_start():
  keywords_stack = []
  initial_url = 'https://www.npmjs.com/search?q=express'
  get_each_page_by_keywords(initial_url, keywords_stack, 0)


npm_fantastic_start()
