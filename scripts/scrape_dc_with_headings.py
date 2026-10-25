import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

## Doctrine & Covenants

sections = {
    "dc": "Doctrine and Covenants"
}

chapter_counts = {
    "dc": 138
}

base_url = "https://www.churchofjesuschrist.org/study/scriptures/dc-testament"
base_path = "../data/Doctrine and Covenants"

def clean_text(text):
    return unicodedata.normalize("NFKD", text).strip()

def scrape_section(book_slug, book_name, section):
    url = f"{base_url}/{book_slug}/{section}"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200:
        print(f"Failed to fetch {book_name} {section}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # --- SECTION HEADING / INTRO TEXT ---
    heading_container = soup.select_one(".intro")  # Section heading block
    heading_text = ""

    if heading_container:
        heading_paragraphs = heading_container.find_all("p")
        heading_text = "\n\n".join(clean_text(p.get_text()) for p in heading_paragraphs)

    # --- SCRIPTURE BODY ---
    paragraphs = soup.select(".body-block p")
    section_text = "\n\n".join(clean_text(p.get_text()) for p in paragraphs)

    # Create directories
    book_path = os.path.join(base_path, book_name)
    os.makedirs(book_path, exist_ok=True)

    file_path = os.path.join(book_path, f"{book_name} {section}.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {book_name} {section}\n\n")

        if heading_text:
            f.write("## Section Heading\n\n")
            f.write(heading_text)
            f.write("\n\n---\n\n")

        f.write(section_text)

    print(f"Saved: {file_path}")
    time.sleep(1)

for book_slug, book_name in sections.items():
    for section in range(1, chapter_counts[book_slug] + 1):
        scrape_section(book_slug, book_name, section)

print("Doctrine and Covenants download complete!")