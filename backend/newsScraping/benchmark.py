from time import perf_counter
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from newsScraping.spiders.DeStandaard import DeStandaardSpider
from newsScraping.spiders.vrtNws import VrtNwsSpider
from newsScraping.spiders.DeMorgen import DeMorgenSpider
from newsScraping.spiders.Nieuwsblad import NieuwsbladSpider
from newsScraping.spiders.HBVL import HBVLSpider
from newsScraping.spiders.Telegraaf import TelegraafSpider
from newsScraping.spiders.GVA import GVASpider
from newsScraping.spiders.DeVolkskrant import DeVolkskrantSpider

spiders = [VrtNwsSpider, DeStandaardSpider, DeMorgenSpider, NieuwsbladSpider, HBVLSpider, TelegraafSpider, GVASpider, DeVolkskrantSpider]

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

def run_parallel_spiders():
    processes = []
    for spider in spiders:
        p = multiprocessing.Process(target=run_single_spider, args=(spider,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

def run_benchmark_spiders(task, iterations):
    times = []
    for _ in range(iterations):
        start_time = perf_counter()
        p = multiprocessing.Process(target=task)
        p.start()
        p.join()
        end_time = perf_counter()
        times.append(end_time - start_time)
    return times

def visualize(benchmark_results):
    alg_names = ['Sequential', 'Parallel']
    plt.figure(figsize=(8, 5))
    plt.bar(alg_names, benchmark_results, color=['#4C72B0', '#55A868'])
    plt.ylabel('Average Runtime (s)')
    plt.title('Average Runtime per Method')
    plt.show()

def run_benchmark(iterations: int):
    seq_res = run_benchmark_spiders(run_spiders, iterations)
    par_res = run_benchmark_spiders(run_parallel_spiders, iterations)
    # Sequential benchmark
    print(f"Sequential times: {seq_res}")
    print(f"Total scraping time: {sum(seq_res)} seconds")
    print(f"Average scraping time: {np.mean(seq_res)} seconds")

    # Parallel benchmark
    print(f"Parallel times: {par_res}")
    print(f"Total scraping time: {sum(par_res)} seconds")
    print(f"Average scraping time: {np.mean(par_res)} seconds")

    visualize([np.mean(seq_res), np.mean(par_res)])

if __name__ == "__main__":
    iterations = 30
    run_benchmark(iterations)