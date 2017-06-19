"""
Unittests for class footballdata.ClubElo
"""

# import pytest
# from footballdata import ClubElo
from datetime import datetime, timedelta
import pandas as pd

from . fixtures import *  # noqa


# Unittests -------------------------------------------------------------------
# Happy flow

def test_by_date(clubElo):
    assert isinstance(clubElo.by_date(), pd.DataFrame)
    assert isinstance(clubElo.by_date('2017-04-01'), pd.DataFrame)
    assert isinstance(clubElo.by_date(datetime(2017, 4, 1)), pd.DataFrame)


def test_club_hist(clubElo):
    assert isinstance(clubElo.club_history('Feyenoord'),
                      pd.DataFrame)
    assert isinstance(clubElo.club_history('Feyenoord', 2),
                      pd.DataFrame)
    max_age = timedelta(seconds=1)
    assert isinstance(clubElo.club_history('Feyenoord', max_age),
                      pd.DataFrame)


# Bad calls

def test_by_date_bad_params(clubElo):
    with pytest.raises(ValueError):
        clubElo.by_date('2017')
    with pytest.raises(AttributeError):
        clubElo.by_date(1 / 4)


def test_club_hist_bad_params(clubElo):
    with pytest.raises(TypeError):
        clubElo.club_history()
    with pytest.raises(ValueError):
        clubElo.club_history('FC Knudde')
    with pytest.raises(TypeError):
        clubElo.club_history('Feyenoord', datetime.now())
