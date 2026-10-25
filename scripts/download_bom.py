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
    print(url)
    print('getting response - pre')
    response = requests.get(url)
    print('got response - post')
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
    print(book_slug)
    print(book_name)
    for chapter in range(1, chapter_counts[book_slug] + 1):
        print(chapter)
        scrape_chapter(book_slug, book_name, chapter)

print("Book of Mormon download complete!")

## Old Testament

books = {
    "gen": "Genesis"
    ,"ex": "Exodus"
    ,"lev": "Leviticus"
    ,"num": "Numbers"
    ,"deut": "Deuteronomy"
    ,"josh": "Joshua"
    ,"judg": "Judges"
    ,"ruth": "Ruth"
    ,"1-sam": "1 Samuel"
    ,"2-sam": "2 Samuel"
    ,"1-kgs": "1 Kings"
    ,"2-kgs": "2 Kings"
    ,"1-chr": "1 Chronicles"
    ,"2-chr": "2 Chronicles"
    ,"ezra": "Ezra"
    ,"neh": "Nehemiah"
    ,"esth": "Esther"
    ,"job": "Job"
    ,"ps": "Psalms"
    ,"prov": "Proverbs"
    ,"eccl": "Ecclesiastes"
    ,"song": "Song of Solomon"
    ,"isa": "Isaiah"
    ,"jer": "Jeremiah"
    ,"lam": "Lamentations"
    ,"ezek": "Ezekiel"
    ,"dan": "Daniel"
    ,"hosea": "Hosea"
    ,"joel": "Joel"
    ,"amos": "Amos"
    ,"obad": "Obadiah"
    ,"jonah": "Jonah"
    ,"micah": "Micah"
    ,"nahum": "Nahum"
    ,"hab": "Habakkuk"
    ,"zeph": "Zephaniah"
    ,"hag": "Haggai"
    ,"zech": "Zechariah"
    ,"mal": "Malachi"
}

# Number of chapters per book
chapter_counts = {
    "gen": 50
    ,"ex": 40
    ,"lev": 27
    ,"num": 36
    ,"deut": 34
    ,"josh": 24
    ,"judg": 21
    ,"ruth": 4
    ,"1-sam": 31
    ,"2-sam": 24
    ,"1-kgs": 22
    ,"2-kgs": 25
    ,"1-chr": 29
    ,"2-chr": 36
    ,"ezra": 10
    ,"neh": 13
    ,"esth": 10
    ,"job": 42
    ,"ps": 150
    ,"prov": 31
    ,"eccl": 12
    ,"song": 8
    ,"isa": 66
    ,"jer": 52
    ,"lam": 5
    ,"ezek": 48
    ,"dan": 12
    ,"hosea": 14
    ,"joel": 3
    ,"amos": 9
    ,"obad": 1
    ,"jonah": 4
    ,"micah": 7
    ,"nahum": 3
    ,"hab": 3
    ,"zeph": 3
    ,"hag": 2
    ,"zech": 14
    ,"mal": 4
}

# Base URL and save path
base_url = "https://www.churchofjesuschrist.org/study/scriptures/ot"
base_path = "../data/Old Testament"

# Function to clean text (fix weird encoding issues)
def clean_text(text):
    return unicodedata.normalize("NFKD", text)

# Function to scrape and save a chapter
def scrape_chapter(book_slug, book_name, chapter):
    url = f"{base_url}/{book_slug}/{chapter}"
    print(url)
    print('Getting response.')
    response = requests.get(url)
    print('Got response')
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

print("Old Testament download complete!")


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


## Doctrine & Covenants

sections = {
    "dc": "Doctrine and Covenants"
}

# Number of sections in the Doctrine and Covenants
chapter_counts = {
    "dc": 138  # The Doctrine and Covenants has 138 sections
}

# Base URL and save path
base_url = "https://www.churchofjesuschrist.org/study/scriptures/dc-testament"
base_path = "..data//Doctrine and Covenants"

# Function to clean text (fix weird encoding issues)
def clean_text(text):
    return unicodedata.normalize("NFKD", text)

# Function to scrape and save a section
def scrape_section(book_slug, book_name, section):
    url = f"{base_url}/{book_slug}/{section}"
    response = requests.get(url)
    response.encoding = "utf-8"  # Fix encoding issues

    if response.status_code != 200:
        print(f"Failed to fetch {book_name} {section}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract scripture text (without footnotes)
    paragraphs = soup.select(".body-block p")
    section_text = "\n\n".join(clean_text(p.get_text()) for p in paragraphs)

    # Create directories
    book_path = os.path.join(base_path, book_name)
    os.makedirs(book_path, exist_ok=True)

    # Save file
    file_path = os.path.join(book_path, f"{book_name} {section}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {book_name} {section}\n\n{section_text}")

    print(f"Saved: {file_path}")
    time.sleep(1)  # Avoid rate-limiting

# Loop through each section
for book_slug, book_name in sections.items():
    for section in range(1, chapter_counts[book_slug] + 1):
        scrape_section(book_slug, book_name, section)

print("Doctrine and Covenants download complete!")

## Pearl of Great Price

# Sections for the Pearl of Great Price
books = {
    "moses": "Moses",
    "abr": "Abraham",
    "js-m": "Joseph Smith - Matthew",
    "js-h": "Joseph Smith - History",
    "a-of-f": "Articles of Faith"
}

# Number of chapters per book or section
chapter_counts = {
    "moses": 8,                # Moses has 8 chapters
    "abr": 5,              # Abraham has 5 chapters
    "js-m": 1, # Joseph Smith - Matthew has 1 chapter
    "js-h": 1, # Joseph Smith - History has 2 sections
    "a-of-f": 1     # Articles of Faith (book itself is just one document)
}

# Base URL and save path
base_url = "https://www.churchofjesuschrist.org/study/scriptures/pgp"
base_path = "../data/Pearl of Great Price"

# Function to clean text (fix weird encoding issues)
def clean_text(text):
    return unicodedata.normalize("NFKD", text)

# Function to scrape and save a chapter or section
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

# Loop through each book and chapter/section
for book_slug, book_name in books.items():
    for chapter in range(1, chapter_counts[book_slug] + 1):
        scrape_chapter(book_slug, book_name, chapter)

print("Pearl of Great Price download complete!")

