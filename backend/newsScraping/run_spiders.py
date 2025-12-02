import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_single_spider(spider_class):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class)
    process.start()

def run_spiders(spider_classes: list):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider in spider_classes:
        process.crawl(spider)
    process.start()

def run_parallel_spiders_for_list(spider_classes: list):
    processes = []
    for spider in spider_classes:
        if spider is None:
            continue
        p = multiprocessing.Process(target=run_single_spider, args=(spider,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()