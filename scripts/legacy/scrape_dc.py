import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

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