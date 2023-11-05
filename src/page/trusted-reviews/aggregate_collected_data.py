from src.config.log_config import get_logger
from src.util.file_io import read_json, write_json

if __name__ == '__main__':
    logger = get_logger()

    logger.info('Started execution')

    data_1 = read_json('../trusted-reviews/resources/data_5000.json')
    data_2 = read_json('../trusted-reviews/resources/data_10000.json')
    data_3 = read_json('../trusted-reviews/resources/data_15000.json')

    logger.info(f'Len of each data: data1: {len(data_1)} data2: {len(data_2)} data3: {len(data_3)}')

    data = data_1 + data_2 + data_3

    logger.info(f'After concat, len of data: {len(data)}')

    write_json(data, '../trusted-reviews/resources/data.json')
