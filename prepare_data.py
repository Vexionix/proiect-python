from create_database import create_database
from scraper import scrape_wikipedia

# Create the database if it doesn't exist
create_database()
# Start scraping process as well as inserting entries as it goes on
# Only add countries that are not already found in the database
scrape_wikipedia()
