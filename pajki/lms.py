import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class LMSSpider(BaseSpider):
    name= "lms"

    allowed_domains = ["strankalms.si"]
    start_urls = ["http://www.strankalms.si/category/novosti/","http://www.strankalms.si/category/blog-zapisi/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//nav[@class="pagination"]/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//header[@class="entry-content-header"]/h3/a')), callback='parse_novica'),
    )


    def parse_novica(self, response):
        body = " ".join(response.xpath('normalize-space(string(//div[@itemprop="text"]/p))').extract())

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

