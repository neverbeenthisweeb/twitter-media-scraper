import click

from app.cmd.scrape import scraper_group


@click.group()
def main_group():
    """Twitter Media Scraper"""


main_group.add_command(scraper_group)


if __name__ == "__main__":
    main_group()
