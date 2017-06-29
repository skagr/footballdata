"""
Pytest fixtures for footballdata package
"""

import footballdata as foo
import pytest


@pytest.fixture
def five38():
    """returns a correctly initialized instance of FiveThirtyEight"""
    return foo.FiveThirtyEight()


@pytest.fixture
def five38_laliga():
    """returns a correctly initialized instance of FiveThirtyEight
    filtered by league: La Liga"""
    return foo.FiveThirtyEight('ESP-La Liga')


@pytest.fixture
def elo():
    """returns a correctly initialized instance of ClubElo"""
    return foo.ClubElo()

@pytest.fixture
def match_eredivisie_10y():
    """returns a MatchHistory instance for the last
    10 years of the Eredivisie"""
    seasons = [x for x in range(2007, 2017)]
    # seasons = 2007
    return foo.MatchHistory('NED-Eredivisie', seasons)

@pytest.fixture
def match_f538():
    """returns a MatchHistory object initialized with
    the intersection of MatchHistory.allowed_leagues
    and FiveThirtyEight.allowed_leagues
    for season 2016-17
    """
    leagues = [
        'GER-Bundesliga',
        'ENG-Premier League',
        'ESP-La Liga',
        'FRA-Ligue 1',
        'ITA-Serie A',
    ]
    return foo.MatchHistory(leagues, '2016-17')
