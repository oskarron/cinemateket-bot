from playwright.async_api import async_playwright


async def scrape_showings_at_date(target_date: str):
    """
    Scrape cinema showings for a given date.
    target_date: str in format DD.MM.YYYY
    Returns: dict { title: [ { "date": <date>, "time": <time> }, ... ] }
    """
    url = f"https://www.cinemateket.no/forestillinger?d={target_date}#"
    cinema_name = "cinemateket oslo"
    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("li")  # wait until content loads

        li_elements = await page.query_selector_all("li")

        for li in li_elements:
            title_elem = await li.query_selector("h4")
            time_elem = await li.query_selector("time")

            if not title_elem or not time_elem:
                continue

            title = (await title_elem.inner_text()).strip().lower()
            datetime_attr = (await time_elem.get_attribute("datetime")).strip()

            # Split into date and time if possible
            date_part, time_part = (
                datetime_attr.split("T")
                if "T" in datetime_attr
                else (datetime_attr, "")
            )
            date_part = date_part.strip()
            time_part = time_part.strip()

            if title not in results:
                results[title] = []

            results[title].append(
                {"cinema": cinema_name, "date": date_part, "time": time_part}
            )

        await browser.close()
    return results
