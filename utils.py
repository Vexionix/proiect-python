import re


# Function to parse integer represented numerical data on the wikipedia sites, treating special
# cases such as references to other pages in the process.
def parse_wikipedia_number_string_to_int(number_string):
    # Return default value in case no input is provided (shouldn't happen)
    if number_string is None:
        return -1
    # Filter wikipedia references such as "[2]" from the input string
    result = re.sub(r'\[.*?\]', '', number_string)
    # Filter the rest non-numeric characters out
    result = re.sub(r'[^\d]', '', result)
    # Return converted value
    return int(result)


# Function to parse float represented numerical data on the wikipedia sites, treating special
# cases such as references to other pages in the process.
def parse_wikipedia_number_string_to_float(number_string):
    # Return default value in case no input is provided (shouldn't happen)
    if number_string is None:
        return -1
    # Filter all non-numeric characters out except the float separators (, or .)
    result = re.sub(r'[^\d,\.]', '', number_string)
    # Replace "," with "." to allow default conversion of the string to float
    if "." in result and "," in result:
        result = result.replace(".","")
    result = result.replace(',', '.')
    # Return converted value
    return float(result)


# Function use to parse capital text based on the way wikipedia formats strings
# Different formats found are: displaying dates since when the capital has been instated
# or if its temporary or de facto or referencing other pages or empty parenthesis (ex Suedia) etc.
def parse_capital_text(capital):
    # Filter out wikipedia references such as [2]
    result = re.sub(r'\[.*?\]', '', capital)
    # Filter out useless parentheses (such as the date since when a capital has become one)
    result = re.sub(r'\([^)]*?(din|note).*?\)', '', result, flags=re.IGNORECASE)
    # Filter out coordinates
    result = re.sub(r'\d+\.\d+°[NSVE]', '', result)
    result = re.sub(r'\d+°\d+′[NSVE]', '', result)
    # Filter out placeholders (Bolivia {{PAGENAME}})
    result = re.sub(r'\{\{.*?\}\}', '', result)
    # Filter out numbers following letters (remaining references)
    result = re.sub(r'([a-zA-Z])\d+', r'\1', result)
    # Add a space between closing parenthesis and the following letter if it's the case
    result = re.sub(r'\)(\S)', r') \1', result)
    # Filter out empty parenthesis
    result = re.sub(r'\(\s*\)', '', result)
    # Replaces whitespace characters with a single space
    result = re.sub(r'\s+', ' ', result).strip()

    return result