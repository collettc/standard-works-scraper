import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

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
