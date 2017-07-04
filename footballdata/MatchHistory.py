# -*- coding: utf-8 -*-

from datetime import date
import itertools
import pandas as pd
import re
import warnings
from ._common import (BaseReader, Path, datadir, TEAMNAME_REPLACEMENTS)


class MatchHistory(BaseReader):
    """Provides pandas.DataFrames from CSV files available at
    http://www.football-data.co.uk/data.php

    Column names are explained here: http://www.football-data.co.uk/notes.txt

    Data will be downloaded as necessary and cached locally in ./data

    Parameters
    ----------
    leagues : string or iterable of league-ids to include, None for all
    seasons : string, int or list of seasons. Examples:
              '16-17'; 2016; '2016-17'; [14, 15, 16]
    """

    def __init__(self, leagues, seasons):
        super(MatchHistory, self).__init__(leagues=leagues)
        self.seasons = seasons

    def read_games(self):
        """Returns game history for the selected leagues and
        seasons in a pandas.DataFrame.
        """

        urlmask = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
        filemask = 'MatchHistory_{}_{}.csv'
        col_rename = {
            'Div': 'league',
            'Date': 'date',
            'HomeTeam': 'home_team',
            'AwayTeam': 'away_team',
        }

        df_list = []
        current_season_ends = str(date.today().year)[-2:]
        for lkey, skey in itertools.product(self._selected_leagues.values(),
                                      self.seasons):
            filepath = Path(datadir(), filemask.format(lkey, skey))
            url = urlmask.format(skey, lkey)
            current_season = skey[-2:] >= current_season_ends
            if current_season or (not filepath.exists()):
                self._download_and_save(url, filepath)

            df_list.append(
                pd.read_csv(str(filepath),
                            parse_dates=['Date'],
                            infer_datetime_format=True,
                            dayfirst=True,
                            encoding='UTF-8',
                            )
                    .assign(season=skey)
            )

        df = (
            pd.concat(df_list)
            .rename(columns=col_rename)
            .pipe(self._translate_league)
            .replace({'home_team': TEAMNAME_REPLACEMENTS,
                      'away_team': TEAMNAME_REPLACEMENTS})
            .dropna(subset=['home_team', 'away_team'])
        )

        df['game_id'] = df.apply(self._make_game_id, axis=1)
        df.set_index(['league', 'season', 'game_id'], inplace=True)
        df.sort_index(inplace=True)
        return df

    @staticmethod
    def _season_code(season):
        """Takes a string or int and tries to convert it to a
        season code like '1718'
        """
        season = str(season)
        pat1 = re.compile(r'^[0-9]{4}$')  # 1994 | 9495
        pat2 = re.compile(r'^[0-9]{2}$')  # 94
        pat3 = re.compile(r'^[0-9]{4}-[0-9]{4}$')  # 1994-1995
        pat4 = re.compile(r'^[0-9]{4}-[0-9]{2}$')  # 1994-95
        pat5 = re.compile(r'^[0-9]{2}-[0-9]{2}$')  # 94-95

        if re.match(pat1, season):
            if int(season[2:]) == int(season[:2]) + 1:
                if season == '1920' or season == '2021':
                    msg = ('Season id "{}" is ambiguous: interpreting as "{}-{}"'
                           .format(season, season[:2], season[-2:]))
                    warnings.warn(msg)
                return season  # 9495
            elif season[2:] == '99':
                return ''.join([season[2:], '00'])  # 1999
            else:
                return ''.join([season[-2:], '{:02d}'.format(int(season[-2:]) + 1)])  # 1994
        elif re.match(pat2, season):
            if season == '99':
                return ''.join([season, '00'])  # 99
            else:
                return ''.join([season, '{:02d}'.format(int(season) + 1)])  # 94
        elif re.match(pat3, season):
            return ''.join([season[2:4], season[-2:]])  # 1994-1995
        elif re.match(pat4, season):
            return ''.join([season[2:4], season[-2:]])  # 1994-95
        elif re.match(pat5, season):
            return ''.join([season[:2], season[-2:]])  # 94-95
        else:
            return season

    @classmethod
    def _download_and_save(cls, url, filepath):
        """Downloads file at url to filepath
        Overwrites if filepath exists
        """
        super(MatchHistory, cls)._download_and_save(url, filepath)

        # Strip trailing commas from Excel-generated csv, fix encoding
        filepath_tmp = Path('tmpfile')
        with filepath_tmp.open(mode='w', encoding='UTF-8') as tmpfile:
            with filepath.open(mode='r', encoding='ISO-8859-1') as file:
                for line in file.readlines():
                    tmpfile.write(line.rstrip(',\n'))
                    tmpfile.write(u'\n')
        filepath_tmp.rename(filepath)

    @property
    def seasons(self):
        return self._season_ids

    @seasons.setter
    def seasons(self, seasons):
        if isinstance(seasons, str) or isinstance(seasons, int):
            seasons = [seasons]
        self._season_ids = [self._season_code(s) for s in seasons]
