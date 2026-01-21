import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    log_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    # File handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes    = 1_000_000,
        backupCount = 5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ))

    # Attach handlers
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)

    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().handlers = app.logger.handlers

    template_logger = logging.getLogger("templateR")
    template_logger.setLevel(logging.INFO)
    template_logger.handlers = app.logger.handlers
    template_logger.propagate = False  # prevents duplicate logs if root also logs
