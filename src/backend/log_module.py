import logging
from logging.handlers import RotatingFileHandler
import time
from functools import wraps

# 日志配置参数
LOG_FILENAME = 'app.log'
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

logger = logging.getLogger('APP')
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = RotatingFileHandler(
        LOG_FILENAME,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )

    formatter = logging.Formatter(
        '%(asctime)s|%(name)s|%(levelname)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log_function(func):
    """装饰器：记录方法的进入时间、传入参数、离开时间和返回结果"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Entering: {func.__name__} with args: {args} and kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {e}")
            raise
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(
                f"Exiting: {func.__name__} after {elapsed_time:.4f} seconds with result: {result if 'result' in locals() else 'Exception'}")

    return wrapper


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)


def log_warning(message):
    logger.warning(message)


def log_debug(message):
    logger.debug(message)
