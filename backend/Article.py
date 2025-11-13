from dataclasses import dataclass, field
from abc import abstractmethod
from datetime import date
from typing import List
from bs4 import BeautifulSoup


@dataclass
class Document:
    title: str
    date: date
    author: str
    url: str
    source: str
    first_lines: str
    thumbnail: str # url to image
    tags: List[str]
    content: str = ""

class ArticleParser():
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> Document:
        """Fetch and parse an article from the given URL."""
        pass