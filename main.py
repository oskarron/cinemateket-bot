from letterboxd_scrape_list import get_watchlist_movies
from cinemateket_scraper import scrape_cinemateket_frontpage
import json


def compare():
    """Return a list of matching movies currently showing at the cinema."""
    # 1️⃣ Get watchlist titles
    kioskarURL = "https://letterboxd.com/kioskar/watchlist/"
    watchlist_titles = get_watchlist_movies(kioskarURL)
    watchlist_titles_lower = [t.lower() for t in watchlist_titles]
    print(watchlist_titles_lower)

    # 2️⃣ Get cinema movies
    cinema_movies = (
        scrape_cinemateket_frontpage()
    )  # dict: {title: [{"date":..., "time":...}, ...]}

    # 3️⃣ Compare and collect matches
    matches = []
    for movie_title, showings in cinema_movies.items():
        print("cinemateket tittel:", movie_title)
        if movie_title.lower() in watchlist_titles_lower:
            for showing in showings:
                matches.append(
                    f"'{movie_title}' is showing at {showing['date']} {showing['time']}"
                )

    return matches  # <-- return results instead of printing


with open("cinema_showings.json", "r", encoding="utf-8") as f:
    cinema_data = json.load(f)

# Print it prettily
print(json.dumps(cinema_data, ensure_ascii=False, indent=4))
