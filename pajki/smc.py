import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class SMCSpider(BaseSpider):
    name= "smc"

    allowed_domains = ["strankasmc.si"]
    start_urls = ["https://www.strankasmc.si/category/novice","https://www.strankasmc.si/tag/poslanska-skupina-smc/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//div[@id="fp_news"]/div[2]/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//div[@id="fp_news"]/div/article/div/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = " ".join(response.xpath('normalize-space(string(//article/p))').extract())

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

