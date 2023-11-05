import json


def read_json(file_path: str):
    """
    :param file_path:
    :return: json file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(json_object: list | dict, file_path: str):
    """
    :param file_path: str
    :param json_object
    :return: None
    """
    json_file = json.dumps(json_object, indent=5)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_file)


def read_list_from_file(file_path: str) -> list:
    """
    :param file_path:
    :return: list
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def write_list_to_file(list_object: list | set, file_path: str):
    """
    :param list_object:
    :param file_path:
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in list_object:
            f.write(item+'\n')