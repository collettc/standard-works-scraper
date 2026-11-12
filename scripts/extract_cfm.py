"""Download the chapters in the 2026 Come, Follow Me Old Testament manual."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from standard_works_scraper.cfm import get_cfm_chapters, scrape_cfm_chapter


def main() -> None:
    chapters = get_cfm_chapters()
    print(f"Found {len(chapters)} manual chapters.")
    for week_number, url, label, lesson_title in chapters:
        print(f"Week {week_number}: {label}")
        scrape_cfm_chapter(week_number, url, lesson_title)
    print("Come, Follow Me download complete.")


if __name__ == "__main__":
    main()
