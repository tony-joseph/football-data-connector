**********
User Guide
**********

Creating a Connection to football-data.org API
==============================================

Before retrieving data, you need to create a connection object.

.. code-block:: python

    from footballdata.connector import Connector

    connection = Connector()


The **Connector** constructor also accepts two optional arguments, *api_key*
and *api_version*.

.. code-block:: python

    from footballdata import Connector

    connection = Connector(api_key='api key from football-data.org', api_version='v1')

Using an API key is recommended. Otherwise you may hit the rate limiting of
API. Currently the only supported API version is v1. You can retrieve the list
of supported API versions using the class method
`Connector.supported_api_versions()supported_api_versions`

Connector object attributes
---------------------------

- **api_key**
    Gives the API key used to create Connector object
- **api_version**
    Gives the API version used to create Connector object
- **base_url**
    Gives the base API URL
- **competitions_endpoint**
    Gives the API endpoint to fetch competitions
- **fixtures_endpoint**
    Gives the API endpoint to fetch fixtures

Connector object methods
------------------------

get_competitions(season='', force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Returns a DataSet object contains Competition objects. Accepts two
optional arguments, *season* and *force_update*. *season* should be a 4
digit integer representing an year (example 2017). If season is given,
only the competitions in the given season will be fetched. Once the values
are fetched from API, the results will be cached and, the subsequent calls
to get_competitions method will return the cached results. Use
*force_update=True* if you want to override the cache and get fresh
results from API.

get_fixtures(force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a **DataSet** object contains **Fixture** objects. Results will be
cached after first API call to avoid unnecessary API hits. Use 
*force_update=True* if you want to override the cache.


DataSet Objects
===============

Methods like *get_competitions*, *get_fixtures* etc will return a **DataSet**
object. **DataSet** is an iterable object. You can use it like any other
iterable such as list, tuple etc. Operations like using with a for loop, 
checking length using len, subscripting, slicing, reversing etc are supported.

Competition Objects
===================

A **Competition** object represents a competition in football-data.org API.

Competition Object Attributes
-----------------------------

- id
- caption
- current_match_day
- last_updated
- league
- number_of_games
- number_of_teams
- year

Competition Object Methods
--------------------------

get_teams(force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a **DataSet** of **Team** objects. Use *force_update=True* to override
cache.

get_fixtures(force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a **DataSet** of **Fixture** objects. Use force_update=True to
override cache.

get_league_table(force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a **DataSet** of **Standing** objects. If league table is not
available for a competition, an empty **DataSet** will be returned. Use
*force_update=True* to override cache.

Fixture Objects
===============

A **Fixture** object represent a fixture in football-data.org API.

Fixture Object Attributes
-------------------------

- date
- away_team_name
- home_team_name
- match_day
- odds
- result
- status

Team Objects
============

A **Team** object represents a team in a competition.

Team Object Attributes
----------------------

- code
- crest_url
- name
- short_name
- squad_market_value

Team Object Methods
-------------------

get_fixtures(force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a **DataSet** of **Fixture** objects representing fixtures of the team
for the current season.

get_players(force_update=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a **DataSet** for Player objects representing players in the team.

Standing Objects
================

A **Standing** object represents the standing of a team in a competition.

Standing Object Attributes
--------------------------

- team_name
- crest_uri
- played_games
- wins
- draws
- losses
- home
- away
- points
- position
- goals
- goals_aganist
- goal_difference

Player Objects
==============

A **Player** object represents a player in a team.

Player Object Attributes
------------------------

- name
- nationality
- position
- contract_until
- date_of_birth
- jersey_number
- market_value
