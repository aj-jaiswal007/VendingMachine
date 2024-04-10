import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
