import os
import logging

def setup_logger():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "../data/app.log")

    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if logger.handlers:
        logger.handlers = []
    logger.addHandler(file_handler)

    return logger

if __name__ == '__main__':
    logger = setup_logger()
    logger.info('Hello World')