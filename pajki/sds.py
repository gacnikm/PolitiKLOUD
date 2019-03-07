import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class SDSSpider(BaseSpider):
    name= "sds"

    allowed_domains = ["sds.si"]
    start_urls = ["https://www.sds.si/arhiv/novice"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//div[@class="pager"]/ul/li/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//div[@class="article-list--archive"]/a')), callback='parse_novica'),

    )

    def parse_novica(self, response):
        body = response.xpath('normalize-space(string(//article))').extract_first("")

        if body:
            URL.create(content=body, url=response.url)