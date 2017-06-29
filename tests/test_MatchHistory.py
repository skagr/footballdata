"""
Unittests for class footballdata.MatchHistory
"""

import pandas as pd
import footballdata as foo
from .testfixtures import *  # noqa


# Unittests -------------------------------------------------------------------
# Reader
def test_eredivisie_10y(match_eredivisie_10y):
    df = match_eredivisie_10y.read_games()
    assert isinstance(df, pd.DataFrame)

def test_like_f538(match_f538):
    """2016 season, league intersection with FiveThirtyEight"""
    df = match_f538.read_games()
    assert isinstance(df, pd.DataFrame)


# Season codes
def test_season_pattern1a():
    assert foo.MatchHistory._season_code('9495') == '9495'


def test_season_pattern1a_warn():
    with pytest.warns(UserWarning) as record:
        assert foo.MatchHistory._season_code('2021') == '2021'

    # check that only one warning was raised
    assert len(record) == 1
    # check that the message matches
    assert record[0].message.args[0] == 'Season id "2021" is ambiguous: interpreting as "20-21"'


def test_season_pattern1b():
    my_season = check_post = '1998'
    assert foo.MatchHistory._season_code(my_season) == '9899'
    assert my_season == check_post


def test_season_pattern1c():
    assert foo.MatchHistory._season_code('1999') == '9900'


def test_season_pattern2():
    assert foo.MatchHistory._season_code('11') == '1112'
    assert foo.MatchHistory._season_code('99') == '9900'


def test_season_pattern3():
    assert foo.MatchHistory._season_code('2011-2012') == '1112'
    assert foo.MatchHistory._season_code('1999-2000') == '9900'


def test_season_pattern4():
    assert foo.MatchHistory._season_code('2011-12') == '1112'
    assert foo.MatchHistory._season_code('1999-00') == '9900'


def test_season_pattern5():
    assert foo.MatchHistory._season_code('13-14') == '1314'
