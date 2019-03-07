import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class PiratiSpider(BaseSpider):
    name= "pirati"

    allowed_domains = ["piratskastranka.si"]
    start_urls = ["https://piratskastranka.si/izjave","https://piratskastranka.si/blog"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//div[@class="pagination"]/span/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//div[@class="search-filter-results"]/div[@class="row"]/div/h3/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = response.xpath('normalize-space(string(//article/div[@class="entry-content"]))').extract_first("")

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

