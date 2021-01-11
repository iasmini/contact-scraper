# -*- encoding: utf-8 -*-
import configparser
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)


def get_parser():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(current_dir, 'config.ini')
    parser = configparser.ConfigParser()
    try:
        parser.read(config_path)
    except FileNotFoundError:
        logger.fatal('{} file was not found'.format(config_path))
        sys.exit(1)
    return parser
