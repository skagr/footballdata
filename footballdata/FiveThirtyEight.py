import json

import numpy as np
import pandas as pd

from .common import (_BaseReader, Path, datadir)

#TODO teamname replacements

class FiveThirtyEight(_BaseReader):
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

        url =  'https://projects.fivethirtyeight.com/soccer-predictions/data.json'
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
        keys = [(v, v + '_matches') for v in self._selected_leagues.values()]

        df = (
            pd.concat(
                [(pd.DataFrame.from_dict(self._data[mkey])
                  .assign(league=lkey)
                ) for lkey, mkey in keys]
            )
                .replace('None', np.nan)
                .assign(datetime=lambda x: pd.to_datetime(x['datetime']))
                .pipe(self._translate_league)
                .set_index(['league', 'datetime', 'id'])
                .sort_index()
        )
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
              .replace('None', np.nan)
              .pipe(self._translate_league)
              .set_index(['league', 'last_updated', 'name'])
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
