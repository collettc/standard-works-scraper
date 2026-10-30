from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from standard_works_scraper.config import (
    GC_DATA_DIR,
    HEADERS
)

from standard_works_scraper.scrape import (
    get_conference_data,
    get_talk_links,
    scrape_talk
)

def main():
    year = 2026
    month = 4  # Keep as integer 4
    
    # Use :02d inside the f-string to pad with a leading zero in the URL
    GC_BASE_URL = f'https://www.churchofjesuschrist.org/study/general-conference/{year}/{month:02d}?lang=eng'
    
    if month == 10:
        month_label = 'October General Conference'
    elif month == 4:
        month_label = 'April General Conference'

    output_path = f'{GC_DATA_DIR}/{year} {month_label}'

    print(f"Fetching {year}-{month:02d} General Conference...")
    conference_date = get_conference_data(year, month)

    talk_links = get_talk_links(GC_BASE_URL, HEADERS, year, f'{month:02d}')
    print(f"Found {len(talk_links)} talks.")

    for link in talk_links:
        scrape_talk(link, conference_date, HEADERS, output_path)

    print("Download complete.")
    
    return None

if __name__ == '__main__':
    main()