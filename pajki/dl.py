import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

from settings import DATA_PATH

class DLSpider(BaseSpider):
    name= "dl"

    allowed_domains = ["d-l.si"]
    start_urls = ["http://www.d-l.si/index.php?page=news&item=9&type=arhiv&c=4"]

    rules = (

        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//div[@id="title"]/h2/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = response.xpath('normalize-space(string(//*[@id="contents"]))').extract_first("")
        if body:
            URL.create(content=body, url=response.url)
            #print(body)

