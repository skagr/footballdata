# -*- coding: utf-8 -*-

import numpy as np
import pprint
import requests
import sys

if sys.version_info >= (3, 4):
    from pathlib import Path
else:
    from pathlib2 import Path

TEAMNAME_REPLACEMENTS = {
    'Akhisar': 'Akhisar Belediyespor',
    'Alaves': 'Alavés',
    'Alkmaar': 'AZ Alkmaar',
    'Ath Bilbao': 'Athletic Bilbao',
    'Ath Madrid': 'Atletico Madrid',
    'Atletico': 'Atletico Madrid',
    'Aue': 'Erzgebirge Aue',
    'Augsburg': 'FC Augsburg',
    'Bayern': 'Bayern München',
    'Bayern Munich': 'Bayern München',
    'Betis': 'Real Betis',
    'Beveren': 'Waasland-Beveren',
    'Bilbao': 'Athletic Bilbao',
    'Borussia Monchengladbach': 'Borussia Mönchengladbach',
    'Bourg-Peronnas': 'Bourg Peronnas',
    'Bournemouth': 'AFC Bournemouth',
    'Braga': 'Sp Braga',
    'Brugge': 'Club Brugge',
    'Bueyueksehir': 'Büyüksehir',
    'Buyuksehyr': 'Büyüksehir',
    'Celta': 'Celta de Vigo',
    'Celta Vigo': 'Celta de Vigo',
    'Chievo': 'Chievo Verona',
    'Darmstadt': 'SV Darmstadt 98',
    'Den Haag': 'ADO Den Haag',
    'Depor': 'Deportivo La Coruña',
    'Dijon': 'Dijon FCO',
    'Dortmund': 'Borussia Dortmund',
    'Duesseldorf': 'Fortuna Düsseldorf',
    'Ein Frankfurt': 'Eintracht Frankfurt',
    'Entella': 'Virtus Entella',
    'Espanol': 'Espanyol',
    'FC Cologne': 'FC Köln',
    'FC Koln': 'FC Augsburg',
    'Forest': 'Nottingham Forest',
    'Fortuna Dusseldorf': 'Fortuna Düsseldorf',
    'Frankfurt': 'Eintracht Frankfurt',
    'Freiburg': 'SC Freiburg',
    'Fuerth': 'Greuther Furth',
    'Gijon': 'Sporting Gijón',
    'Gladbach': 'Borussia Mönchengladbach',
    'Groningen': 'FC Groningen',
    'Hamburg': 'Hamburg SV',
    'Hertha': 'Hertha Berlin',
    'Hoffenheim': 'TSG Hoffenheim',
    'Hull': 'Hull City',
    'Ingolstadt': 'FC Ingolstadt 04',
    'Inter': 'Internazionale',
    'Karabuekspor': 'Karabükspor',
    'Karabukspor': 'Karabükspor',
    'Kayseri': 'Kayserispor',
    'Koeln': 'FC Köln',
    'La Coruna': 'Deportivo La Coruña',
    'Lautern': 'Kaiserslautern',
    'Leicester': 'Leicester City',
    'Leverkusen': 'Bayer Leverkusen',
    "M'gladbach": 'Borussia Mönchengladbach',
    'Malaga': 'Málaga',
    'Man City': 'Leicester City',
    'Man United': 'Manchester United',
    'Milan': 'AC Milan',
    'Monaco': 'AS Monaco',
    'Muenchen 60': 'München 1860',
    'Munich 1860': 'München 1860',
    'Nancy': 'AS Nancy Lorraine',
    'Nijmegen': 'NEC Nijmegen',
    "Nott'm Forest": 'Nottingham Forest',
    'Nuernberg': 'Nürnberg',
    'Nurnberg': 'Nürnberg',
    'PSV Eindhoven': 'PSV',
    'Paris SG': 'Paris Saint-Germain',
    'Pescara': 'US Pescara',
    'Rennes': 'Stade Rennes',
    'Roda': 'Roda JC',
    'Roma': 'AS Roma',
    'Saint-Etienne': 'St Etienne',
    'Schalke': 'Schalke 04',
    'Sevilla': 'Sevilla FC',
    'Sociedad': 'Real Sociedad',
    'Sp Gijon': 'Sporting Gijón',
    'Stoke': 'Stoke City',
    'Swansea': 'Swansea City',
    'Tottenham': 'Tottenham Hotspur',
    'Twente': 'FC Twente',
    'Utrecht': 'FC Utrecht',
    'Vallecano': 'Rayo Vallecano',
    'Waregem': 'Zulte Waregem',
    'Werder': 'Werder Bremen',
    'West Brom': 'West Bromwich Albion',
    'West Ham': 'West Ham United',
    'Wolfsburg': 'VfL Wolfsburg',
    'Wuerzburg': 'Würzburger Kickers',
    'Wurzburger Kickers': 'Würzburger Kickers',
    'Zwolle': 'PEC Zwolle'}

