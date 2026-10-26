
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from standard_works_scraper.config import (
    BOOKS_OF_NT,
    NT_CHAPTER_COUNT,
    NT_BASE_URL,
    NT_DATA_DIR
)

from standard_works_scraper.scrape import (
    scrape_chapter
)



def main():

    collection_name = 'New Testament'
    base_url = NT_BASE_URL
    books = BOOKS_OF_NT
    chapter_counts = NT_CHAPTER_COUNT
    base_path = NT_DATA_DIR

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