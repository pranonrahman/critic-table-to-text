from src.config.log_config import get_logger
from src.util.file_io import read_json

if __name__ == '__main__':
    logger = get_logger()

    logger.info('Started execution')

    data = read_json('../trusted-reviews/resources/data.json')

    logger.info(f'Data size {len(data)}')

    missing_verdict = 0
    pros_count = 0
    cons_count = 0
    spec_count = 0
    missing_lab = 0
    lab_test_count = 0

    for item in data:
        if item.get('verdict', None) is None:
            missing_verdict += 1

        pros_count += len(item.get('pros'))
        cons_count += len(item.get('cons'))

        spec_count += len(item.get('specs').keys())

        if item.get('lab_data', None) is None:
            missing_lab += 1
        else:
            lab_test_count += len(item.get('lab_data').keys())

    logger.info(f'Missing verdicts: {missing_verdict}')

    logger.info(f'Average pros count: {pros_count/len(data)}')
    logger.info(f'Average cons count: {cons_count/len(data)}')
    logger.info(f'Average full spec keys: {spec_count/len(data)}')
    logger.info(f'Missing lab count: {missing_lab}')
    logger.info(f'Average lab test keys: {lab_test_count/(len(data)-missing_lab)}')
