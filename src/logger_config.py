import logging

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler("./logs/etl.log")
    file_handler.setFormatter(format)

    logger.addHandler(file_handler)

    return logger