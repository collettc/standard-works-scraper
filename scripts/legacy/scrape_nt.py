import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

# New Testament
books = {
    "matt": "Matthew"
    ,"mark": "Mark"
    ,"luke": "Luke"
    ,"john": "John"
    ,"acts": "Acts"
    ,"rom": "Romans"
    ,"1-cor": "1 Corinthians"
    ,"2-cor": "2 Corinthians"
    ,"gal": "Galatians"
    ,"eph": "Ephesians"
    ,"phil": "Philippians"
    ,"col": "Colossians"
    ,"1-thess": "1 Thessalonians"
    ,"2-thess": "2 Thessalonians"
    ,"1-tim": "1 Timothy"
    ,"2-tim": "2 Timothy"
    ,"titus": "Titus"
    ,"phm": "Philemon"
    ,"heb": "Hebrews"
    ,"james": "James"
    ,"1-pet": "1 Peter"
    ,"2-pet": "2 Peter"
    ,"1-john": "1 John"
    ,"2-john": "2 John"
    ,"3-john": "3 John"
    ,"jude": "Jude"
    ,"rev": "Revelation"
}

# Number of chapters per book
chapter_counts = {
    "matt": 28
    ,"mark": 16
    ,"luke": 24
    ,"john": 21
    ,"acts": 28
    ,"rom": 16
    ,"1-cor": 16
    ,"2-cor": 13
    ,"gal": 6
    ,"eph": 6
    ,"phil": 4
    ,"col": 4
    ,"1-thess": 5
    ,"2-thess": 3
    ,"1-tim": 6
    ,"2-tim": 4
    ,"titus": 3
    ,"phm": 1
    ,"heb": 13
    ,"james": 5
    ,"1-pet": 5
    ,"2-pet": 3
    ,"1-john": 5
    ,"2-john": 1
    ,"3-john": 1
    ,"jude": 1
    ,"rev": 22
}

# Base URL and save path
base_url = "https://www.churchofjesuschrist.org/study/scriptures/nt"
base_path = "../data/New Testament"

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

print("New Testament download complete!")