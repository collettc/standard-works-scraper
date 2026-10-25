import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

## Book of Mormon

# Book names for URLs vs. formal names for saving
books = {
    "1-ne": "1 Nephi"
    , "2-ne": "2 Nephi"
    , "jacob": "Jacob"
    , "enos": "Enos"
    , "jarom": "Jarom"
    , "omni": "Omni"
    , "w-of-m": "Words of Mormon"
    , "mosiah": "Mosiah"
    , "alma": "Alma"
    , "hel": "Helaman"
    , "3-ne": "3 Nephi"
    , "4-ne": "4 Nephi"
    , "morm": "Mormon"
    , "ether": "Ether"
    , "moro": "Moroni"
}

# Number of chapters per book
chapter_counts = {
    "1-ne": 22
    , "2-ne": 33
    , "jacob": 7
    , "enos": 1
    , "jarom": 1
    , "omni": 1
    , "w-of-m": 1
    , "mosiah": 29
    , "alma": 63
    , "hel": 16
    , "3-ne": 30
    , "4-ne": 1
    , "morm": 9
    , "ether": 15
    , "moro": 10
}

# Base URL and save path
base_url = "https://www.churchofjesuschrist.org/study/scriptures/bofm"
base_path = "../data/Book of Mormon"

# Function to clean text (fix weird encoding issues)
def clean_text(text):
    return unicodedata.normalize("NFKD", text)

# Function to scrape and save a chapter
def scrape_chapter(book_slug, book_name, chapter):
    url = f"{base_url}/{book_slug}/{chapter}"
    response = requests.get(url)
    response.encoding = "utf-8"  # Fix encoding issues

    if response.status_code != 200:
        print(f"Failed to fetch {book_name} {chapter}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract scripture text (without footnotes)
    paragraphs = soup.select(".body-block p")
    chapter_text = "\n\n".join(clean_text(p.get_text()) for p in paragraphs)

    # Create directories
    book_path = os.path.join(base_path, book_name)
    os.makedirs(book_path, exist_ok=True)

    # Save file
    file_path = os.path.join(book_path, f"{book_name} {chapter}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {book_name} {chapter}\n\n{chapter_text}")

    print(f"Saved: {file_path}")
    time.sleep(1)  # Avoid rate-limiting

# Loop through each book and chapter
for book_slug, book_name in books.items():
    for chapter in range(1, chapter_counts[book_slug] + 1):
        scrape_chapter(book_slug, book_name, chapter)

print("Book of Mormon download complete!")