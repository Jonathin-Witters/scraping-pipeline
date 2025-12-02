# https://docs.scrapy.org/en/latest/topics/practices.html
from newsScraping.DatabaseManager import DatabaseManager
import scrapy
import time
import numpy as np
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from run_spiders import run_parallel_spiders_for_list
from run_spiders import run_spiders
from run_spiders import run_single_spider

from newsScraping.spiders.DeStandaard import DeStandaardSpider
from newsScraping.spiders.vrtNws import VrtNwsSpider
from newsScraping.spiders.DeMorgen import DeMorgenSpider
from newsScraping.spiders.Nieuwsblad import NieuwsbladSpider
from newsScraping.spiders.HBVL import HBVLSpider
from newsScraping.spiders.Telegraaf import TelegraafSpider
from newsScraping.spiders.GVA import GVASpider
from newsScraping.spiders.DeVolkskrant import DeVolkskrantSpider

spiders = {
    "destandaard": DeStandaardSpider,
    "vrtnws": VrtNwsSpider,
    "demorgen": DeMorgenSpider,
    "nieuwsblad": NieuwsbladSpider,
    "hbvl": HBVLSpider,
    "telegraaf": TelegraafSpider,
    "gva": GVASpider,
    "devolkskrant": DeVolkskrantSpider,
}

def get_spider_by_name(name: str):
    if not name:
        return None

    # Case-insensitive
    return spiders.get(name.lower())

if __name__ == "__main__":
    manager = DatabaseManager()

    # Try to fetch jobs with retries on exception
    max_attempts = 3
    backoff = 0.5
    nr_of_jobs = 2
    interval_between_job_checks = 1800 # Recheck for jobs every 30 minutes
    try:
        while True:
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
                time.sleep(interval_between_job_checks)
                continue
            else:
                # Map jobs to spider classes using spider_map
                spider_classes = []
                for job in jobs:
                    spider = get_spider_by_name(job)
                    spider_classes.append(spider)

                print(spider_classes)

                run_parallel_spiders_for_list(spider_classes)
    
    except KeyboardInterrupt:
        print("Shut down by user.")