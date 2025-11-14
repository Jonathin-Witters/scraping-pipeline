# https://docs.scrapy.org/en/latest/topics/practices.html

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import spider implementations
from newsScraping.spiders.DeStandaard import DeStandaardSpider
from newsScraping.spiders.vrtNws import VrtNwsSpider


def run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(VrtNwsSpider)
    process.crawl(DeStandaardSpider)
    process.start()

if __name__ == "__main__":
    run_spiders()