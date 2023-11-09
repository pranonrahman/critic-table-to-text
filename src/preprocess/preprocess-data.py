import random

from sklearn.model_selection import train_test_split

from src.util.file_io import read_json, write_json


def add_shoes_category(item: dict):
    item['category'] = 'shoe'
    return item


def add_device_category(item):
    item['category'] = 'device'
    return item


def remove_lab_data(item):
    if item.get('lab_data', None) is not None:
        item.pop('lab_data')

    return item


def split_and_process_data(run_repeat_data, trusted_reviews_data):
    train_run_repeat, test_run_repeat = train_test_split(run_repeat_data, test_size=0.2, random_state=3)
    train_trusted_review, test_trusted_review = train_test_split(trusted_reviews_data, test_size=0.2, random_state=3)

    test_run_repeat, valid_run_repeat = train_test_split(test_run_repeat, test_size=0.5, random_state=3)
    test_trusted_review, valid_trusted_review = train_test_split(test_trusted_review, test_size=0.5, random_state=3)

    train_data = train_trusted_review + train_run_repeat
    valid_data = valid_trusted_review + valid_run_repeat
    test_data = test_trusted_review + test_run_repeat

    random.shuffle(train_data)
    random.shuffle(valid_data)
    random.shuffle(test_data)

    return train_data, valid_data, test_data


if __name__ == '__main__':
    run_repeat_data = read_json('../../data/preprocessed-data/run-repeat-data-with-lab-specs.json')
    trusted_reviews_data = read_json('../../data/preprocessed-data/trusted-reviews-data-with-lab-specs.json')

    run_repeat_data = list(map(add_shoes_category, run_repeat_data))
    trusted_reviews_data = list(map(add_device_category, trusted_reviews_data))

    run_repeat_data_without_lab_data = list(map(remove_lab_data, run_repeat_data))
    trusted_reviews_data_without_lab_data = list(map(remove_lab_data, trusted_reviews_data))

    train_data_without_lab_data, valid_data_without_lab_data, test_data_without_lab_data = split_and_process_data(
        run_repeat_data_without_lab_data, trusted_reviews_data_without_lab_data)

    run_repeat_data = read_json('../../data/preprocessed-data/run-repeat-data-with-lab-specs.json')
    trusted_reviews_data = read_json('../../data/preprocessed-data/trusted-reviews-data-with-lab-specs.json')

    run_repeat_data = list(map(add_shoes_category, run_repeat_data))
    trusted_reviews_data = list(map(add_device_category, trusted_reviews_data))

    run_repeat_data_only_lab_data = [item for item in run_repeat_data if 'lab_data' in item.keys()]
    trusted_reviews_data_only_lab_data = [item for item in trusted_reviews_data if 'lab_data' in item.keys()]

    train_data_with_lab_data, valid_data_with_lab_data, test_data_with_lab_data = split_and_process_data(
        run_repeat_data_only_lab_data, trusted_reviews_data_only_lab_data)

    print(len(train_data_with_lab_data), len(valid_data_with_lab_data), len(test_data_with_lab_data))
    print(len(train_data_without_lab_data), len(valid_data_without_lab_data), len(test_data_without_lab_data))

    write_json(train_data_without_lab_data, '../../data/without_lab_data/train.json')
    write_json(valid_data_without_lab_data, '../../data/without_lab_data/valid.json')
    write_json(test_data_without_lab_data, '../../data/without_lab_data/test.json')

    write_json(train_data_with_lab_data, '../../data/containing_lab_data/train.json')
    write_json(valid_data_with_lab_data, '../../data/containing_lab_data/valid.json')
    write_json(test_data_with_lab_data, '../../data/containing_lab_data/test.json')

