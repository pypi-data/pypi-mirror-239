import time
import logging

logger = logging.getLogger()

def stopwatch(func):
    def wrapper():
        start = time.time()
        func()
        logger.info(f"{func.__name__} took {time.time()-start} ms.")
    return wrapper