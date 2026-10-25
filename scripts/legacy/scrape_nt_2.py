import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

# New Testament books
books = {
    "matt": "Matthew",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "rom": "Romans",
    "1-cor": "1 Corinthians",
    "2-cor": "2 Corinthians",
    "gal": "Galatians",
    "eph": "Ephesians",
    "phil": "Philippians",
    "col": "Colossians",
    "1-thess": "1 Thessalonians",
    "2-thess": "2 Thessalonians",
    "1-tim": "1 Timothy",
    "2-tim": "2 Timothy",
    "titus": "Titus",
    "phm": "Philemon",
    "heb": "Hebrews",
    "james": "James",
    "1-pet": "1 Peter",
    "2-pet": "2 Peter",
    "1-john": "1 John",
    "2-john": "2 John",
    "3-john": "3 John",
    "jude": "Jude",
    "rev": "Revelation"
}

chapter_counts = {
    "matt": 28,
    "mark": 16,
    "luke": 24,
    "john": 21,
    "acts": 28,
    "rom": 16,
    "1-cor": 16,
    "2-cor": 13,
    "gal": 6,
    "eph": 6,
    "phil": 4,
    "col": 4,
    "1-thess": 5,
    "2-thess": 3,
    "1-tim": 6,
    "2-tim": 4,
    "titus": 3,
    "phm": 1,
    "heb": 13,
    "james": 5,
    "1-pet": 5,
    "2-pet": 3,
    "1-john": 5,
    "2-john": 1,
    "3-john": 1,
    "jude": 1,
    "rev": 22
}

base_url = "https://www.churchofjesuschrist.org/study/scriptures/nt"
base_path = "../data/New Testament"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ScriptureScraper/1.0)"
}

def clean_text(text):
    """Normalize unicode text and strip extra spaces."""
    return unicodedata.normalize("NFKD", text).strip()

def get_chapter_url(book_slug, chapter):
    """Determine the correct URL for a chapter."""
    single_chapter = ["phm", "2-john", "3-john", "jude"]
    short_first_chapter = ["2-thess"]

    # Single-chapter books or short epistles first chapter
    if chapter_counts[book_slug] == 1 or (chapter == 1 and book_slug in single_chapter + short_first_chapter):
        return f"{base_url}/{book_slug}"
    return f"{base_url}/{book_slug}/{chapter}"

def scrape_chapter(book_slug, book_name, chapter):
    """Scrape a chapter and save as Markdown with headings."""
    url = get_chapter_url(book_slug, chapter)
    response = requests.get(url, headers=HEADERS)
    response.encoding = "utf-8"

    if response.status_code != 200:
        print(f"Failed to fetch {book_name} {chapter} (status {response.status_code})")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    body_blocks = soup.select(".body-block")
    if not body_blocks:
        print(f"Warning: {book_name} {chapter} returned empty content!")
        return

    # Build Markdown text with headings
    chapter_text = ""
    for block in body_blocks:
        for child in block.children:
            # Skip anything that isn't a tag
            if not hasattr(child, "name"):
                continue

            # Paragraphs
            if child.name == "p":
                chapter_text += clean_text(child.get_text()) + "\n\n"

            # Headings
            elif child.name in ["h2", "h3"] or (child.get("class") and "heading" in child.get("class", [])):
                heading_text = clean_text(child.get_text())
                chapter_text += f"## {heading_text}\n\n"

    # Save Markdown file
    book_path = os.path.join(base_path, book_name)
    os.makedirs(book_path, exist_ok=True)

    file_path = os.path.join(book_path, f"{book_name} {chapter}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {book_name} {chapter}\n\n{chapter_text}")

    print(f"Saved: {file_path}")
    time.sleep(1)  # Be nice to the server

# Main scraping loop
for book_slug, book_name in books.items():
    if chapter_counts[book_slug] == 1:
        scrape_chapter(book_slug, book_name, 1)
    else:
        for chapter in range(1, chapter_counts[book_slug] + 1):
            scrape_chapter(book_slug, book_name, chapter)

print("New Testament download complete!")
