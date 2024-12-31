import requests
from bs4 import BeautifulSoup
import sqlite3

# Establish connection with the database to save the scraped data
# in the countries table
conn = sqlite3.connect('states_of_the_world.db')
cursor = conn.cursor()


# Scrape the searched data for each country found in the table. It first gets each row of
# the table and then parses the content to get the link to each country's page which
# then scrapes again to get the desired data such as name, population etc. I chose to
# extract the data in romanian, but I could also have used the english wikipedia page
# just as well, possibly needing slight adjustments in logic (such as treating svg links).
def scrape_wikipedia():
    base_url = "https://ro.wikipedia.org"
    countries_table_url = "https://ro.wikipedia.org/wiki/Lista_țărilor_după_populație"
    response = requests.get(countries_table_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select("table.wikitable tbody tr")

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) > 2:
            name_link = cols[1].find('a')
            if name_link and '.svg' in name_link['href']:
                name_link = name_link.findNext('a')
            if not name_link:
                continue

            name = name_link.text.strip()
            country_url = base_url + name_link['href']
            print(name + ' - ' + country_url)


scrape_wikipedia()
