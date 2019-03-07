import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

from settings import DATA_PATH

class LevicaSpider(BaseSpider):
    name= "levica"

    allowed_domains = ["levica.si"]
    start_urls = ["http://www.levica.si/novice/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//div[@class="main-pagination"]/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//article/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = response.xpath('normalize-space(string(//div[@class="post-content-right"]))').extract_first("")

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

