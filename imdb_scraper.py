import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.imdb.com/chart/top/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def scrape_top_chart():
    resp = requests.get(URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    movies = []
    rows = soup.select('table.chart.full-width tr')
    for row in rows:
        title_col = row.select_one('td.titleColumn a')
        if not title_col:
            continue

        title = title_col.text.strip()
        link = "https://www.imdb.com" + title_col["href"].split("?")[0]
        year_span = row.select_one("td.titleColumn span.secondaryInfo")
        year = int(year_span.text.strip("()")) if year_span else None
        rating_col = row.select_one("td.ratingColumn.imdbRating strong")
        rating = float(rating_col.text.strip()) if rating_col else None

        movies.append({
            "title": title,
            "year": year,
            "rating": rating,
            "link": link
        })

        time.sleep(0.05)

    df = pd.DataFrame(movies)
    df.to_csv("imdb_top250_sample.csv", index=False)
    print(f"Saved imdb_top250_sample.csv with {len(df)} rows")

if __name__ == "__main__":
    scrape_top_chart()