import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class SLSSpider(BaseSpider):
    name= "sls"

    allowed_domains = ["sls.si"]
    start_urls = ["http://www.sls.si/c/obvestila/page/1/","http://www.sls.si/c/arhiv/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//div[@class="pagination"]/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//article/a[@class="search-result"]')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = response.xpath('normalize-space(string(//article[1]))').extract_first("")

        if body:
            URL.create(content=body, url=response.url)

