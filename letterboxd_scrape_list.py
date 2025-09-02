from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_watchlist_movies(url):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # use headful for React rendering
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    wait = WebDriverWait(driver, 10)

    driver.get(url)
    all_movies = []

    while True:
        # Wait for the movie items to load
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.react-component[data-item-name]")
            )
        )

        movies = driver.find_elements(
            By.CSS_SELECTOR, "div.react-component[data-item-name]"
        )
        for movie in movies:
            title = movie.get_attribute("data-item-name")
            if title.endswith(")"):
                # split off the last " (" part
                clean_title = title.rsplit(" (", 1)[0]
            else:
                clean_title = title
            all_movies.append(clean_title)

        # Try to find the "Next" button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
            if "disabled" in next_button.get_attribute("class"):
                break  # last page
            next_button.click()
            time.sleep(2)  # wait for the next page to load
        except:
            break  # no next button found, done

    driver.quit()
    return all_movies
