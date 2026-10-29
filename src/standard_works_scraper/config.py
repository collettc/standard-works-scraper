from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
EXPORT_DIR = DATA_DIR / 'exports'
BOFM_DATA_DIR = EXPORT_DIR / 'bofm'
OT_DATA_DIR = EXPORT_DIR / 'ot'
NT_DATA_DIR = EXPORT_DIR / 'nt'
DC_DATA_DIR = EXPORT_DIR / 'dc'
PGP_DATA_DIR = EXPORT_DIR / 'pgp'
GC_DATA_DIR = EXPORT_DIR / 'gc'


# Base URLs
BOFM_BASE_URL = 'https://www.churchofjesuschrist.org/study/scriptures/bofm'
OT_BASE_URL = 'https://www.churchofjesuschrist.org/study/scriptures/ot'
NT_BASE_URL = 'https://www.churchofjesuschrist.org/study/scriptures/nt' 
DC_BASE_URL = 'https://www.churchofjesuschrist.org/study/scriptures/dc-testament'
PGP_BASE_URL = 'https://www.churchofjesuschrist.org/study/scriptures/pgp'


# Book reference
BOOKS_OF_BOFM = {
    "1-ne": "1 Nephi"
    , "2-ne": "2 Nephi"
    , "jacob": "Jacob"
    , "enos": "Enos"
    , "jarom": "Jarom"
    , "omni": "Omni"
    , "w-of-m": "Words of Mormon"
    , "mosiah": "Mosiah"
    , "alma": "Alma"
    , "hel": "Helaman"
    , "3-ne": "3 Nephi"
    , "4-ne": "4 Nephi"
    , "morm": "Mormon"
    , "ether": "Ether"
    , "moro": "Moroni"
}

BOOKS_OF_OT = {
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

BOOKS_OF_NT = {
    "matt": "Matthew"
    ,"mark": "Mark"
    ,"luke": "Luke"
    ,"john": "John"
    ,"acts": "Acts"
    ,"rom": "Romans"
    ,"1-cor": "1 Corinthians"
    ,"2-cor": "2 Corinthians"
    ,"gal": "Galatians"
    ,"eph": "Ephesians"
    ,"phil": "Philippians"
    ,"col": "Colossians"
    ,"1-thess": "1 Thessalonians"
    ,"2-thess": "2 Thessalonians"
    ,"1-tim": "1 Timothy"
    ,"2-tim": "2 Timothy"
    ,"titus": "Titus"
    ,"phm": "Philemon"
    ,"heb": "Hebrews"
    ,"james": "James"
    ,"1-pet": "1 Peter"
    ,"2-pet": "2 Peter"
    ,"1-john": "1 John"
    ,"2-john": "2 John"
    ,"3-john": "3 John"
    ,"jude": "Jude"
    ,"rev": "Revelation"
}

SECTIONS_OF_DC = {
    'dc': 138
}

BOOKS_OF_DC = {
    'dc': 'Doctring and Covenants'
}

BOOKS_OF_PGP = {
    "moses": "Moses",
    "abr": "Abraham",
    "js-m": "Joseph Smith - Matthew",
    "js-h": "Joseph Smith - History",
    "a-of-f": "Articles of Faith"
}

# Chapter Counts
BOFM_CHAPTER_COUNT = {
    "1-ne": 22
    , "2-ne": 33
    , "jacob": 7
    , "enos": 1
    , "jarom": 1
    , "omni": 1
    , "w-of-m": 1
    , "mosiah": 29
    , "alma": 63
    , "hel": 16
    , "3-ne": 30
    , "4-ne": 1
    , "morm": 9
    , "ether": 15
    , "moro": 10
}

OT_CHAPTER_COUNT = {
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

NT_CHAPTER_COUNT= {
    "matt": 28
    ,"mark": 16
    ,"luke": 24
    ,"john": 21
    ,"acts": 28
    ,"rom": 16
    ,"1-cor": 16
    ,"2-cor": 13
    ,"gal": 6
    ,"eph": 6
    ,"phil": 4
    ,"col": 4
    ,"1-thess": 5
    ,"2-thess": 3
    ,"1-tim": 6
    ,"2-tim": 4
    ,"titus": 3
    ,"phm": 1
    ,"heb": 13
    ,"james": 5
    ,"1-pet": 5
    ,"2-pet": 3
    ,"1-john": 5
    ,"2-john": 1
    ,"3-john": 1
    ,"jude": 1
    ,"rev": 22
}

PGP_CHAPTER_COUNT = {
    "moses": 8,
    "abr": 5,
    "js-m": 1,
    "js-h": 1,
    "a-of-f": 1,
}

# General Conference variables

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

