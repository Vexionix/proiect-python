import re


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


def parse_wikipedia_number_string_to_float(number_string):
    # Filter all non-numeric characters out except the float separators (, or .)
    result = re.sub(r'[^\d,\.]', '', number_string)
    # Replace "," with "." to allow default conversion of the string to float
    result = result.replace(',', '.')
    # Return converted value
    return float(result)