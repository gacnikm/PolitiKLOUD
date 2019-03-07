import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class SDSpider(BaseSpider):
    name= "sd"

    allowed_domains = ["socialnidemokrati.si"]
    start_urls = ["http://socialnidemokrati.si/blog/category/novice/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//nav[@class="pagination"]/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//header[@class="entry-content-header"]/h2/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = " ".join(response.xpath('//div[@itemprop="text"]/p/text()').extract())

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

