"""
Unittests for class footballdata.FiveThirtyEight
"""

import pytest
# import footballdata as foo
import pandas as pd

from . testfixtures import *  # noqa


# Unittests -------------------------------------------------------------------
# Happy flow


def test_five38_league_ids(five38):
    assert isinstance(five38.league_ids, list)


def test_five38_leagues(five38):
    assert isinstance(five38.leagues(), pd.DataFrame)


def test_five38_games(five38):
    assert isinstance(five38.games(), pd.DataFrame)


def test_five38_forecasts(five38):
    assert isinstance(five38.forecasts(), pd.DataFrame)


def test_five38_clinches(five38):
    assert isinstance(five38.clinches(), pd.DataFrame)


def test_five38_laliga(five38_laliga):
    df = five38_laliga.leagues()
    assert len(df) == 1
    assert df.loc['la-liga', 'longName'] == 'La Liga'


def test_league_counts(five38):
    assert len(five38.league_ids) == len(five38.leagues())
    assert len(five38.league_ids) == len(five38.games()
                                         .reset_index()['league']
                                         .unique())
    assert len(five38.league_ids) == len(five38.forecasts()
                                         .reset_index()['league']
                                         .unique())


def test_league_matches_games(five38):
    assert all(
        five38.games().reset_index().league.unique() ==
        five38.leagues().reset_index().league.unique())


def test_league_matches_forecasts(five38):
    assert all(
        five38.forecasts().reset_index().league.unique() ==
        five38.leagues().reset_index().league.unique())

# Bad inits


def test_five38_league_value_error():
    with pytest.raises(ValueError):
        fbd.FiveThirtyEight('xxx')


def test_five38_league_type_error():
    with pytest.raises(TypeError):
        fbd.FiveThirtyEight(1)
