from .datasets import DataSet, Competition, Fixture


class Connector:
    """Class to initialise connection to football-data.org"""

    __supported_api_versions = ['v1']

    def __init__(self, api_key='', api_version='v1'):
        """Initialises connection to football-data.org
        
        :param api_key: API key from football-data.org, optional
        :param api_version: API version, defaults to v1
        :return: Connector object
        """

        # Check if API version is supported
        if api_version not in self.__supported_api_versions:
            raise NotImplementedError('This API version is not supported')

        self.api_key = api_key
        self.api_version = api_version

        # Build base url with API version
        self.base_url = "http://api.football-data.org/{api_version}/".format(api_version=api_version)

        # Build other endpoint urls
        self.competition_endpoint = "{base_url}competitions/".format(base_url=self.base_url)
        self.fixtures_endpoint = "{base_url}fixtures/".format(base_url=self.base_url)

        # Initialise competitions and fixtures
        self.__competitions = []
        self.__fixtures = []

    @classmethod
    def supported_api_versions(cls):
        """Returns the supported api versions as list"""
        return cls.__supported_api_versions

    def get_competitions(self, season='', force_update=False):
        """Fetches all competitions
        
        :param force_update: Boolean, overrides cached results if True
        :param season: 4 digit integer representing a season, optional
        :return: DataSet of Competition objects
        """

        if force_update or not self.__competitions:
            options = {'season': season} if season else None
            self.__competitions = DataSet(klass=Competition, endpoint=self.competition_endpoint, api_key=self.api_key,
                                          options=options)

        return self.__competitions

    def get_fixtures(self, force_update=False):
        """Fetches all fixtures

        :param force_update: Boolean, overrides cached results if True
        :return: DataSet of Fixture objects
        """

        if force_update or not self.__fixtures:
            self.__fixtures = DataSet(klass=Fixture, endpoint=self.fixtures_endpoint, api_key=self.api_key)

        return self.__fixtures
