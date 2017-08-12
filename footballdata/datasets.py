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

    def _build_endpoints(self):
        """Builds API endpoints
        
        Creates API endpoints which are dependant on other attributes hence 
        can not be created in init
        """

        pass


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

        # Build endpoints
        self._build_endpoints()

        if force_update or not self._teams:
            self._teams = DataSet(klass=Team, endpoint=self.teams_endpoint, api_key=self.api_key)

        return self._teams

    def get_fixtures(self, force_update=False):
        """Fetches all fixtures in a competition

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Fixture objects
        """

        # Build endpoints
        self._build_endpoints()

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

        # Build endpoints
        self._build_endpoints()

        if force_update or not self._fixtures:
            self._fixtures = DataSet(klass=Fixture, endpoint=self.fixtures_endpoint, api_key=self.api_key)

        return self._fixtures


class DataSet:
    """Class to represent a sequence of football data objects"""

    def __init__(self, klass, endpoint, api_key=''):
        self._klass = klass
        self._endpoint = endpoint
        self._api_key = api_key
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

        if not self._data_set:
            data_list = fetch_data_from_api(endpoint=self._endpoint, api_key=self._api_key)

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

        # If key is an integer
        if isinstance(key, int):
            try:
                return self._data_set[key]
            except IndexError:
                raise IndexError('Index out of range')

        raise TypeError('Key must be an integer')

    def __len__(self):
        self._load_data_set()
        return len(self._data_set)

    def __bool__(self):
        self._load_data_set()
        return bool(self._data_set)
