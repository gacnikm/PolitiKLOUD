import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pajki.db import db, URL
from pajki.base import BaseSpider

class SABSpider(BaseSpider):
    name= "sab"

    allowed_domains = ["sab.si"]
    start_urls = ["http://www.sab.si/aktualno/"]

    rules = (
        Rule(LinkExtractor(allow=(),
                               restrict_xpaths=('//div[@class="et_pb_ajax_pagination_container"]/div[2]/div/a')),
             follow=True),
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//article/div/a')), callback='parse_novica'),
    )

    def parse_novica(self, response):
        body = " ".join(response.xpath('normalize-space(string(//div[@class="et_pb_text_inner"]))').extract())

        if body:
            URL.create(content=body, url=response.url)
            #print(body)

