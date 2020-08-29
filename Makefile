#!make

include .env
export

scrape:
	@python main.py scraper scrape