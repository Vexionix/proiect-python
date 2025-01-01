import requests
from bs4 import BeautifulSoup
import sqlite3
import utils
from utils import parse_wikipedia_number_string_to_int, parse_wikipedia_number_string_to_float, parse_capital_text, \
    parse_neighbors_text, parse_languages_text, parse_regime_text, parse_timezone_text

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

            if name_link['href'] == "/wiki/Jersey":
                name_link['href'] = "/wiki/Insula_Jersey"

            if name_link['href'] == "/wiki/Sf%C3%A2nta_Lucia":
                name_link['href'] = "/wiki/Sf%C3%A2nta_Lucia_(stat)"

            country_url = base_url + name_link['href']

            population_as_string = cols[2].text.strip().replace(".", "")
            population = int(population_as_string) if population_as_string.isdigit() else None

            area, density, capital, neighbors, languages, timezone, regime = scrape_country_details(country_url)

            if density == -1.0:
                if area != -1:
                    density = round(population / area,1)

            cursor.execute('''SELECT COUNT(*) FROM countries WHERE name = ?''', (name,))
            existing_entry = cursor.fetchone()[0]

            if existing_entry == 0:
                cursor.execute('''INSERT INTO countries (name, capital, population, density, area, neighbors, languages, timezone, regime)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (name, capital, population, density, area, neighbors, languages, timezone, regime))
                print(f"Added country to table - {name}")
            else:
                print(f"The country {name} already exists in the database.")

        conn.commit()


def scrape_country_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    infobox = soup.find('table', {'class': 'infocaseta'})

    # Set default values to the fields
    area, density, capital, neighbors, languages, timezone, regime = -1, -1.0, "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"
    # Variable used for keeping old title with the purpose of
    # checking if the row is adjacent to the area field in the table
    # due to the way the country data is displayed in romanian wikipedia pages
    old_row_title = None

    if infobox:
        rows = infobox.find_all('tr')

        for row in rows:
            th = row.find('th')
            td = row.find('td')

            if th and td:
                key = th.get_text(
                    strip=True).lower()

                if 'total' in key and "Suprafață" in old_row_title:
                    value = td.get_text().strip()
                    area = parse_wikipedia_number_string_to_int(value.strip())
                elif 'densitate' in key:
                    value = td.get_text().strip()
                    density = round(parse_wikipedia_number_string_to_float(value.strip()), 1)
                elif 'capitala' in key:
                    value = td.get_text().strip()
                    capital = parse_capital_text(value)
                elif 'vecini' in key:
                    value = td.get_text().strip()
                    neighbors = parse_neighbors_text(value)
                elif 'limbi oficiale' in key:
                    value = td.get_text(separator=" ").strip()
                    languages = parse_languages_text(value)
                elif 'fus orar' in key:
                    value = td.get_text(separator=" ").strip()
                    timezone = parse_timezone_text(value)
                elif 'sistem politic' in key:
                    value = td.get_text().strip()
                    regime = parse_regime_text(value)

                old_row_title = th.get_text()

    return area, density, capital, neighbors, languages, timezone, regime


scrape_wikipedia()
