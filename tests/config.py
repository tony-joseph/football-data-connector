"""
    tests.config
    ~~~~~~~~~~~~

    Includes configuration to control test run.

    :copyright: (c) 2018 Tony Joseph
    :license: BSD 3-Clause
"""

import datetime
import os


API_KEY = os.environ.get('TEST_API_KEY', '')

START_YEAR = datetime.datetime.now().year - 3

END_YEAR = datetime.datetime.now().year

DATA_LIMIT = 3
