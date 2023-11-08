import requests
import logging
import utils
import cceyes
from cceyes.models import Production, ProductionDataset, ProductionMeta, ProductionReviews
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def find_popular_shows(number=100):
    start = 0
    all_tv_shows = []

    while start < number:
        url = f"https://api.betaseries.com/shows/list?limit=100&order=popularity&locale=en&start={start}"
        response = requests.get(url, headers=utils.headers)
        tv_shows = response.json()['shows']

        if not tv_shows:
            break

        if number < 100:
            tv_shows = tv_shows[:number]

        all_tv_shows.extend(tv_shows)
        start += 100

    return all_tv_shows


def create_meta(tv_show):
    popularity = 0
    followers = int(tv_show['followers'])

    if followers > 10000:
        popularity = 10
    elif followers > 5000:
        popularity = 9
    elif followers > 1000:
        popularity = 8
    elif followers > 500:
        popularity = 7
    elif followers > 100:
        popularity = 6
    elif followers > 50:
        popularity = 5
    elif followers > 10:
        popularity = 4
    elif followers > 5:
        popularity = 3
    elif followers > 1:
        popularity = 2
    elif followers > 0:
        popularity = 1

    # Fetch the TV series details
    return {
        'id': str(tv_show['id']),
        'title': tv_show['title'],
        'image': tv_show['images']['poster'],
        'reviews': {
            'rating': float(tv_show['notes']['mean']),
            'count': int(tv_show['notes']['total']),
            'popularity': popularity,
        }
    }


def create_content(tv_show):
    # Fetch the TV series details including the synopsis
    content = f"{tv_show['title']}: {tv_show['description']}"

    # Limit to 1000 characters
    return content[:1000]


def main():
    log = logging.getLogger("rich")
    log.info(cceyes.providers.datasets().text)

    with Progress(
        SpinnerColumn(),
        TimeElapsedColumn(),
        BarColumn(),
        TimeRemainingColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        global_progress = progress.add_task("[red]Fetching TV Series…")
        tv_shows = find_popular_shows(3000)
        progress.update(global_progress, total=len(tv_shows))
        productions = []

        for tv_show in tv_shows:
            log.debug(tv_show['title'])

            progress.update(global_progress, advance=0.1, description=tv_show['title'])

            meta = create_meta(tv_show)
            progress.update(global_progress, advance=0.2)

            content = create_content(tv_show)
            progress.update(global_progress, advance=0.2)

            # Add the production to the list
            productions.append(Production(
                title=meta["title"],
                content=content,
                dataset=ProductionDataset(
                    type='TV Series',
                    provider='BetaSeries',
                ),
                meta=ProductionMeta(
                    id=meta["id"],
                    title=meta["title"],
                    image=meta['image'],
                    publication_year=tv_show['creation'],
                    reviews=ProductionReviews(
                        rating=meta['reviews']['rating'],
                        count=meta['reviews']['count'],
                        popularity=meta['reviews']['popularity'],
                    )
                ),
            ))

            progress.update(global_progress, advance=0.2)

            # If we have 100 productions, send them to the API
            if len(productions) == 100:
                response = cceyes.providers.upsert(productions)
                log.debug(response.text)

                progress.update(global_progress, advance=0.3*10)
                productions = []

        response = cceyes.providers.upsert(productions)
        log.debug(response.text)

        progress.update(global_progress, advance=len(tv_shows))


if __name__ == "__main__":
    main()
