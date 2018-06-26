"""
    tests.test_football_data

    Tests data retrieval from API.

    :copyright: (c) 2018 Tony Joseph
    :license: BSD 3-Clause
"""

import unittest

from footballdata import Connector
from footballdata.datasets import DataSet, Competition, Fixture, Team, Standing, Player

from . import config


class TestFootballData(unittest.TestCase):
    """Tests data retrieval from API"""

    def setUp(self):
        self.connector = Connector(api_key=config.API_KEY)
        self.end_year = config.END_YEAR
        self.start_year = config.START_YEAR
        self.limit = config.DATA_LIMIT

    def verify_dataset(self, dataset, dataset_type):
        """Checks type and contents of data set object

        :param dataset: DataSet object
        :param dataset_type: class object
        :return: None
        """
        self.assertTrue(isinstance(dataset, DataSet))
        self.assertTrue((all(isinstance(c, dataset_type) for c in dataset)))

    def verify_competition(self, competition):
        """Checks properties of competition objects

        :param competition: Competition object
        :return: None
        """

        self.verify_get_method(competition.get_teams, Team)
        self.verify_get_method(competition.get_fixtures, Fixture)
        self.verify_get_method(competition.get_league_table, Standing)
        teams = competition.get_teams(force_update=True)[:self.limit]
        self.verify_dataset(teams, Team)
        for team in teams:
            self.verify_team(team)

    def verify_team(self, team):
        """Checks properties of team objects

        :param team: Team object
        :return: None
        """

        self.verify_get_method(team.get_fixtures, Fixture)
        self.verify_get_method(team.get_players, Player)

    def verify_get_method(self, method, dataset_type):
        """Checks data retrieval by get method

        :param method: Function - get method
        :param dataset_type: Class - expected type
        :return: None
        """
        dataset = method(force_update=True)[:self.limit]
        self.verify_dataset(dataset, dataset_type)

    def test_get_competitions_current_season(self):
        """Tests competition retrieval for current season"""

        competitions = self.connector.get_competitions(force_update=True)[:self.limit]
        self.verify_dataset(competitions, Competition)
        for competition in competitions:
            self.verify_competition(competition)

    def test_get_competitions_all_seasons(self):
        """Tests competition retrieval for all seasons"""

        for season in range(self.start_year, self.end_year+1):
            competitions = self.connector.get_competitions(force_update=True, season=season)[:self.limit]
            self.verify_dataset(competitions, Competition)
            for competition in competitions:
                self.verify_competition(competition)

    def test_get_fixtures_current_season(self):
        """Tests fixture retrieval for current season"""

        fixtures = self.connector.get_fixtures(force_update=True)[:self.limit]
        self.verify_dataset(fixtures, Fixture)
