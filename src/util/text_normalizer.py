import nltk

nltk.download('punkt')


def remove_trailing_colon(text):
    if len(text.split(':')) == 2:
        return ' '.join(nltk.word_tokenize(text.split(':')[0]))


def tokenize_text(text):
    """
    :param text: str
    :return: tokenized text
    """
    return ' '.join(nltk.word_tokenize(text))
