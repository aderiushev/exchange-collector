# Requirements:
- Python 3.5
- [pipenv](https://docs.pipenv.org/) used to get and keep the required packages isolated in your env.
Basically it could be done with `pip install pipenv` command
# Installation:
1. clone this repo
2. run `pipenv shell` in the project's root dir
3. run `pipenv install`
4. run `python collect.py --help` to get the list of available command

# Example:
- execute `python collect.py daemon-start --exchange=kraken --pair=XXMRZUSD` to start USD-XMR scraping-daemon
- you can see all the possible daemon options by running `python collect.py daemon-start --help`