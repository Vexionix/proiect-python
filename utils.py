import re


def parse_wikipedia_number_string_to_int(number_string):
    """
    Function to parse integer represented numerical data on the wikipedia sites, treating special
    cases such as references to other pages in the process.
    More specifically used for area
    :param number_string: A string containing a numerical value (specifically country's area)
    :return: The integer resulted from converting the given string
    """

    # Return default value in case no input is provided (shouldn't happen)
    if number_string is None:
        return -1
    # Filter out wikipedia references such as [2]
    number_string = re.sub(r'\[.*?\]', '', number_string)
    match = re.search(r'([\d., ]+)\s*km²', number_string)
    if match:
        result = match.group(1)
    else:
        return -1
    parts = result.split()
    result = ''.join([parts[0]] + [part for part in parts[1:] if len(part) == 3])
    if "." in result and "," in result:
        result = result.split(',')[0]
    result = result.replace('.', '').replace(',', '').replace(' ', '')
    # Return converted value
    return int(result)


def parse_population_string_to_int(number_string):
    """
    Function to parse population number string to an int
    :param number_string: The string containing the population number
    :return The integer representation of the value after conversion
    """

    # Return default value in case no input is provided (shouldn't happen)
    if number_string is None:
        return -1
    result = number_string.replace('.', '').replace(',', '').replace(' ', '')
    # Return converted value
    return int(result)


def parse_wikipedia_number_string_to_float(number_string):
    """
    Function to parse float represented numerical data on the wikipedia sites, treating special
    cases such as references to other pages in the process.
    More specifically used to parse the density value
    :param number_string: The string that's supposed to contain a float number
    :return: The float number resulted from the conversion of the given string
    """

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
    result = re.sub(r'\s+\d+\s+', '', result)
    # Replace "," with "." to allow default conversion of the string to float
    if "." in result and "," in result:
        result = result.replace(".","")
    result = result.replace(',', '.')
    # Return converted value
    return float(result)


def parse_capital_text(capital):
    """
    Function use to parse capital text based on the way wikipedia formats strings
    Different formats found are: displaying dates since when the capital has been instated
    or if its temporary or de facto or referencing other pages or empty parenthesis (ex Suedia) etc.
    :param capital: Capital text string from wikipedia's country page infobox
    :return: parsed capital text string, only containing the necessary information
    """

    # Filter out coordinates
    result = re.sub(r'\d+\.\d+°[NSVE]', '', capital)
    result = re.sub(r'\d+°\d+′[NSVE]', '', result)
    # Filter out useless parentheses (such as the date since when a capital has become one)
    result = re.sub(r'\([^)]*?(din|note).*?\)', '', result, flags=re.IGNORECASE)
    # Filter out placeholders (Bolivia {{PAGENAME}})
    result = re.sub(r'\{\{.*?\}\}', '', result)
    # Add a space between closing parenthesis and the following letter if it's the case
    result = re.sub(r'\)(\S)', r') \1', result)
    # Filter out empty parenthesis
    result = re.sub(r'\(\s*\)', '', result)
    # Parse with general parsing
    result = general_parse(result)

    return result


def parse_neighbors_text(neighbors):
    """
    Function use to parse neighbors text based on the way wikipedia formats strings
    and removing data that is not deemed necessary
    :param neighbors: the text containing the list of neighbors of the country extracted from the wikipedia page
    :return: the parsed value removing useless characters - the clean string
    """

    # Pre-parse with general parsing
    result = general_parse(neighbors)
    # Add " / " between neighbors
    result = re.sub(r'([a-z])([A-Z])', r'\1 / \2', result)

    return result


def parse_languages_text(languages):
    """
    Function use to parse languages text based on the way wikipedia formats strings
    and removing data that is not deemed necessary
    :param languages: the text containing the list of languages spoken in the country
    extracted from the wikipedia page
    :return: the parsed value removing useless characters - the clean string
    """

    # Pre-parse with general parsing
    result = general_parse(languages)
    # Fix spacing for commas
    result = re.sub(r'\s*,\s*', r', ', result)
    # Add space between languages if missing
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', result)
    # Remove commas if they are the last character
    result = re.sub(r',\s*$', '', result)
    # Remove remaining references
    result = re.sub(r'([a-z])(?: \d+| [¹-⁰]+)', r'\1', result)

    return result


def parse_timezone(timezone):
    """
    Function to parse timezone (From example from "UTC - 3" to "UTC-3"
    :param timezone: the time zone of the country extracted from the wikipedia page
    :return: the parsed value removing useless characters - the clean string
    """

    result = general_parse(timezone)
    # Remove spaces around '+'
    result = re.sub(r'\s*\+\s*', '+', result)
    # Remove spaces around '-'
    result = re.sub(r'\s*-\s*', '-', result)

    return result


def general_parse(value):
    """
    Function use to parse most text based on the way wikipedia formats strings
    and removing data that is not deemed necessary
    :param value: the value (string) to be parsed
    :return clean string after parsing (this method is composed of the most
    required adjustments for the way the strings are received upon the calls
    to the wikipedia page
    """

    # Filter out wikipedia references such as [2]
    result = re.sub(r'\[.*?\]', '', remove_diacritics(value))
    # Filter out zero width space
    result = re.sub(r'[\u200B\uFEFF]', '', result)
    # Filter out numbers following letters (remaining references)
    result = re.sub(r'([a-z])(?: \d+ | [¹-⁰]+ |\d+|[¹-⁰]+)', r'\1', result)
    # Replace multiple whitespaces with a single space
    result = re.sub(r'\s+', ' ', result).strip()

    return result


def remove_diacritics(string):
    """
    Function to remove diacritics from string
    :param string: the string to be cleaned
    :return: the cleaned string
    """

    string = re.sub(r'[ăâ]', 'a', string)
    string = re.sub(r'[ĂÂ]', 'A', string)
    string = re.sub(r'[î]', 'i', string)
    string = re.sub(r'[Î]', 'i', string)
    string = re.sub(r'[ș]', 's', string)
    string = re.sub(r'[ÎȘ]', 's', string)
    string = re.sub(r'[ț]', 't', string)
    string = re.sub(r'[Ț]', 't', string)

    return string