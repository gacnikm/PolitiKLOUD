import argparse
import logging
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from settings import STRANKE, DATA_PATH

parser = argparse.ArgumentParser()
parser.add_argument("stranka", choices=STRANKE,
                    help="izberi stranko")

args = parser.parse_args()
STRANKA = args.stranka

settings = get_project_settings()
settings['TELNETCONSOLE_ENABLED'] = False
settings['LOG_LEVEL'] = logging.INFO
settings['LOG_FILE'] = os.path.join(DATA_PATH,'log',"%s_log.txt" % (STRANKA,))

process = CrawlerProcess(settings)
process.crawl(STRANKA)
process.start()