"""


:author Johan Lanzrein:
:file __init__.py:
"""

import logging

from .logger import ColoredLogger, set_default_logger


# Set up the colored logger
class Logger:

    def __init__(self,
                 filename='logs.log',
                 level=logging.WARNING,
                 name='Palo Alto Utils'):
        logging.setLoggerClass(ColoredLogger)
        logging.basicConfig(filename=filename, level=level)
        self.log = logging.getLogger(name)
