from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_DIR = Path(__file__).resolve().parent


def required_text(element: BeautifulSoup | None, selector: str) -> str:
    selected = element.select_one(selector) if element else None
    if selected is None:
        raise ValueError(f"Required page element is missing: {selector}")
    text = selected.get_text(" ", strip=True)
    if not text:
        raise ValueError(f"Required page element is empty: {selector}")
    return text


def scrape() -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    quotes: list[dict[str, object]] = []
    author_urls: dict[str, str] = {}
    visited_pages: set[str] = set()
    page_url = BASE_URL

    with requests.Session() as session:
        while page_url:
            if page_url in visited_pages:
                raise ValueError(f"Pagination loop detected at {page_url}")
            visited_pages.add(page_url)

            response = session.get(page_url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            quote_cards = soup.select(".quote")
            if not quote_cards:
                raise ValueError(f"No quotes found on {page_url}")

            for card in quote_cards:
                author_element = card.select_one(".author")
                if author_element is None:
                    raise ValueError("A quote is missing its author")
                author_name = author_element.get_text(strip=True)
                author_link = author_element.find_next("a", href=True)
                if author_link is None:
                    raise ValueError(f"Author profile link is missing: {author_name}")

                keywords = card.select_one(".keywords")
                tags = (
                    [tag.strip() for tag in keywords.get("content", "").split(",") if tag.strip()]
                    if keywords
                    else []
                )
                quotes.append(
                    {
                        "tags": tags,
                        "author": author_name,
                        "quote": required_text(card, ".text"),
                    }
                )
                author_urls[author_name] = urljoin(BASE_URL, author_link["href"])

            next_link = soup.select_one("li.next a[href]")
            page_url = urljoin(BASE_URL, next_link["href"]) if next_link else ""

        authors: list[dict[str, str]] = []
        for author_name, author_url in author_urls.items():
            response = session.get(author_url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            profile_name = required_text(soup, ".author-title")

            authors.append(
                {
                    "fullname": profile_name,
                    "born_date": required_text(soup, ".author-born-date"),
                    "born_location": required_text(soup, ".author-born-location"),
                    "description": required_text(soup, ".author-description"),
                }
            )

    return quotes, authors


def main() -> None:
    quotes, authors = scrape()
    (OUTPUT_DIR / "qoutes.json").write_text(
        json.dumps(quotes, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "authors.json").write_text(
        json.dumps(authors, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {len(quotes)} quotes and {len(authors)} authors.")


if __name__ == "__main__":
    main()
