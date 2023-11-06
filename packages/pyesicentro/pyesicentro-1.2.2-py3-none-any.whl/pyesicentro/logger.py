import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
c_format = logging.Formatter(
    '%(name)s - %(levelname)-8s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S'
    )
c_handler.setFormatter(c_format)

# Add handlers to the logger
logger.addHandler(c_handler)
