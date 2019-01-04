# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy import Spider
from douban.items import DoubanItem
from scrapy.http import Request

class DoubanSpider(Spider):
  """docstring for Movie2015Spider"""
  name = 'movie2015'
  allowed_domains = ["douban.com"]
  start_urls = [
    "http://www.douban.com/doulist/36742433/"
  ]

  def parse(self, response):
    for info in response.xpath('//div[@class="doulist-item"]'):
      item = DoubanItem()
      item['number'] = info.xpath('div[@class="mod"]/div[@class="bd doulist-subject"]/div[@class="rating"]/span[3]/text()').extract()
      item['rate'] = info.xpath('div[@class="mod"]/div[@class="bd doulist-subject"]/div[@class="rating"]/span[@class="rating_nums"]/text()').extract()

      yield item

    # 翻页
    next_page = response.xpath('//span[@class="next"]/a/@href')
    if next_page:
      url = response.urljoin(next_page[0].extract())
      yield Request(url, self.parse)
