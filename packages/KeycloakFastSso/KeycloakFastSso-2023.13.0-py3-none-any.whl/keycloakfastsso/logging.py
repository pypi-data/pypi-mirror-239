import logging

def setup_logging():
    """
    Configure and return the logger for keycloakfastsso.

    This function sets up both the console handler and the formatter for the logger. The logger logs the timestamp, name, levelname and message.
    
    The console handler's level is set to 'DEBUG' and the logger's level is also set to 'DEBUG' to capture all kinds of logs.
    
    Returns:
        logger : The configured logger for 'keycloakfastsso'.

    Examples:
    ```python
    logger = setup_logging()
    logger.info('This is an info message')

    # Console output: {timestamp} - keycloakfastsso - INFO - This is an info message
    ```

    """
    logger = logging.getLogger('keycloakfastsso')
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    return logger

logger = setup_logging()