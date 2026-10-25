import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata


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

print("Old Testament download complete!")