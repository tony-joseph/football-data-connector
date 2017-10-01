from dateutil.parser import parse as datetime_parse

from .utils import fetch_data_from_api, clean_object


class FootballDataObject:
    """Parent class for all football data components"""

    def __init__(self, **kwargs):
        """Initialises new object with attributes from keyword arguments"""

        for key in kwargs.keys():
            if key == 'last_updated' and kwargs[key]:
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
        self.__teams = []
        self.__fixtures = []
        self.__league_table = []

    def get_teams(self, force_update=False):
        """Fetches all teams in a competition
        
        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Team objects
        """

        if force_update or not self.__teams:
            self.__teams = DataSet(klass=Team, endpoint=self.teams_endpoint, api_key=self.api_key)

        return self.__teams

    def get_fixtures(self, force_update=False):
        """Fetches all fixtures in a competition

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Fixture objects
        """

        if force_update or not self.__fixtures:
            self.__fixtures = DataSet(klass=Fixture, endpoint=self.fixtures_endpoint, api_key=self.api_key)

        return self.__fixtures

    def get_league_table(self, force_update=False):
        """Fetches standing of all teams in competition

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Standing objects
        """

        if force_update or not self.__league_table:
            self.__league_table = DataSet(klass=Standing, endpoint=self.league_table_endpoint, api_key=self.api_key)

        return self.__league_table


class Fixture(FootballDataObject):
    """Class to represent a fixture"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Convert date to datetime object
        if hasattr(self, 'date'):
            self.date = datetime_parse(self.date)


class Team(FootballDataObject):
    """Class to represent a team"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set extra attributes
        self.fixtures_endpoint = self.links['fixtures']['href']
        self.players_endpoint = self.links['players']['href']
        self.base_endpoint = self.links['self']['href']
        self.__fixtures = []
        self.__players = []

    def get_fixtures(self, force_update=False):
        """Fetches all fixtures for a team

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Fixture objects
        """

        if force_update or not self.__fixtures:
            self.__fixtures = DataSet(klass=Fixture, endpoint=self.fixtures_endpoint, api_key=self.api_key)

        return self.__fixtures

    def get_players(self, force_update=False):
        """Fetches all players in a team

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Player objects
        """

        if force_update or not self.__players:
            self.__players = DataSet(klass=Player, endpoint=self.players_endpoint, api_key=self.api_key)

        return self.__players


class Standing(FootballDataObject):
    """Class to represent a team's standing in a competition"""

    pass


class Player(FootballDataObject):
    """Class to represent a player"""

    def __init__(self, **kwargs):
        """Initialises Player object"""
        super().__init__(**kwargs)

        # Convert contract_until and date_of_birth to datetime objects
        if hasattr(self, 'contract_until') and self.contract_until:
            self.contract_until = datetime_parse(self.contract_until)
        if hasattr(self, 'date_of_birth') and self.date_of_birth:
            self.date_of_birth = datetime_parse(self.date_of_birth)


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

        self.__klass = klass
        self.__endpoint = endpoint
        self.__api_key = api_key
        self.__options = options if options else {}

        # Set data_list as data_set if available
        if data_list:
            # Type check all elements in iterable
            if not all(isinstance(item, klass) for item in data_list):
                raise TypeError("All items should be an instance of {}".format(klass))
            self.__data_set = list(data_list)
        else:
            self.__data_set = []

    def __create_data_set_item(self, cleaned_data):
        """Creates a single football data object
        
        :param cleaned_data: Dict with proper key value pairs
        :return: FootballDataObject object
        """

        data_set_item = self.__klass(**cleaned_data)

        # Build base endpoint if id is available
        if hasattr(data_set_item, 'id'):
            data_set_item.base_endpoint = "{}{}".format(self.__endpoint, data_set_item.id)
        else:
            data_set_item.base_endpoint = self.__endpoint

        data_set_item.api_key = self.__api_key
        return data_set_item

    def __load_data_set(self):
        """Loads data from football-data.org in not already loaded"""

        if not self.__data_set and self.__endpoint:
            data_list = fetch_data_from_api(endpoint=self.__endpoint, api_key=self.__api_key, options=self.__options)

            if data_list:
                # Handles inconsistent API structures
                if self.__klass == Team:
                    # Actual team list is in dict with key teams
                    data_list = data_list['teams']
                elif self.__klass == Fixture:
                    # Actual fixture list is in dict with key fixtures
                    data_list = data_list['fixtures']
                elif self.__klass == Standing:
                    # Handle differences in league and cup standing
                    if 'standing' in data_list:
                        # Competition is a league
                        data_list = data_list['standing']
                    else:
                        # No league table available
                        return
                elif self.__klass == Player:
                    data_list = data_list['players']

                cleaned_data_list = map(clean_object, data_list)
                self.__data_set = list(map(self.__create_data_set_item, cleaned_data_list))
            else:
                # Data list fetching failed due to some reason
                self.__data_set = []

    def __iter__(self):
        self.__load_data_set()
        for data in self.__data_set:
            yield data

    def __getitem__(self, key):
        self.__load_data_set()

        if isinstance(key, int):
            # If key is an integer, return item at index
            try:
                return self.__data_set[key]
            except IndexError:
                raise IndexError('Index out of range')
        elif isinstance(key, slice):
            return DataSet(klass=self.__klass, data_list=self.__data_set[key])

        raise TypeError('Key must be an integer or slice object')

    def __len__(self):
        self.__load_data_set()
        return len(self.__data_set)

    def __bool__(self):
        self.__load_data_set()
        return bool(self.__data_set)
