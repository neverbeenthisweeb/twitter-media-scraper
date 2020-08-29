tech stack:
* python 3.8.2 (formatter: autopep8, linter: flake8)
* pip 20.0.2
* chrome driver (default: 83.0.4103.39, at the end it should match your chrome version)

how to install:
1) clone repo
2) copy `.env.example` and suit it to your own `cp .env.example .env` (later, edit this `.env` to match your config)
2) download python dependencies `pip install -r requirements.txt`
3) run scraper `make run-scraper`

demo:

![demoo](https://user-images.githubusercontent.com/42462215/91636704-e2a2c480-ea2c-11ea-802a-dee299d615c9.png)

notes:
* make sure you have the correct chrome driver version (see here for [download](https://sites.google.com/a/chromium.org/chromedriver/downloads))
* path for downloaded file and chrome driver is configurable (see `.env.example`)
* make sure your waifu twitter is not private

todo:
* tidy up readme
* add support for downloading videos
* implement threading when downloading media
* replace print statement with logging