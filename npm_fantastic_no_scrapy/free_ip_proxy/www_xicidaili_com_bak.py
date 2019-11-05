# import re
# import requests
# import time
# import redis
# import json
# from urllib.parse import urljoin
# from bs4 import BeautifulSoup as BSoup
#
# initial_url = 'https://www.xicidaili.com/nn'
# user_agents = [
#   'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
#   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
#   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
#   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
#   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
# ]
#
#
# def www_xicidaili_com(count=None):
#   if count == len(user_agents):
#     count = 0
#   else:
#     count += 1
#   headers = {
#     'User-Agent': user_agents[count],
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'Connection': 'keep-alive',
#     'Host': 'www.xicidaili.com',
#     'Cache-Control': 'no-cache',
#     'Accept-Encoding': 'gzip, deflate',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Referer': 'https://www.xicidaili.com/',
#     'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTI1NmRiNjI5NzVhNzAyNWU2MWRjN2ZhMzM1NDFhNzU4BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXJRV3pPYVR5ZUgyTE15b0oyaWpZR0N4bUQ3SDFkTHFxS1loWmtTaFdtdnM9BjsARg%3D%3D--b0b90403969295a73c6cf28ff5dde639579f5664; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1572664303; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1572664930'
#   }
#   # print(headers)
#   r = requests.get(initial_url, headers)
#   print(r.text)
#   soup = BSoup(r.text, 'html.parser')
#   tr = soup.find('table', id='table_list')
#
#   next = soup.find('a', attrs={'class': 'next_page'})
#   print(tr, next)
#   # if next:
#   #   www_xicidaili_com()
#
#
# www_xicidaili_com(0)

