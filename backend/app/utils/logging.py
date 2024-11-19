import logging


def setup_logging(level=logging.INFO):
    """
    Sets up the logging configuration for the application.

    Args:
    - level: The logging level (default is INFO).
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info("Initiating logger")
