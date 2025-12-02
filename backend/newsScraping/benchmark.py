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

def visualize_boxplot(seq_res, par_res):
    plt.figure(figsize=(8, 5))
    plt.boxplot([seq_res, par_res], labels=["Sequential", "Parallel"])
    plt.ylabel("Runtime (s)")
    plt.title("Runtime Distribution per Method")
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
    visualize_boxplot(seq_res, par_res)

if __name__ == "__main__":
    iterations = 30
    run_benchmark(iterations)

# Results:
# resultsSequential times: [23.626118415995734, 21.673146790999454, 21.205485790997045, 23.126512332994025, 22.556135791994166, 21.428416000009747, 22.28065683398745, 21.75242912498652, 21.22254591700039, 21.519486250006594, 21.940987458016025, 23.636160958005348, 21.44708795801853, 21.38007795799058, 21.66545674999361, 21.261695166991558, 21.482931457983796, 20.70558925002115, 21.428023582993774, 21.361957125016488, 21.68478829099331, 21.332889499986777, 20.949695582996355, 21.567138415994123, 21.693591917020967, 21.21318487499957, 21.667167625011643, 21.97927024998353, 21.65316487502423, 21.28790629201103]
# Total scraping time: 651.7296985380235 seconds
# Average scraping time: 21.724323284600782 seconds
# Parallel times: [10.431813041010173, 10.07098158399458, 11.95580479199998, 12.3039501660096, 9.53071533300681, 9.90062412500265, 9.909137208014727, 10.24562750000041, 9.410556290997192, 11.323562834004406, 11.593255250016227, 9.284883124986663, 9.908456375007518, 9.369293584022671, 9.452995334024308, 14.872982333006803, 11.933713124977658, 10.410692834004294, 9.904907541000284, 9.481279500003438, 9.138920124998549, 9.461785292020068, 9.371127790975152, 9.752690666995477, 13.753375415981282, 10.546589666017098, 9.74182516700239, 9.632359999988694, 9.578060375002678, 9.861835584015353]
# Total scraping time: 312.13380195808713 seconds
# Average scraping time: 10.404460065269571 seconds