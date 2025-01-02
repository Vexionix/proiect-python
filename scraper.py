import requests
from bs4 import BeautifulSoup
import sqlite3
from utils import (parse_wikipedia_number_string_to_int,
                   parse_population_string_to_int,
                   parse_density_string_to_int,
                   parse_capital_text,
                   parse_languages_text,
                   parse_neighbors_text,
                   parse_timezone,
                   general_parse)

# Establish connection with the database to save the scraped data
# in the countries table
conn = sqlite3.connect('states_of_the_world.db')
cursor = conn.cursor()


def scrape_wikipedia():
    """
    Scrape the searched data for each country found in the table. It first
    gets each row of the table and then parses the content to get the link
    to each country's page which then scrapes again to get the desired data
    such as name, population etc. The data is extracted from the romanian
    wikipedia site.
    """
    # Prepare the base url used when concatenating it with the
    # href link of each country using romanian version of wikipedia
    base_url = "https://ro.wikipedia.org"
    # Link to the table containing the top of countries sorted by
    # population from where the name of the country, the population
    # as well as the link to each country's page can be extracted
    # to get more details for each entry
    countries_table_url = (
        "https://ro.wikipedia.org/wiki/Lista_țărilor_după_populație")
    # Make the http request to the wikipedia page
    response = requests.get(countries_table_url)
    # Parse the received content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get each row of the table found on the page with all the countries
    rows = soup.select("table.wikitable tbody tr")

    # Go through each of the rows and extract the data accordingly
    for row in rows[1:]:
        # Get each cell of the current row containing data
        # such as "Name", "Population"
        cols = row.find_all('td')
        if len(cols) > 2:
            # name_link will contain the link to the
            # country if successful, for example it extracts
            # the <a href="...">China</a> field for China
            name_link = cols[1].find('a')
            # Extra check in case of having a link to an image
            # prior to the country name as it is an inconsistent
            # thing, some countries do have this, others don't
            if name_link and '.svg' in name_link['href']:
                name_link = name_link.findNext('a')
            # If nothing was found to fit our search criterion
            # we skip to the next row
            if not name_link:
                continue

            # If the previous step was successful, extract the
            # country name from the name_link field
            name = name_link.text.strip()

            # Fix wrong link for Jersey (special case)
            if name_link['href'] == "/wiki/Jersey":
                name_link['href'] = "/wiki/Insula_Jersey"

            # Fix wrong link for Sfanta Lucia (special case)
            if name_link['href'] == "/wiki/Sf%C3%A2nta_Lucia":
                name_link['href'] = "/wiki/Sf%C3%A2nta_Lucia_(stat)"

            # Build the url to the current row's country's page
            country_url = base_url + name_link['href']

            # Check if the country is already added in the
            # database before proceeding with scraping
            cursor.execute(
                '''SELECT COUNT(*) FROM countries
                WHERE name = ?''', (name,))
            existing_entry = cursor.fetchone()[0]
            if existing_entry == 0:

                # As the data is saved in string format,
                # extract as a string first and then
                # convert to integer if possible, but
                # the data is consistent here
                population_as_string = cols[2].text.strip().replace(".", "")
                population = parse_population_string_to_int(
                    population_as_string)

                # Get all data from the current page and
                # store it in its respective variable
                (area,
                 density,
                 capital,
                 neighbors,
                 languages,
                 timezone,
                 regime) = scrape_country_details(country_url)

                # If no density was found calculate it manually
                # with a formula that provides an approximate result
                if density == -1.0:
                    if area != -1:
                        density = round(population / area, 1)

                # Insert the found data in the created database table
                cursor.execute(
                    '''INSERT INTO countries
                    (name,
                    capital,
                    population,
                    density,
                    area,
                    neighbors,
                    languages,
                    timezone,
                    regime)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name,
                     capital,
                     population,
                     density,
                     area,
                     neighbors,
                     languages,
                     timezone,
                     regime))
                print(f"Added country to table - {name}")
            else:
                print(f"The country {name} already exists in the database.")

        conn.commit()


def scrape_country_details(url):
    """
    Extract data from each country's page that is not found in the
    main table page. The method works for romanian wikipedia country
    pages, as it looks for specific keywords found in those. It looks
    in the information box found in the upper right of the page, a
    table marked as "infocaseta" where most crucial information is
    found. Some countries miss some datas and as such have default values
    :param url: The URL of the country's wikipedia page for which the method
    will scrape details
    :return: The details of the country after scraping data or default values
    if none were found
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract the information box on the upper right side of the wikipedia page
    infobox = soup.find('table', {'class': 'infocaseta'})

    # Set default values to the fields
    (area,
     density,
     capital,
     neighbors,
     languages,
     timezone,
     regime) = -1, -1.0, "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"
    # Variable used for keeping old title with the purpose of
    # checking if the row is adjacent to the area field in the table
    # due to the way the country data is displayed in romanian wikipedia pages
    old_row_title = None

    if infobox:
        # Select each row of the extracted table
        rows = infobox.find_all('tr')

        for row in rows:
            # Use both th and td to get matching search criteria,
            # inline elements that have both a subtitle next to
            # them and descriptive text next to them
            # (example: "Suprafata    494.595km^2")
            # Select each of the searched element based on matching
            # title of the searched criterion, if the title is
            # "densitate" then "density" should take the value
            # found in the td element proceeding the header (th)
            th = row.find('th')
            td = row.find('td')

            if th and td:
                # Extract the title of the current entry (row in the table)
                key = th.get_text(
                    strip=True).lower()

                # For each of the searched field try to match
                # the expected title to the current row one and
                # take the value describing the row and save it
                # in the respective variable
                if 'total' in key and "suprafață" in old_row_title:
                    value = td.get_text().strip()
                    area = parse_wikipedia_number_string_to_int(value.strip())
                elif 'densitate' in key:
                    value = td.get_text().strip()
                    density = round(
                        parse_density_string_to_int(
                            value.strip()), 1)
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
                    timezone = parse_timezone(value)
                elif 'sistem politic' in key:
                    value = td.get_text().strip()
                    regime = general_parse(value)

                # Save the previous row title
                # (specifically for area, because the data is displayed as
                # "Suprafata
                #  - Total(a)          (value)"
                # But looking for "total" is not enough because there are
                # multiple rows that can fit this criterion and as such
                # lead to errors
                old_row_title = key

    # Return the found values or the default ones for
    # the fields that did not have a corresponding
    # information box row to extract data from
    return area, density, capital, neighbors, languages, timezone, regime
