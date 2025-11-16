from pathlib import Path

import scrapy

# Data Model:

# Document {
# title: string
# date: date
# author: string
# url: url
# source: string
# first_lines: string
# thumbnail: img (/url)
# tags: string[]
# content: string
# } 


class NieuwsbladSpider(scrapy.Spider):
    name = "nieuwsblad"
    start_urls = [
        "https://www.nieuwsblad.be"
    ]

    custom_settings = {
        'FEEDS': {
            'data/nieuwsblad.json': {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf8'
            }
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for teaser in response.css('article'):
            article_url = teaser.css('a::attr(href)').get()
            yield response.follow(article_url, self.parse_article)

        page = response.url.split("/")[-2] or "index"
        filename = f"nieuwsblad-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

    def parse_article(self, response):
        yield {
            "title": response.css('h1[class="Heading_heading__g_Vyj Heading_heading--2xl__XYmSS story-headline_storyHeadlineHeading__3WzwH"]::text').get(),
            "date": response.css('time::attr(datetime)').get(),
            "author": response.css('p[data-testid="author-name"]::text').get(),
            "url": response.url,
            "source": "Nieuwsblad",
            "first_lines": response.css('h2[class="Paragraph_paragraph__nQNQ9 Paragraph_paragraph--default-sm-strong__IZ8XV articleParagraph story-intro_storyIntro__7SJ5Q"]::text').get(),
            "thumbnail": response.css('img::attr(srcset)').get().split(',')[0],
            "tags": response.css('a[data-testid="article-tag"]::text').getall(),
            "content": response.css('p[class="Paragraph_paragraph__nQNQ9 Paragraph_paragraph--default-sm-default__bs4Xa articleParagraph"]::text').getall(),
        }
        
        