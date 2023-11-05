from src.util.text_normalizer import tokenize_text, remove_trailing_colon


def extract_from_list(section):
    """
    :param section: html section
    :return: list of text
    """
    if section is None:
        return []

    return [tokenize_text(item.text) for item in section.findAll('li')]


def make_key_value_pair(keys, values):
    data = {}
    for key, value in zip(keys, values):
        data[key.get_text(strip=True)] = value.get_text(strip=True)

    return data
