from src.util.text_normalizer import tokenize_text, remove_trailing_colon


def extract_from_list(section):
    """
    :param section: html section
    :return: list of text
    """
    return [tokenize_text(item.text) for item in section.findAll('li')]

