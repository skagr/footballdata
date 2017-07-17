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
    'Akhisar': u'Akhisar Belediyespor',
    'Ajaccio': u'Ajaccio GFCO',
    'Alaves': u'Alavés',
    'Alkmaar': u'AZ Alkmaar',
    'Arles': u'Arles-Avignon',
    'Ath Bilbao': u'Athletic Bilbao',
    'Ath Madrid': u'Atletico Madrid',
    'Atletico': u'Atletico Madrid',
    'Aue': u'Erzgebirge Aue',
    'Augsburg': u'FC Augsburg',
    'Bayern': u'Bayern München',
    'Bayern Munich': u'Bayern München',
    'Betis': u'Real Betis',
    'Beveren': u'Waasland-Beveren',
    'Bilbao': u'Athletic Bilbao',
    'Borussia Monchengladbach': u'Borussia Mönchengladbach',
    'Bourg-Peronnas': u'Bourg Peronnas',
    'Bournemouth': u'AFC Bournemouth',
    'Braga': u'Sp Braga',
    'Brugge': u'Club Brugge',
    'Bueyueksehir': u'Büyüksehir',
    'Buyuksehyr': u'Büyüksehir',
    'Celta': u'Celta de Vigo',
    'Celta Vigo': u'Celta de Vigo',
    'Chievo': u'Chievo Verona',
    'Darmstadt': u'SV Darmstadt 98',
    'Den Haag': u'ADO Den Haag',
    'Depor': u'Deportivo La Coruña',
    'Dijon': u'Dijon FCO',
    'Dortmund': u'Borussia Dortmund',
    'Duesseldorf': u'Fortuna Düsseldorf',
    'Ein Frankfurt': u'Eintracht Frankfurt',
    'Entella': u'Virtus Entella',
    'Espanol': u'Espanyol',
    'EvianTG': u'Evian Thonon Gaillard',
    'Evian TG': u'Evian Thonon Gaillard',
    'FC Cologne': u'FC Köln',
    'FC Koln': u'FC Augsburg',
    'Forest': u'Nottingham Forest',
    'Fortuna Dusseldorf': u'Fortuna Düsseldorf',
    'Frankfurt': u'Eintracht Frankfurt',
    'Freiburg': u'SC Freiburg',
    'Fuerth': u'Greuther Furth',
    'Gijon': u'Sporting Gijón',
    'Gladbach': u'Borussia Mönchengladbach',
    'Groningen': u'FC Groningen',
    'Hamburg': u'Hamburg SV',
    'Hertha': u'Hertha Berlin',
    'Hoffenheim': u'TSG Hoffenheim',
    'Hull': u'Hull City',
    'Ingolstadt': u'FC Ingolstadt 04',
    'Inter': u'Internazionale',
    'Karabuekspor': u'Karabükspor',
    'Karabukspor': u'Karabükspor',
    'Kayseri': u'Kayserispor',
    'Koeln': u'FC Köln',
    'La Coruna': u'Deportivo La Coruña',
    'Lautern': u'Kaiserslautern',
    'Leicester': u'Leicester City',
    'Leverkusen': u'Bayer Leverkusen',
    "M'gladbach": u'Borussia Mönchengladbach',
    'Malaga': u'Málaga',
    'Man City': u'Manchester City',
    'Man United': u'Manchester United',
    'Milan': u'AC Milan',
    'Monaco': u'AS Monaco',
    'Muenchen 60': u'München 1860',
    'Munich 1860': u'München 1860',
    'Nancy': u'AS Nancy Lorraine',
    'Nijmegen': u'NEC Nijmegen',
    "Nott'm Forest": u'Nottingham Forest',
    'Nuernberg': u'Nürnberg',
    'Nurnberg': u'Nürnberg',
    'PSV Eindhoven': u'PSV',
    'Paris SG': u'Paris Saint-Germain',
    'Pescara': u'US Pescara',
    'Rennes': u'Stade Rennes',
    'Roda': u'Roda JC',
    'Roma': u'AS Roma',
    'Rostock': 'Hansa Rostock',
    'Saint-Etienne': u'St Etienne',
    'Schalke': u'Schalke 04',
    'Sevilla': u'Sevilla FC',
    'Sociedad': u'Real Sociedad',
    'Sp Gijon': u'Sporting Gijón',
    'Stoke': u'Stoke City',
    'Swansea': u'Swansea City',
    'Tottenham': u'Tottenham Hotspur',
    'Twente': u'FC Twente',
    'Utrecht': u'FC Utrecht',
    'Vallecano': u'Rayo Vallecano',
    'Waregem': u'Zulte Waregem',
    'Werder': u'Werder Bremen',
    'West Brom': u'West Bromwich Albion',
    'West Ham': u'West Ham United',
    'Wolfsburg': u'VfL Wolfsburg',
    'Wuerzburg': u'Würzburger Kickers',
    'Wurzburger Kickers': u'Würzburger Kickers',
    'Zwolle': u'PEC Zwolle'}

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
    },
    'SCO-Premiership': {
        'ClubElo': 'SCO_1',
        'MatchHistory': 'SC0',
        'MH_from_season': '9495'
    },  # Previously Scottish Premier League
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


class BaseReader(object):
    """Base class for datareaders"""

    def __init__(self, leagues=None):
        self._selected_leagues = leagues

    @staticmethod
    def _make_game_id(row):
        """Returns a game-id based on date, home and away team"""
        game_id = u'{} {}-{}'.format(
            row['date'].strftime("%Y-%m-%d"),
            row['home_team'],
            row['away_team']
        )
        return game_id

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
