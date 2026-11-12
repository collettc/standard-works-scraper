"""Scraping helpers for the Come, Follow Me manual."""

import re
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

from standard_works_scraper.config import (
    CFM_CONTENTS_URL,
    CFM_CURRICULUM,
    CFM_DATA_DIR,
    CFM_MANUAL_PATH,
    HEADERS,
)


def clean_cfm_text(text: str) -> str:
    """Normalize text while retaining meaningful paragraph boundaries."""
    text = unicodedata.normalize("NFKC", text).replace("\xa0", " ")
    text = re.sub(r"[\u200b-\u200d\ufeff]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def get_cfm_chapters() -> list[tuple[int, str, str, str]]:
    """Return numbered weekly lesson URLs and labels from the manual index."""
    response = requests.get(CFM_CONTENTS_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    chapters = []
    seen_urls = set()
    month_names = (
        "January|February|March|April|May|June|July|August|September|"
        "October|November|December"
    )
    week_label = re.compile(
        rf"^(?:{month_names})\s+\d{{1,2}}\s*[–—-]\s*"
        rf"(?:(?:{month_names})\s+)?\d{{1,2}}(?:\s*:\s*|\s)",
        re.IGNORECASE,
    )
    date_prefix = re.compile(
        rf"^(?:{month_names})\s+\d{{1,2}}\s*[–—-]\s*"
        rf"(?:(?:{month_names})\s+)?\d{{1,2}}\s*:?\s*",
        re.IGNORECASE,
    )
    scripture_reference = re.compile(
        r"\b(?:Matthew|Mark|Luke|John|Acts|Romans|Corinthians|Galatians|"
        r"Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|"
        r"Philemon|Hebrews|James|Peter|Jude|Revelation)\b",
        re.IGNORECASE,
    )

    for link in soup.select("a[href]"):
        href = link["href"].split("#", 1)[0]
        absolute_url = urljoin(CFM_CONTENTS_URL, href)
        parsed = urlsplit(absolute_url)
        if not parsed.path.startswith(f"{CFM_MANUAL_PATH}/"):
            continue
        if parsed.path.endswith("/000-spine"):
            continue

        english_url = urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, "lang=eng", "")
        )
        label = clean_cfm_text(link.get_text(" "))
        if label and week_label.match(label) and english_url not in seen_urls:
            remainder = date_prefix.sub("", label, count=1)
            quoted_title = re.search(r"[“\"]([^”\"]+)[”\"]", remainder)
            if quoted_title:
                lesson_title = quoted_title.group(1).strip()
            else:
                scripture_start = scripture_reference.search(remainder)
                lesson_title = remainder[:scripture_start.start()].strip() if scripture_start else ""
            chapters.append((len(chapters) + 1, english_url, label, lesson_title))
            seen_urls.add(english_url)

    return chapters


def scrape_cfm_chapter(week_number: int, url: str, filename_title: str = "") -> None:
    """Save one manual chapter as a Markdown file."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    if response.status_code != 200:
        print(f"Failed to fetch {url}: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    title_tag = soup.select_one(".body-block h1") or soup.find("h1")
    title = clean_cfm_text(title_tag.get_text(" ")) if title_tag else "Untitled"
    body = soup.select_one(".body-block")

    parts = []
    if body:
        for block in body.find_all(["h2", "h3", "h4", "h5", "h6", "p"]):
            text = clean_cfm_text(block.get_text(" "))
            if not text:
                continue
            if block.name.startswith("h"):
                parts.append(f"{'#' * int(block.name[1])} {text}")
            else:
                parts.append(text)

    if not parts:
        print(f"No article body found: {url}")
        return

    safe_title = (filename_title or title).replace(";", ",").replace(":", " - ")
    safe_title = re.sub(r"[\u2010-\u2015]", " - ", safe_title)
    safe_title = re.sub(r"[\\/*?\"<>|]", "", safe_title)
    safe_title = re.sub(r"\s+", " ", safe_title).strip(" .")
    CFM_DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path: Path = CFM_DATA_DIR / f"Week {week_number} - {safe_title or 'Untitled'}.md"
    content = (
        "---\n"
        "type: lesson\n"
        f'curriculum: "[[{CFM_CURRICULUM}]]"\n'
        f"link: {url}\n"
        "tags:\n"
        "---\n\n"
        f"# {title}\n\n"
        + "\n\n".join(parts)
    )
    file_path.write_text(content, encoding="utf-8")
    print(f"Saved: {file_path}")
    time.sleep(1)
