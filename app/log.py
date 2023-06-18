import logging

def init_log(
    name: str = "app", log_level: str = "INFO"
) -> None:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(log_level)
