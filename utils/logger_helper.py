import logging
import os


def setup_test_logger(test_name):
    """Логгер на каждый тест, пишет в файл logs/<test>.log"""
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.isdir(logs_dir):
        os.makedirs(logs_dir)

    safe_name = test_name.replace("/", "_").replace("[", "").replace("]", "")
    log_path = os.path.join(logs_dir, safe_name + ".log")

    logger = logging.getLogger("test." + safe_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # дублируем в api логгер
    api_log = logging.getLogger("api.students")
    api_log.setLevel(logging.DEBUG)
    api_log.handlers.clear()
    api_log.addHandler(fh)

    return logger, log_path
