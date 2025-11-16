# https://docs.scrapy.org/en/latest/topics/practices.html
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import spider implementations
from newsScraping.spiders.DeStandaard import DeStandaardSpider
from newsScraping.spiders.vrtNws import VrtNwsSpider
from newsScraping.spiders.DeMorgen import DeMorgenSpider


def run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(VrtNwsSpider)
    process.crawl(DeStandaardSpider)
    process.crawl(DeMorgenSpider)
    process.start()

if __name__ == "__main__":
    run_spiders()