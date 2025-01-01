import re


# Function to parse integer represented numerical data on the wikipedia sites, treating special
# cases such as references to other pages in the process.
def parse_wikipedia_number_string_to_int(number_string):
    # Return default value in case no input is provided (shouldn't happen)
    if number_string is None:
        return -1
    # Filter out wikipedia references such as [2]
    number_string = re.sub(r'\[.*?\]', '', number_string)
    match = re.search(r'(\d[\d., ]*)\s*km²', number_string)
    if match:
        result = match.group(1)
    else:
        return -1
    result = result.replace('.', '').replace(',', '').replace(' ', '')
    # Return converted value
    return int(result)


# Function to parse float represented numerical data on the wikipedia sites, treating special
# cases such as references to other pages in the process.
def parse_wikipedia_number_string_to_float(number_string):
    # Return default value in case no input is provided (shouldn't happen)
    if number_string is None:
        return -1
    # Filter out wikipedia references such as [2]
    number_string = re.sub(r'\[.*?\]', '', number_string)
    # Select only the number found prior to loc/km^2
    match = re.search(r'(\d[\d., ]*)\s*loc/km²', number_string)
    if match:
        result = match.group(1)
    else:
        return -1
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
    result = re.sub(r'([a-zăâîșțA-ZĂÂÎȘȚ]) \d+', r'\1', result)
    result = re.sub(r'([a-zăâîșțA-ZĂÂÎȘȚ]) [¹-⁰]', r'\1', result)
    # Add a space between closing parenthesis and the following letter if it's the case
    result = re.sub(r'\)(\S)', r') \1', result)
    # Filter out empty parenthesis
    result = re.sub(r'\(\s*\)', '', result)
    # Replaces whitespace characters with a single space
    result = re.sub(r'\s+', ' ', result).strip()

    return result


def parse_neighbors_text(neighbors):
    # Filter out wikipedia references such as [2]
    result = re.sub(r'\[.*?\]', '', neighbors)
    # Filter out numbers following letters (remaining references)
    result = re.sub(r'([a-zăâîșțA-ZĂÂÎȘȚ]) \d+', r'\1', result)
    result = re.sub(r'([a-zăâîșțA-ZĂÂÎȘȚ]) [¹-⁰]', r'\1', result)
    # Add " / " between neighbors
    result = re.sub(r'([a-zăâîșț])([A-ZĂÂÎȘȚ])', r'\1 / \2', result)
    # Replace multiple whitespaces with a single space
    result = re.sub(r'\s+', ' ', result).strip()

    return result


def parse_languages_text(languages):
    # Filter out wikipedia references such as [2]
    result = re.sub(r'\[.*?\]', '', languages)
    # Fix spacing for commas
    result = re.sub(r'\s*,\s*', r', ', result)
    # Filter out numbers following letters (remaining references)
    result = re.sub(r'([a-zăâîșțA-ZĂÂÎȘȚ]) \d+', r'\1', result)
    result = re.sub(r'([a-zăâîșțA-ZĂÂÎȘȚ]) [¹-⁰]', r'\1', result)
    # Add space between languages if missing
    result = re.sub(r'([a-zăâîșț])([A-ZĂÂÎȘȚ])', r'\1 \2', result)
    # Replace multiple whitespaces with a single space
    result = re.sub(r'\s+', ' ', result).strip()
    # Remove commas if they are the last character
    result = re.sub(r',\s*$', '', result)

    return result

