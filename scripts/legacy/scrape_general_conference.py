import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata
import re
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================
YEAR = "2026"
MONTH = "10"  # "04" = April, "10" = October

BASE_CONF_URL = f"https://www.churchofjesuschrist.org/study/general-conference/{YEAR}/{MONTH}?lang=eng"
BASE_PATH = f"../data/General Conference/{YEAR}-{MONTH}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ==============================
# TEXT CLEANING
# ==============================
def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ==============================
# SPEAKER NORMALIZATION
# ==============================
def normalize_speaker_name(raw_name):
    name = raw_name.replace("By ", "")

    # Remove titles
    name = re.sub(r"^(Elder|President|Sister|Brother|Bishop)\s+", "", name)

    # Remove calling descriptions
    name = re.sub(r"\s+Of the.*", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+of the.*", "", name, flags=re.IGNORECASE)

    name = re.sub(r"\s+", " ", name)

    return name.strip()


# ==============================
# CONFERENCE DATE (First Sunday)
# ==============================
def get_conference_date():
    month_num = int(MONTH)

    for day in range(1, 8):
        date = datetime(int(YEAR), month_num, day)
        if date.weekday() == 6:  # Sunday
            return date.strftime("%Y-%m-%d")

    return f"{YEAR}-{MONTH}-01"


# ==============================
# GET TALK LINKS
# ==============================
def get_talk_links(conf_url):
    response = requests.get(conf_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].split("?")[0]

        if f"/study/general-conference/{YEAR}/{MONTH}/" in href:
            full_url = "https://www.churchofjesuschrist.org" + href
            if full_url not in links:
                links.append(full_url)

    return links


# ==============================
# SCRAPE SINGLE TALK
# ==============================
def scrape_talk(url, conf_date):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # ---- Title ----
    title_tag = soup.find("h1")
    title = clean_text(title_tag.get_text()) if title_tag else "Untitled"

    # ---- Speaker ----
    speaker_tag = soup.select_one(".byline")
    raw_speaker = clean_text(speaker_tag.get_text()) if speaker_tag else "Unknown"
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
            cleaned = clean_text(raw_text)

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
    os.makedirs(BASE_PATH, exist_ok=True)

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    file_path = os.path.join(BASE_PATH, safe_title + ".md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Saved: {file_path}")
    time.sleep(1)


# ==============================
# MAIN
# ==============================
print(f"Fetching {YEAR}-{MONTH} General Conference...")
conference_date = get_conference_date()

talk_links = get_talk_links(BASE_CONF_URL)
print(f"Found {len(talk_links)} talks.")

for link in talk_links:
    scrape_talk(link, conference_date)

print("Download complete.")
