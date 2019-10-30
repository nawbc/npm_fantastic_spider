from scrapy.spiders import CrawlSpider, Rule
from re import search, match
from scrapy.linkextractors import LinkExtractor
from npm_fantastic.items import NpmFantasticItem
from urllib.parse import urlunparse, urlparse
from scrapy.http import Request as Req


def dev_console():
  print('\033[1;35;46m {} \033[0m'.format('*' * 20))


class NpmFantasticSpider(CrawlSpider):
  name = 'npm'

  allowed_domains = [
    'npmjs.com'
  ]

  start_urls = [
    "https://www.npmjs.com/search?q=web",
  ]

  def merge_item(self, origin, target, can_pass):
    for (index, val) in target.items():
      if match(can_pass, index):
        origin[index] = val
    return origin

  def handle_mqp(self, ls):
    return [{search('[a-zA-Z]+', b).group(0): int(search('\d+', b).group(0))} for b in ls]

  def request_github(self, res):
    repo_item = NpmFantasticItem()
    dev_console()
    return repo_item

  # get package details
  def get_details_page(self, res):
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

    item['repo_link'] = repo_links[1]

    item = self.merge_item(item, res.meta, 'repo|pkg')

    print(item)

    # yield Req(repo_links[1], method='GET', callback=self.request_github)

    return item

  # get initial page
  def request_page(self, res):
    hostname = urlparse(res.url).hostname
    list_item = NpmFantasticItem()

    for section in res.xpath('//section[contains(@class, "flex flex-row-reverse pl1-ns pt3 pb2 ph1 bb b--black-10")]'):
      mqp = self.handle_mqp(section.xpath(
        './/div[re:test(@title,"Popularity|Maintenance|Quality")]//@title').extract())

      maintenance = mqp[0]['Maintenance']
      quality = mqp[1]['Quality']
      popularity = mqp[2]['Popularity']
      if maintenance > 30 and quality > 20 and popularity > 50:
        detail_link = 'https://' + hostname + section.xpath(
          './/div[contains(@class,"flex flex-row items-end pr3")]/a//@href').extract()[0]
        author_link = section.xpath(
          './/a[contains(@class, "pl2 pr2 black-70 fw6 db hover-black no-underline")]//@href').extract()[0]

        list_item['pkg_name'] = section.xpath(
          './/h3[contains(@class, "fw6 f4 black-90 dib lh-solid ma0 no-underline hover-black")]/text()').extract()[0]

        list_item['pkg_author'] = {
          "name": search('(?<=/~)(.)+', author_link).group(0),
          "homepage": 'https://' + hostname + author_link
        }

        list_item['pkg_link'] = detail_link

        list_item['pkg_quality'] = mqp

        a = dict(list_item)

        yield list_item

        yield Req(detail_link, method='GET', callback=self.get_details_page, meta=a)

      else:
        continue

  def err_back(self, err):
    print(err)

  def parse(self, res):

    return self.request_page(res)
