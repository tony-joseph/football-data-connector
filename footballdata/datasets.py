from dateutil.parser import parse as datetime_parse

from .utils import fetch_data_from_api, clean_object


class FootballDataObject:
    """Parent class for all football data components"""

    def __init__(self, **kwargs):
        """Initialises new object with attributes from keyword arguments"""

        for key in kwargs.keys():
            if key == 'last_updated':
                kwargs[key] = datetime_parse(kwargs[key])
            setattr(self, key, kwargs[key])

        # Base API endpoint and API key of current object
        # Set by subclasses or object creator
        self.base_endpoint = ''
        self.api_key = ''


class Competition(FootballDataObject):
    """Class to represent a competition"""

    def __init__(self, **kwargs):
        """Initialises new competition object"""

        super().__init__(**kwargs)

        # Set competition attributes
        self.fixtures_endpoint = self.links['fixtures']['href']
        self.league_table_endpoint = self.links['leagueTable']['href']
        self.teams_endpoint = self.links['teams']['href']
        self.base_endpoint = self.links['self']['href']
        self._teams = []
        self._fixtures = []
        self._league_table = []

    def get_teams(self, force_update=False):
        """Fetches all teams in a competition
        
        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Team objects
        """

        if force_update or not self._teams:
            self._teams = DataSet(klass=Team, endpoint=self.teams_endpoint, api_key=self.api_key)

        return self._teams

    def get_fixtures(self, force_update=False):
        """Fetches all fixtures in a competition

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Fixture objects
        """

        if force_update or not self._fixtures:
            self._fixtures = DataSet(klass=Fixture, endpoint=self.fixtures_endpoint, api_key=self.api_key)

        return self._fixtures


class Fixture(FootballDataObject):
    """Class to represent a fixture"""

    pass


class Team(FootballDataObject):
    """Class to represent a team"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set extra attributes
        self.fixtures_endpoint = self.links['fixtures']['href']
        self.players_endpoint = self.links['players']['href']
        self.base_endpoint = self.links['self']['href']
        self._fixtures = []
        self._players = []

    def get_fixtures(self, force_update=False):
        """Fetches all fixtures for a team

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Fixture objects
        """

        if force_update or not self._fixtures:
            self._fixtures = DataSet(klass=Fixture, endpoint=self.fixtures_endpoint, api_key=self.api_key)

        return self._fixtures


class DataSet:
    """Class to represent a sequence of football data objects"""

    def __init__(self, klass, endpoint='', api_key='', options=None, data_list=None):
        """Initialises FootballDataObject sequence

        :param klass: type, Class of objects in data set. Should be either FootballDataObject or its subclass
        :param endpoint: str, API endpoint to fetch data
        :param api_key: str, API key
        :param options: dict, Additional arguments to sent with API call
        :param data_list: iterable containing klass objects
        """

        self._klass = klass
        self._endpoint = endpoint
        self._api_key = api_key
        self._options = options if options else {}

        # Set data_list as data_set if available
        if data_list:
            # Type check all elements in iterable
            if not all(isinstance(item, klass) for item in data_list):
                raise TypeError("All items should be an instance of {}".format(klass))
            self._data_set = list(data_list)
        else:
            self._data_set = []

    def _create_data_set_item(self, cleaned_data):
        """Creates a single football data object
        
        :param cleaned_data: Dict with proper key value pairs
        :return: FootballDataObject object
        """

        data_set_item = self._klass(**cleaned_data)

        # Build base endpoint if id is available
        if hasattr(data_set_item, 'id'):
            data_set_item.base_endpoint = "{}{}".format(self._endpoint, data_set_item.id)
        else:
            data_set_item.base_endpoint = self._endpoint

        data_set_item.api_key = self._api_key
        return data_set_item

    def _load_data_set(self):
        """Loads data from football-data.org in not already loaded"""

        if not self._data_set and self._endpoint:
            data_list = fetch_data_from_api(endpoint=self._endpoint, api_key=self._api_key, options=self._options)

            # Handles inconsistent API structures
            if self._klass == Team:
                # Actual team list is in dict with key teams
                data_list = data_list['teams']
            elif self._klass == Fixture:
                data_list = data_list['fixtures']

            cleaned_data_list = map(clean_object, data_list)
            self._data_set = list(map(self._create_data_set_item, cleaned_data_list))

    def __iter__(self):
        self._load_data_set()
        for data in self._data_set:
            yield data

    def __getitem__(self, key):
        self._load_data_set()

        if isinstance(key, int):
            # If key is an integer, return item at index
            try:
                return self._data_set[key]
            except IndexError:
                raise IndexError('Index out of range')
        elif isinstance(key, slice):
            return DataSet(klass=self._klass, data_list=self._data_set[key])

        raise TypeError('Key must be an integer or slice object')

    def __len__(self):
        self._load_data_set()
        return len(self._data_set)

    def __bool__(self):
        self._load_data_set()
        return bool(self._data_set)
