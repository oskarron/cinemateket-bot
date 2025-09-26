from playwright.async_api import async_playwright


async def get_watchlist_movies(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        all_movies = []

        while True:
            # Wait for movies to appear
            await page.wait_for_selector("div.react-component[data-item-name]")
            movies = await page.query_selector_all(
                "div.react-component[data-item-name]"
            )

            for movie in movies:
                title = await movie.get_attribute("data-item-name")
                if title.endswith(")"):
                    clean_title = title.rsplit(" (", 1)[0].lower()
                else:
                    clean_title = title.lower()
                all_movies.append(clean_title)

            # Try to click next button
            try:
                next_button = await page.query_selector("a.next")
                disabled = await next_button.get_attribute("class")
                if "disabled" in disabled:
                    break
                await next_button.click()
                await page.wait_for_timeout(2000)
            except:
                break

        await browser.close()
    return all_movies
