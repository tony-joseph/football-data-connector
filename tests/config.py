import datetime
import os


API_KEY = os.environ.get('TEST_API_KEY', '')

START_YEAR = datetime.datetime.now().year - 3

END_YEAR = datetime.datetime.now().year

DATA_LIMIT = 3
