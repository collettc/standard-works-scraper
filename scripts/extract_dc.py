from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from standard_works_scraper.config import (
    DC_BASE_URL,
    DC_DATA_DIR,
    SECTIONS_OF_DC,
)
from standard_works_scraper.scrape import scrape_chapter


def main() -> None:
    collection_name = "Doctrine and Covenants"

    for section_slug, section_count in SECTIONS_OF_DC.items():
        print(section_slug)
        for section in range(1, section_count + 1):
            print(section)
            scrape_chapter(
                DC_BASE_URL,
                DC_DATA_DIR,
                section_slug,
                collection_name,
                section,
            )

    print(f"{collection_name} download complete.")


if __name__ == "__main__":
    main()
