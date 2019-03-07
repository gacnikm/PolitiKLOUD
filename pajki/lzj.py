import os
from urllib.parse import parse_qs, urlparse

from scrapy import Request
from scrapy.spiders import Spider

from pajki.db import db, URL

from settings import DB_DATA_PATH,DATA_PATH

class LZJSpider(Spider):
    name= "lzj"

    allowed_domains = ["zoranjankovic.si"]
    start_urls = ["https://www.zoranjankovic.si/novice?page=0"]

    def __init__(self,*a, **kw):
        super(LZJSpider, self).__init__(*a, **kw)
        db.init(os.path.join(DB_DATA_PATH,'%s.sqlite'%(self.name,)))
        db.connect()
        db.create_tables([URL])

    def parse(self, response):
        hrefs = response.xpath("//article/h2/a/@href").extract()

        if hrefs:
            for href in hrefs:
                yield Request(url=response.urljoin(href),callback=self.parse_novica)

            h = {
                "DNT":"1",
                "Accept-Language":"en,sl;q=0.9,en-US;q=0.8",
                "Accept-Encoding:":"gzip, deflate, br",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/70.0.3538.102",
                "Accept":"*/*",
                "Referer":"https//www.zoranjankovic.si/novice",
                "X-Requested-With":"XMLHttpRequest",
                "Connection":"keep-alive"
            }
            page = int(parse_qs(urlparse(response.url).query)['page'][0])
            page +=1
            req = Request(url="https://www.zoranjankovic.si/novice?page="+str(page), callback=self.parse, headers=h)
            yield req

    def parse_novica(self, response):

        body = response.xpath('normalize-space(string(///div[@class="container"]/div[3]/div))').extract_first("")

        if body:
            URL.create(content=body, url=response.url)
            #print(body)
