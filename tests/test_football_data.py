import unittest

from footballdata import Connector
from footballdata.datasets import DataSet, Competition, Fixture, Team, Standing, Player

from . import config


class TestFootballData(unittest.TestCase):
    def setUp(self):
        self.connector = Connector(api_key=config.API_KEY)
        self.end_year = config.END_YEAR
        self.start_year = config.START_YEAR
        self.limit = config.DATA_LIMIT

    def verify_dataset(self, dataset, dataset_type):
        self.assertTrue(isinstance(dataset, DataSet))
        self.assertTrue((all(isinstance(c, dataset_type) for c in dataset)))

    def verify_competition(self, competition):
        self.verify_get_method(competition.get_teams, Team)
        self.verify_get_method(competition.get_fixtures, Fixture)
        self.verify_get_method(competition.get_league_table, Standing)
        teams = competition.get_teams(force_update=True)[:self.limit]
        self.verify_dataset(teams, Team)
        for team in teams:
            self.verify_team(team)

    def verify_team(self, team):
        self.verify_get_method(team.get_fixtures, Fixture)
        self.verify_get_method(team.get_players, Player)

    def verify_get_method(self, method, dataset_type):
        dataset = method(force_update=True)[:self.limit]
        self.verify_dataset(dataset, dataset_type)

    def test_get_competitions_current_season(self):
        competitions = self.connector.get_competitions(force_update=True)[:self.limit]
        self.verify_dataset(competitions, Competition)
        for competition in competitions:
            self.verify_competition(competition)

    def test_get_competitions_all_seasons(self):
        for season in range(self.start_year, self.end_year+1):
            competitions = self.connector.get_competitions(force_update=True, season=season)[:self.limit]
            self.verify_dataset(competitions, Competition)
            for competition in competitions:
                self.verify_competition(competition)

    def test_get_fixtures_current_season(self):
        fixtures = self.connector.get_fixtures(force_update=True)[:self.limit]
        self.verify_dataset(fixtures, Fixture)
