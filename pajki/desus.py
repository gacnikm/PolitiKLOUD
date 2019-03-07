import os

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from pajki.base import BaseSpider
from pajki.db import db, URL

class DESUSSpider(BaseSpider):
    name= "desus"

    allowed_domains = ["desus.si"]
    start_urls = ["http://desus.si/novice/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//ul[@class="kl-pagination"]/li/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//h3[@itemprop="headline"]/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = " ".join(response.xpath('normalize-space(string(//div[@itemprop="text"]/p))').extract())

        if body:
            URL.create(content=body, url=response.url)

