import pandas as pd
import pprint
import requests
import sys

if sys.version_info >= (3, 4):
    from pathlib import Path
else:
    from pathlib2 import Path

TEAMNAME_REPLACEMENTS = {
    'Alkmaar': 'AZ Alkmaar',
    'Den Haag': 'ADO Den Haag',
    'Groningen': 'FC Groningen',
    'Nijmegen': 'NEC Nijmegen',
    'PSV Eindhoven': 'PSV',
    'Roda': 'Roda JC',
    'Twente': 'FC Twente',
    'Utrecht': 'FC Utrecht',
    'Zwolle': 'PEC Zwolle',
}

LEAGUE_DICT = {
    'ENG-Premier League': {
        'MatchHistory': 'E0',  # Code used on football-data.co.uk
        'fbd_from_season': '9394',  # Availability on football-data.co.uk
        'FiveThirtyEight': 'premier-league',  # Slug used on fivethirtyeight.com
    },
    'ENG-Championship': {
        'MatchHistory': 'E1',
        'fbd_from_season': '9394'
    },  # Division 1 before 2004
    'ENG-League 1': {
        'MatchHistory': 'E2',
        'fbd_from_season': '9394'
    },  # Division 2 before 2004
    'ENG-League 2': {
        'MatchHistory': 'E3',
        'fbd_from_season': '9394'
    },  # Division 3 before 2004
    'ENG-Conference': {
        'MatchHistory': 'EC',
        'fbd_from_season': '0506'
    },  # Not available before 2005
    'SCO-Premier League': {
        'MatchHistory': 'E0',
        'fbd_from_season': '9495'
    },
    'SCO-Division 1': {
        'MatchHistory': 'E1',
        'fbd_from_season': '9495'
    },  # Division 1 before 2004
    'SCO-Division 2': {
        'MatchHistory': 'E2',
        'fbd_from_season': '9798'
    },  # Division 2 before 2004
    'SCO-Division 3': {
        'MatchHistory': 'E3',
        'fbd_from_season': '9798'
    },  # Division 3 before 2004
    'GER-Bundesliga': {
        'MatchHistory': 'D1',
        'fbd_from_season': '9394',
        'FiveThirtyEight': 'bundesliga',
    },
    'GER-Bundesliga 2': {
        'MatchHistory': 'D2',
        'fbd_from_season': '9394'
    },
    'ESP-La Liga': {
        'MatchHistory': 'SP1',
        'fbd_from_season': '9394',
        'FiveThirtyEight': 'la-liga',
    },
    'ESP-La Liga 2': {
        'MatchHistory': 'SP2',
        'fbd_from_season': '9697'
    },
    'ITA-Serie A': {
        'MatchHistory': 'I1',
        'fbd_from_season': '9394',
        'FiveThirtyEight': 'serie-a',
    },
    'ITA-Serie B': {
        'MatchHistory': 'I2',
        'fbd_from_season': '9798',
    },
    'FRA-Ligue 1': {
        'MatchHistory': 'F1',
        'fbd_from_season': '9394',
        'FiveThirtyEight': 'ligue-1',
    },
    'FRA-Ligue 2': {
        'MatchHistory': 'F2',
        'fbd_from_season': '9697',
    },
    'NED-Eredivisie': {
        'MatchHistory': 'N1',
        'fbd_from_season': '9394',
    },
    'BEL-Jupiler League': {
        'MatchHistory': 'B1',
        'fbd_from_season': '9596',
    },
    'POR-Liga 1': {
        'MatchHistory': 'P1',
        'fbd_from_season': '9495',
    },
    'TUR-Ligi 1': {
        'MatchHistory': 'T1',
        'fbd_from_season': '9495',
    },
    'GRE-Ethniki Katigoria': {
        'MatchHistory': 'G1',
        'fbd_from_season': '9495',
    },
    'Champions League': {
        'FiveThirtyEight': 'champions-league',
    },
    'USA-MLS': {
        'FiveThirtyEight': 'mls',
    },
    'USA-NWSL': {
        'FiveThirtyEight': 'nwsl',
    },
    'MEX-Liga MX': {
        'FiveThirtyEight': 'liga-mx',
    },
}


def datadir(directory='data'):
    """Return pathlib.Path to <cwd>/data
    Creates this directory if it doesn't exist
    """
    path = Path(directory)
    if not path.exists():
        path.mkdir()
    return path


class _BaseReader(object):
    """Base class for datareaders"""

    def __init__(self, leagues=None):
        self._selected_leagues = leagues

    @classmethod
    def _download_and_save(cls, url, filepath):
        """Downloads file at url to filepath
        Overwrites if filepath exists
        """
        r = requests.get(url)
        r.raise_for_status()
        with filepath.open(mode='wb') as f:
            f.write(r.content)

    @classmethod
    def available_leagues(cls):
        """Returns a list of league-ids available for this source"""
        return sorted(list(cls._all_leagues().keys()))

    @classmethod
    def _all_leagues(cls):
        """Returns a dict mapping all canonical league-ids to source league-ids"""
        if not hasattr(cls, '_all_leagues_dict'):
            cls._all_leagues_dict = {
                k: v[cls.__name__]
                for k, v in LEAGUE_DICT.items()
                if cls.__name__ in v
            }
        return cls._all_leagues_dict

    @classmethod
    def _translate_league(cls, df, col='league'):
        """Dataframe: source league id to canonical id"""
        df[col] = df[col].replace({v:k for k, v in cls._all_leagues().items()})
        return df

    @property
    def _selected_leagues(self):
        """A dict mapping selected canonical league-ids to source league-ids"""
        if not hasattr(self, '_leagues_dict'):
            self._leagues_dict = self._all_leagues()
        return self._leagues_dict

    @_selected_leagues.setter
    def _selected_leagues(self, ids=None):
        if ids is None:
            self._leagues_dict = self._all_leagues()
        else:
            if len(ids) == 0:
                raise ValueError("Empty iterable not allowed for 'leagues'")
            if isinstance(ids, str):
                ids = [ids]
            tmp_league_dict = {}
            for id in ids:
                if id not in self._all_leagues():
                    raise ValueError(
                        "Invalid league '{}'.\nValid leagues are:\n{}"
                            .format(id, pprint.pformat(self.available_leagues())))
                tmp_league_dict[id] = self._all_leagues()[id]
            self._leagues_dict = tmp_league_dict

