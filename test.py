from cinemateket_scraper import create_driver, scrape_showings_at_date
import json

if __name__ == "__main__":
    driver = create_driver()

    showings = scrape_showings_at_date(driver, "28.08.2025")
    with open("cinema_showings.json", "w", encoding="utf-8") as f:
        json.dump(showings, f, ensure_ascii=False, indent=4)

    with open("cinema_showings.json", "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    driver.quit()
