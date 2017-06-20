"""
Pytest fixtures for footballdata package
"""

import footballdata as fbd
import pytest


@pytest.fixture
def five38():
    """returns a correctly initialized instance of FiveThirtyEight"""
    return fbd.FiveThirtyEight()


@pytest.fixture
def five38_laliga():
    """returns a correctly initialized instance of FiveThirtyEight
    filtered by league: La Liga"""
    return fbd.FiveThirtyEight('la-liga')


@pytest.fixture
def clubElo():
    """returns a correctly initialized instance of ClubElo"""
    return fbd.ClubElo()
