# -*- coding: utf-8 -*-

from __future__ import division
"""
Unittests for class footballdata.clubelo
"""

from datetime import datetime, timedelta
import pandas as pd
from .testfixtures import *  # noqa


# Unittests -------------------------------------------------------------------
# Happy flow

def test_by_date(elo):
    assert isinstance(elo.read_by_date(), pd.DataFrame)
    assert isinstance(elo.read_by_date('2017-04-01'), pd.DataFrame)
    assert isinstance(elo.read_by_date(datetime(2017, 4, 1)), pd.DataFrame)


def test_club_hist_age(elo):
    assert isinstance(elo.read_team_history('Feyenoord'),
                      pd.DataFrame)
    assert isinstance(elo.read_team_history('Feyenoord', 2),
                      pd.DataFrame)
    max_age = timedelta(seconds=1)
    assert isinstance(elo.read_team_history('Feyenoord', max_age),
                      pd.DataFrame)


def test_club_hist_replacement(elo):
    assert isinstance(elo.read_team_history('ADO Den Haag'),
                      pd.DataFrame)

# Bad calls

def test_by_date_bad_params(elo):
    with pytest.raises(ValueError):
        elo.read_by_date('2017')
    with pytest.raises(AttributeError):
        elo.read_by_date(1 / 4)


def test_club_hist_bad_params(elo):
    with pytest.raises(TypeError):
        elo.read_team_history()
    with pytest.raises(ValueError):
        elo.read_team_history('FC Knudde')
    with pytest.raises(TypeError):
        elo.read_team_history('Feyenoord', datetime.now())
