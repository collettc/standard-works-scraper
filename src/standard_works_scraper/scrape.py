import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import unicodedata
import re
from datetime import datetime

def clean_text(text:str) -> str:
    """Normalize text"""
    return unicodedata.normalize('NFKD', text)

def scrape_chapter(
    base_url:str,
    base_path:str,
    book_slug:str, 
    book_name:str, 
    chapter:str
    ) -> None:
    """
    Extract text from url

    Args:
        base_url (str): Base URL for library
        base_path (str): Export directory
        book_slug (str): Constructed URL to ping
        book_name (str): Unique URL addition for book
        chapter (str): Unique URL addition for chapter
    """

    url = f'{base_url}/{book_slug}/{chapter}'
    print(url)
    print('getting_response - pre')
    response = requests.get(url)
    print('got response - post')
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f'Failed to fetch {book_name} {chapter}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text without footnotes
    paragraphs = soup.select('.body-block p')
    chapter_text = '\n\n'.join(clean_text(p.get_text()) for p in paragraphs)
    
    # Create directories
    book_path = os.path.join(base_path, book_name)
    os.makedirs(book_path, exist_ok=True)
    
    # Save file
    file_path = os.path.join(book_path, f'{book_name} {chapter}.md')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'#  {book_name} {chapter}\n\n{chapter_text}')

    print(f'Saved: {file_path}')
    time.sleep(1) # Avoid rate-limiting


def clean_general_conference_text(text:str) -> str:
    """
    Clean general conference text coming from website

    Args:
        text (str): Text to be cleaned

    Returns:
        str: Cleaned text
    """

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_speaker_name(raw_name:str) -> str:
    """
    Normalize the name of the general conference speaker

    Args:
        raw_name (str): raw text

    Returns:
        str: cleaned text
    """


    name = raw_name.replace("By ", "")

    # Remove titles
    name = re.sub(r"^(Elder|President|Sister|Brother|Bishop)\s+", "", name)

    # Remove calling descriptions
    name = re.sub(r"\s+Of the.*", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+of the.*", "", name, flags=re.IGNORECASE)

    name = re.sub(r"\s+", " ", name)

    return name.strip()

def get_conference_data(year:int, month:int) -> str:

    for day in range(1,8):
        date = datetime(int(year), month, day)
        if date.weekday() == 6: # Sunday
            return date.strftime('%Y-%m-%d')
        
    return f'{year}-{month}-01'

def get_talk_links(
    conf_url:str, 
    headers:dict,
    year:int,
    month:int,
    ) -> list:
    response = requests.get(conf_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href'].split('?')[0]

        if f'/study/general-conference/{year}/{month}/' in href:
            full_url = 'https://www.churchofjesuschrist.org' + href
            if full_url not in links:
                links.append(full_url)
                
    return links

def scrape_talk(url:str, 
                conf_date,
                headers:dict,
                base_path:str,
                )-> None:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # ---- Title ----
    title_tag = soup.find("h1")
    title = clean_general_conference_text(title_tag.get_text()) if title_tag else "Untitled"

    # ---- Speaker ----
    speaker_tag = soup.select_one(".byline")
    raw_speaker = clean_general_conference_text(speaker_tag.get_text()) if speaker_tag else "Unknown"
    speaker = normalize_speaker_name(raw_speaker)

    # ---- Body (Preserve ALL Headers + Paragraphs in Order) ----
    body_container = soup.select_one(".body-block")

    body_parts = []

    if body_container:
        content_blocks = body_container.find_all(["h2", "p"])

        for block in content_blocks:

            # Prevent word merging
            for tag in block.find_all():
                tag.insert_after(" ")

            raw_text = block.get_text()
            cleaned = clean_general_conference_text(raw_text)

            if not cleaned:
                continue

            # Section headers
            if block.name == "h2":
                body_parts.append(f"## {cleaned}")

            # Paragraphs
            elif block.name == "p":
                body_parts.append(cleaned)

    body_text = "\n\n".join(body_parts)


    # ---- YAML FRONTMATTER ----
    frontmatter = f"""---
type: talk
curriculum: "[[General Conference]]"

speaker: "[[{speaker}]]"
link: {url}
date: "[[{conf_date}]]"
tags:
---
"""

    md_content = f"{frontmatter}\n# {title}\n\n{body_text}"

    # ---- Save File ----
    os.makedirs(base_path, exist_ok=True)

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    file_path = os.path.join(base_path, safe_title + ".md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Saved: {file_path}")
    time.sleep(1)