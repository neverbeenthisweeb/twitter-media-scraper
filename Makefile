#!make

include .env
export

run-scraper:
	@python main.py scraper scrape