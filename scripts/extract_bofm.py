
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from standard_works_scraper.config import (
    BOOKS_OF_BOFM,
    BOFM_CHAPTER_COUNT,
    BOFM_BASE_URL,
    BOFM_DATA_DIR
)

from standard_works_scraper.scrape import (
    scrape_chapter
)



def main():

    collection_name = 'Book of Mormon'
    base_url = BOFM_BASE_URL
    books = BOOKS_OF_BOFM
    chapter_counts = BOFM_CHAPTER_COUNT
    base_path = BOFM_DATA_DIR

    for book_slug, book_name in books.items():
        print(book_slug)
        print(book_name)
        for chapter in range(1, chapter_counts[book_slug]+1):
            print(chapter)
            scrape_chapter(
                base_url,
                base_path,
                book_slug, 
                book_name, 
                chapter)
    print(f'{collection_name} download complete.')
    
    return None

if __name__=='__main__':
    main()