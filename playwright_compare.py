from playwright_cinemateket import scrape_showings_at_date
from playwright_watchlist import get_watchlist_movies


async def compare():
    """Return a list of matching movies currently showing at the cinema."""
    kioskarURL = "https://letterboxd.com/kioskar/list/test/"
    watchlist_titles = await get_watchlist_movies(kioskarURL)

    # Normalize watchlist titles (strip & lower just in case)
    watchlist_titles = [t.strip().lower() for t in watchlist_titles]

    cinema_movies = await scrape_showings_at_date("25.09.2025")

    matches = []
    for movie_title, showings in cinema_movies.items():
        normalized_title = movie_title.strip().lower()
        if normalized_title in watchlist_titles:
            for showing in showings:
                matches.append(
                    f"'{movie_title}' is showing at {showing['cinema']} on {showing['date']} at {showing['time']}"
                )

    return matches
