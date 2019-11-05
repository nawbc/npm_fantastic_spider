from scrapy.spiders import CrawlSpider
from re import search, match
from npm_fantastic.items import NpmFantasticItem
from urllib.parse import urlparse
from scrapy.http import Request as Req

def dev_console():
  print('\033[1;35;46m {} \033[0m'.format('*' * 20))

_item = NpmFantasticItem()

class NpmFantasticSpider(CrawlSpider):
  name = 'npm'

  allowed_domains = [
    'www.npmjs.com',
    'www.github.com',
  ]

  start_urls = [
    "https://www.npmjs.com/search?q=web",
  ]

  def __init__(self, search):
    self.search = search

  def dfs(self):

    return True

  def merge_item(self, origin, target, can_pass):
    for (index, val) in target.items():
      if match(can_pass, index):
        origin[index] = val
    return origin

  def handle_mqp(self, ls):
    return [{search('[a-zA-Z]+', b).group(0): int(search('\d+', b).group(0))} for b in ls]

  def group_link(self, res, link):
    hostname = urlparse(res.url).hostname
    return 'https://' + hostname + link

  # exrtract name from href
  def extract_name(self, link):
    return search('(?<=/~)(.)+', link).group(0)

  def request_github(self, res):
    repo_item = NpmFantasticItem()

    dev_console()
    return repo_item

  # get package details
  def get_pkg_details_page(self, res):
    item = NpmFantasticItem()
    repo_links = res.xpath(
      '//div[contains(@class, "dib w-50 bb b--black-10 pr2")]//a//@href').extract()

    item['pkg_version'] = res.xpath(
      '//p[contains(@class, "fw6 mb3 mt2 truncate black-80 f4")]//text()').extract()[0]

    item['pkg_license'] = res.xpath(
      '//p[contains(@class, "fw6 mb3 mt2 truncate black-80 f4")]/text()').extract()[1]

    item['pkg_homepage'] = repo_links[0]

    item['pkg_last_update'] = res.xpath(
      '//p[contains(@class, "fw6 mb3 mt2 truncate black-80 f4")]/time//@datetime').extract()[0]

    item['pkg_collaborator'] = [
      {
        'name': self.extract_name(name_link),
        'homepage': self.group_link(res, name_link)
      } for name_link in res.xpath('//ul[contains(@class, "list pl0 cf")]//a//@href').extract()]

    item['repo_link'] = repo_links[1]

    dev_console()

    return self.merge_item(item, res.meta, 'repo|pkg')

  # get initial page
  def request_page(self, res, list_item):

    for section in res.xpath('//section[contains(@class, "flex flex-row-reverse pl1-ns pt3 pb2 ph1 bb b--black-10")]'):

      mqp = self.handle_mqp(section.xpath(
        './/div[re:test(@title,"Popularity|Maintenance|Quality")]//@title').extract())

      quality = mqp[1]['Quality']
      popularity = mqp[2]['Popularity']
      maintenance = mqp[0]['Maintenance']

      if maintenance > 30 and quality > 20 and popularity > 50:

        detail_link = self.group_link(res, section.xpath(
          './/div[contains(@class,"flex flex-row items-end pr3")]/a//@href').extract()[0])

        author_link = section.xpath(
          './/a[contains(@class, "pl2 pr2 black-70 fw6 db hover-black no-underline")]//@href').extract()[0]

        list_item['pkg_name'] = section.xpath(
          './/h3[contains(@class, "fw6 f4 black-90 dib lh-solid ma0 no-underline hover-black")]/text()').extract()[0]

        list_item['pkg_author'] = {
          "name": self.extract_name(author_link),
          "homepage": self.group_link(res, author_link)
        }

        list_item['pkg_link'] = detail_link

        list_item['pkg_quality'] = mqp

        dict_item = dict(list_item)

        yield Req(detail_link, method='GET', callback=self.get_pkg_details_page, meta=dict_item)

      else:
        continue

    jump_links = res.xpath('//div[contains(@class,"fl tl tr-l pt3-l pb1-l mb3")]//a//@href').extract()
    next = jump_links[len(jump_links) - 1]
    if next:
      yield Req(self.group_link(res, next), callback=self.parse)

  def parse(self, res):
    return self.request_page(res, _item)