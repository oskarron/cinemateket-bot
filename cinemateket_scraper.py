from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


# obsoloony
def scrape_cinemateket_frontpage(driver):
    # --- SCRAPE MOVIE BLOCKS ---
    blocks = driver.find_elements(
        By.XPATH, '//div[contains(@class,"page-shows__section-block")]'
    )

    cinema_dict = {}  # key: movie title, value: list of {"date": ..., "time": ...}

    for block in blocks:
        date = block.get_attribute("data-block-date")
        movies = block.find_elements(By.CSS_SELECTOR, "ul li a")

        for movie in movies:
            try:
                title = movie.find_element(By.TAG_NAME, "h4").text

            except:
                title = "Unknown title"

            try:
                time_of_day = movie.find_element(By.CSS_SELECTOR, ".time").text

            except:
                time_of_day = "Unknown time"

            if title not in cinema_dict:
                cinema_dict[title] = []

            cinema_dict[title].append({"date": date, "time": time_of_day})

    driver.quit()
    return cinema_dict


def scrape_showings_at_date(driver, target_date: str):
    url = f"https://www.cinemateket.no/forestillinger?d={target_date}#"
    driver.get(url)
    time.sleep(2)  # wait for JS to load

    cinema_dict = {}  # key: movie title, value: list of {"datetime": ..., "time_text": ...}

    # Get all <li> elements on the page
    li_elements = driver.find_elements(By.TAG_NAME, "li")

    for li in li_elements:
        try:
            title_elem = li.find_element(By.TAG_NAME, "h4")
            time_elem = li.find_element(By.TAG_NAME, "time")
        except:
            # Skip <li> that don't have h4 or time
            continue

        cinema_name = "cinemateket oslo"

        title = (
            title_elem.text.strip().lower()
        )  # store title in lowercase for consistency
        datetime_attr = time_elem.get_attribute("datetime").strip()

        # Initialize nested structure if needed
        if title not in cinema_dict:
            cinema_dict[title] = {}
        if cinema_name not in cinema_dict[title]:
            cinema_dict[title][cinema_name] = []

        # Append datetime to the list for this cinema
        cinema_dict[title][cinema_name].append(datetime_attr)

    return cinema_dict
