import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class NSISpider(BaseSpider):
    name= "nsi"

    allowed_domains = ["nsi.si"]
    start_urls = ["http://nsi.si/category/novice/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//ul[@class="page-numbers"]/li/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//div[@id="primary-left"]/div/div[@class="entry-content"]/a[@class="read-more"]')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = response.xpath('normalize-space(string(//div[@class="single-post-container"]/div[1]))').extract_first("")

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

