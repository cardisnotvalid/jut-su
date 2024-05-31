import sys
import logging

FORMAT_LOG  = "%(levelname)s: %(message)s"
FORMAT_DATE = "%H:%M:%S"

formatter = logging.Formatter(fmt=FORMAT_LOG, datefmt=FORMAT_DATE)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

