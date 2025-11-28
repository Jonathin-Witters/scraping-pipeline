# https://docs.scrapy.org/en/latest/topics/practices.html
from newsScraping.DatabaseManager import DatabaseManager
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
from newsScraping.spiders.HBVL import HBVLSpider
from newsScraping.spiders.Telegraaf import TelegraafSpider
from newsScraping.spiders.GVA import GVASpider

spiders = {
    "destandaard": DeStandaardSpider,
    "vrtnws": VrtNwsSpider,
    "dedorgen": DeMorgenSpider,
    "nieuwsblad": NieuwsbladSpider,
    "hbvl": HBVLSpider,
    "telegraaf": TelegraafSpider,
    "gva": GVASpider,
}


def get_spider_by_name(name: str):
    if not name:
        return None

    # Case-insensitive
    return spiders.get(name.lower())

def run_single_spider(spider_class):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class)
    process.start()

def run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider in spiders.values:
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

if __name__ == "__main__":
    manager = DatabaseManager()

    # Try to fetch jobs with retries on exception
    max_attempts = 3
    backoff = 0.5
    nr_of_jobs = 2
    jobs = None
    for attempt in range(1, max_attempts + 1):
        try:
            jobs = manager.get_work_batch(nr_of_jobs)
        except Exception as exc:
            print(f"Attempt {attempt} failed when fetching jobs: {exc}")
            if attempt < max_attempts:
                time.sleep(backoff * attempt)
            else:
                print("Max attempts reached; aborting.")

    # If no jobs returned or an error occurred and jobs is still None, do nothing
    if not jobs:
        print("No jobs to process.")
    else:
        # Map jobs to spider classes using spider_map
        spider_classes = []
        for job in jobs:
            spider = get_spider_by_name(job)
            spider_classes.append(spider)

        print(spider_classes)

        run_parallel_spiders_for_list(spider_classes)
    # seq_res = run_benchmark_spiders(run_spiders)
    # par_res = run_benchmark_spiders(run_parallel_spiders)
    # print(f"Sequential times: {seq_res}")
    # print(f"Total scraping time: {sum(seq_res)} seconds")
    # print(f"Average scraping time: {np.mean(seq_res)} seconds")
    # print(f"Parallel times: {par_res}")
    # print(f"Total scraping time: {sum(par_res)} seconds")
    # print(f"Average scraping time: {np.mean(par_res)} seconds")