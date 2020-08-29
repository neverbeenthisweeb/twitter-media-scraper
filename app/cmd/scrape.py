import click

from app.service.twitter_scraper.scraper import Scraper


@click.group("scraper")
def scraper_group():
    """
    Commands related to scraper
    """
    pass


@click.command("scrape")
def scrape():
    """
    Scrape twitter media
    """
    twitter_profile = click.prompt("What is your simpee's twitter profile?",
                                   type=str, default="@C_JessiJKT48")
    url = "https://twitter.com/{}".format(twitter_profile)
    media_counts = click.prompt(
        "How many media do you want to scrape?", type=int, default=5)

    scraper = Scraper(url=url, media_counts=media_counts)
    scraper.start()


scraper_group.add_command(scrape)
