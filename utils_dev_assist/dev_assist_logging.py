#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
dev_assist_logging.py--set up the logging for dev_assist.py.
'''

import logging
from logging import handlers


def app_log(name: str) -> logging.Logger:
    ''' Set-up the logging object. '''

    logger = logging.getLogger(name)

    # Set log level to debug - higher than info.
    logger.setLevel(logging.DEBUG)

    # Create a formatter object with specified format for the logs.
    formatter = logging.Formatter(
                              '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                              "%Y-%m-%d %H:%M:%S")

    # Create file handler to handle log files rotation and backup.
    file_handler = handlers.RotatingFileHandler('.dev_assist.log',
                                                maxBytes=60000, backupCount=2)
    # Set formatter for the file handler object.
    file_handler.setFormatter(formatter)

    # Add file handler to logger instance.
    logger.addHandler(file_handler)

#    # Create stream handler to handle logs in console.
#    stream_handler = logging.StreamHandler()
#
#    # Set formatter for the stream handler object.
#    stream_handler.setFormatter(formatter)
#
#    # Add stream handler to logger instance.
#    logger.addHandler(stream_handler)

    return logger


# Calling the function and logging a message.
if __name__ == "__main__":
    log = app_log(__name__)
    log.info("[TEST] logging is set up.")
