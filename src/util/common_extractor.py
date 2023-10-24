from src.util.text_normalizer import tokenize_text, remove_trailing_colon


def extract_from_list(section):
    """
    :param section: html section
    :return: list of text
    """
    return [tokenize_text(item.text) for item in section.findAll('li')]


def extract_from_table(section):
    """
    :param section: html selection
    :return: json where key is first column and value is second column of each row
    """
    table_data = dict()

    for row in section.find_all('tr'):
        key = remove_trailing_colon(tokenize_text(row.find_all('th')[0].text))
        value = tokenize_text(row.find_all('td')[0].text)

        if key and value:
            table_data[key] = value

    return table_data

