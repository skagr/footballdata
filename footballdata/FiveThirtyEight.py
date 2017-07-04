# -*- coding: utf-8 -*-

import json
import numpy as np
import pandas as pd
from ._common import (BaseReader, Path, datadir, TEAMNAME_REPLACEMENTS)


class FiveThirtyEight(BaseReader):
    """ Provides pandas.DataFrames from the fivethirtyeight.com project
    "2016-17 Club Soccer Predictions"

    Data will be downloaded as necessary and cached locally in ./data

    Original project and background info:
    https://projects.fivethirtyeight.com/soccer-predictions/
    https://fivethirtyeight.com/features/how-our-club-soccer-projections-work/

    Source JSON:
    https://projects.fivethirtyeight.com/soccer-predictions/data.json

    Parameters
    ----------
    leagues : string or iterable of league-ids to include, None for all
    """

    def __init__(self, leagues=None):
        super(FiveThirtyEight, self).__init__(leagues=leagues)
        self._data = {}

        url = 'https://projects.fivethirtyeight.com/soccer-predictions/data.json'
        filepath = Path(datadir(), 'FiveThirtyEight_1617.json')
        if not filepath.exists():
            self._download_and_save(url, filepath)

        with filepath.open(encoding='utf-8') as data_file:
            for k, v in json.load(data_file).items():
                self._data[k] = v

    def read_leagues(self):
        """Returns a Dataframe of selected leagues from the datasource"""
        df = (
            pd.DataFrame.from_dict(self._data['leagues'])
            .rename(columns={'slug': 'league', 'id': 'league_id'})
            .pipe(self._translate_league)
            .set_index('league')
            .loc[self._selected_leagues.keys()]
            .sort_index()
        )
        return df

    def read_games(self):
        """Returns a Dataframe of all games for the selected leagues"""

        col_rename = {
            'adj_score1': 'adj_score_home',
            'adj_score2': 'adj_score_away',
            'chances1': 'chances_home',
            'chances2': 'chances_away',
            'datetime': 'date',
            'moves1': 'moves_home',
            'moves2': 'moves_away',
            'prob1': 'prob_home',
            'prob2': 'prob_away',
            'probtie': 'prob_tie',
            'score1': 'score_home',
            'score2': 'score_away',
            'team1': 'home_team',
            'team1_code': 'home_code',
            'team1_id': 'home_id',
            'team1_sdr_id': 'home_sdr_id',
            'team2': 'away_team',
            'team2_code': 'away_code',
            'team2_id': 'away_id',
            'team2_sdr_id': 'away_sdr_id'
        }

        keys = [(v, v + '_matches') for v in self._selected_leagues.values()]

        df = (
            pd.concat(
                [(pd.DataFrame.from_dict(self._data[mkey])
                  .assign(league=lkey)
                  ) for lkey, mkey in keys]
            )
            .rename(columns=col_rename)
            .assign(date=lambda x: pd.to_datetime(x['date']))
            .replace({'home_team': TEAMNAME_REPLACEMENTS,
                      'away_team': TEAMNAME_REPLACEMENTS})
            .drop('id', axis=1)
            .assign(season='1617')
            .replace('None', np.nan)
            .pipe(self._translate_league)
        )

        df['game_id'] = df.apply(self._make_game_id, axis=1)
        df.set_index(['league', 'season', 'game_id'], inplace=True)
        df.sort_index(inplace=True)
        return df

    def read_forecasts(self):
        """Returns a Dataframe of forecasted results for all games for the selected leagues"""
        keys = [(v, v + '_forecast') for v in self._selected_leagues.values()]

        df_list = []
        for lkey, fkey in keys:
            forecast_by_date = self._data[fkey]['forecasts']
            df_list += [
                (pd.DataFrame.from_dict(f['teams'])
                    .assign(league=lkey)
                    .assign(
                    last_updated=lambda x: pd.to_datetime(f['last_updated']))
                ) for f in forecast_by_date]

        df = (pd.concat(df_list)
              .rename(columns={'name': 'team'})
              .replace({'team': TEAMNAME_REPLACEMENTS})
              .replace('None', np.nan)
              .pipe(self._translate_league)
              .set_index(['league', 'last_updated', 'team'])
              .sort_index()
              )
        return df

    def read_clinches(self):
        """Returns a Dataframe of clinches for the selected leagues"""
        keys = [(v, v + '_clinches') for v in self._selected_leagues.values()]

        df = (pd.concat([(pd.DataFrame.from_dict(self._data[ckey])
                          .assign(league=lkey)
                          ) for lkey, ckey in keys]
                        )
              .assign(date=lambda x: pd.to_datetime(x['dt']))
              .drop('dt', axis=1)
              .pipe(self._translate_league)
              .set_index(['league', 'date'])
              .sort_index()
              )
        return df