# TEAMNAME_REPLACEMENTS = {'Den Haag': 'ADO Den Haag'}

LEAGUE_DICT = {
    'ENG-Premier League': {
        'ClubElo': 'ENG_1',  # Used to id on clubelo.co)m
        'MatchHistory': 'E0',  # Code used on football-data.co.uk
        'MH_from_season': '9394',  # Availability on football-data.co.uk
        'FiveThirtyEight': 'premier-league',  # Slug used on fivethirtyeight.com
    },
    'ENG-Championship': {
        'ClubElo': 'ENG_2',
        'MatchHistory': 'E1',
        'MH_from_season': '9394'
    },  # Division 1 before 2004
    'ENG-League 1': {
        'MatchHistory': 'E2',
        'MH_from_season': '9394'
    },  # Division 2 before 2004
    'ENG-League 2': {
        'MatchHistory': 'E3',
        'MH_from_season': '9394'
    },  # Division 3 before 2004
    'ENG-Conference': {
        'MatchHistory': 'EC',
        'MH_from_season': '0506'
    },  # Not available before 2005
    'SCO-Premier League': {
        'ClubElo': 'SCO_1',
        'MatchHistory': 'SC0',
        'MH_from_season': '9495'
    },
    'SCO-Division 1': {
        'MatchHistory': 'SC1',
        'MH_from_season': '9495'
    },  # Division 1 before 2004
    'SCO-Division 2': {
        'MatchHistory': 'SC2',
        'MH_from_season': '9798'
    },  # Division 2 before 2004
    'SCO-Division 3': {
        'MatchHistory': 'SC3',
        'MH_from_season': '9798'
    },  # Division 3 before 2004
    'GER-Bundesliga': {
        'ClubElo': 'GER_1',
        'MatchHistory': 'D1',
        'MH_from_season': '9394',
        'FiveThirtyEight': 'bundesliga',
    },
    'GER-Bundesliga 2': {
        'ClubElo': 'GER_2',
        'MatchHistory': 'D2',
        'MH_from_season': '9394'
    },
    'ESP-La Liga': {
        'ClubElo': 'ESP_1',
        'MatchHistory': 'SP1',
        'MH_from_season': '9394',
        'FiveThirtyEight': 'la-liga',
    },
    'ESP-La Liga 2': {
        'ClubElo': 'ESP_2',
        'MatchHistory': 'SP2',
        'MH_from_season': '9697'
    },
    'ITA-Serie A': {
        'ClubElo': 'ITA_1',
        'MatchHistory': 'I1',
        'MH_from_season': '9394',
        'FiveThirtyEight': 'serie-a',
    },
    'ITA-Serie B': {
        'ClubElo': 'ITA_2',
        'MatchHistory': 'I2',
        'MH_from_season': '9798',
    },
    'FRA-Ligue 1': {
        'ClubElo': 'FRA_1',
        'MatchHistory': 'F1',
        'MH_from_season': '9394',
        'FiveThirtyEight': 'ligue-1',
    },
    'FRA-Ligue 2': {
        'ClubElo': 'FRA_2',
        'MatchHistory': 'F2',
        'MH_from_season': '9697',
    },
    'NED-Eredivisie': {
        'ClubElo': 'NED_1',
        'MatchHistory': 'N1',
        'MH_from_season': '9394',
    },
    'BEL-Jupiler League': {
        'ClubElo': 'BEL_1',
        'MatchHistory': 'B1',
        'MH_from_season': '9596',
    },
    'POR-Liga 1': {
        'ClubElo': 'POR_1',
        'MatchHistory': 'P1',
        'MH_from_season': '9495',
    },
    'TUR-Ligi 1': {
        'ClubElo': 'TUR_1',
        'MatchHistory': 'T1',
        'MH_from_season': '9495',
    },
    'GRE-Ethniki Katigoria': {
        'ClubElo': 'GRE_1',
        'MatchHistory': 'G1',
        'MH_from_season': '9495',
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
    'Champions League': {
        'FiveThirtyEight': 'champions-league',
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
        flip = {v: k for k, v in cls._all_leagues().items()}
        mask = ~df[col].isin(flip)
        df.loc[mask, col] = np.nan
        df[col] = df[col].replace(flip)
        # df[col] = df[col].replace({v:k for k, v in cls._all_leagues().items()})
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
            for i in ids:
                if i not in self._all_leagues():
                    raise ValueError(
                        "Invalid league '{}'.\nValid leagues are:\n{}"
                            .format(i, pprint.pformat(self.available_leagues())))
                tmp_league_dict[i] = self._all_leagues()[i]
            self._leagues_dict = tmp_league_dict
