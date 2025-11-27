# https://docs.scrapy.org/en/latest/topics/practices.html
import scrapy
import time
import numpy as np
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from newsScraping.spiders.DeStandaard import DeStandaardSpider
from newsScraping.spiders.vrtNws import VrtNwsSpider
from newsScraping.spiders.DeMorgen import DeMorgenSpider
from newsScraping.spiders.Nieuwsblad import NieuwsbladSpider

spiders = [VrtNwsSpider, DeStandaardSpider, DeMorgenSpider, NieuwsbladSpider]

def run_single_spider(spider_class):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class)
    process.start()

def run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider in spiders:
        process.crawl(spider)
    process.start()

def run_benchmark_spiders(task):
    times = []
    iterations = 5
    for _ in range(iterations):
        start_time = time.time()
        p = multiprocessing.Process(target=task)
        p.start()
        p.join()
        end_time = time.time()
        times.append(end_time - start_time)
    return times

def run_parallel_spiders():
    processes = []
    for spider in spiders:
        p = multiprocessing.Process(target=run_single_spider, args=(spider,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

if __name__ == "__main__":
    run_parallel_spiders()
    # seq_res = run_benchmark_spiders(run_spiders)
    # par_res = run_benchmark_spiders(run_parallel_spiders)
    # print(f"Sequential times: {seq_res}")
    # print(f"Total scraping time: {sum(seq_res)} seconds")
    # print(f"Average scraping time: {np.mean(seq_res)} seconds")
    # print(f"Parallel times: {par_res}")
    # print(f"Total scraping time: {sum(par_res)} seconds")
    # print(f"Average scraping time: {np.mean(par_res)} seconds")