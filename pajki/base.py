import os

from scrapy.spiders import CrawlSpider

from pajki.db import db, URL
from settings import DB_DATA_PATH

class BaseSpider(CrawlSpider):

    def __init__(self,*a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)
        db.init(os.path.join(DB_DATA_PATH,'%s.sqlite'%(self.name,)))
        db.connect()
        db.create_tables([URL])

