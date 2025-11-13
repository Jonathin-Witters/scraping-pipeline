from dataclasses import dataclass, asdict
from abc import abstractmethod
from datetime import date, datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup

@dataclass
class Document:
    title: str
    date: date
    author: str
    url: str
    source: str
    first_lines: str
    thumbnail: str  # URL to image
    tags: List[str]
    content: str = ""

    def to_json(self) -> Dict[str, Any]:
        data = asdict(self)

        # Convert non-safe types
        if isinstance(self.date, date):
            data["date"] = self.date.isoformat()

        return data

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Document":
        raw_date = data.get("date")
        if isinstance(raw_date, str):
            try:
                parsed_date = datetime.fromisoformat(raw_date).date()
            except ValueError:
                parsed_date = date.today()
        elif isinstance(raw_date, date):
            parsed_date = raw_date
        else:
            parsed_date = date.today()

        tags = data.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]

        return cls(
            title=data.get("title", ""),
            date=parsed_date,
            author=data.get("author", ""),
            url=data.get("url", ""),
            source=data.get("source", ""),
            first_lines=data.get("first_lines", ""),
            thumbnail=data.get("thumbnail", ""),
            tags=tags,
            content=data.get("content", ""),
        )

class ArticleParser():
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> Document:
        """Fetch and parse an article from the given URL."""
        pass