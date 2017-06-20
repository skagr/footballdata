import json
import numpy as np
import pandas as pd
from pathlib import Path
import pprint

from footballdata.common import datadir, download_and_save


class FiveThirtyEight(object):
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
    league_ids : string or iterable of league-ids to include, None for all
    """

    def __init__(self, league_ids=None):
        self.league_ids = league_ids
        self._data = {}
        url = 'https://projects.fivethirtyeight.com/soccer-predictions/data.json'  # nopep8

        filepath = Path(datadir(), 'FiveThirtyEight_1617.json')
        if not filepath.exists():
            download_and_save(url, filepath)

        with filepath.open(encoding='utf-8') as data_file:
            for k, v in json.load(data_file).items():
                self._data[k] = v

    def leagues(self):
        df = (pd.DataFrame.from_dict(self._data['leagues'])
              .rename(columns={'slug': 'league', 'id': 'league_id'})
              )

        df.set_index('league', inplace=True)
        df = df.loc[self._league_ids]
        return df.sort_index()

    def games(self):
        keys = zip(self.league_ids, [l + '_matches' for l in self.league_ids])

        df = (pd.concat([
            (pd.DataFrame.from_dict(self._data[mkey])
             .assign(league=lkey)
             ) for lkey, mkey in keys])
            .replace('None', np.nan)
            .assign(league=lambda x: x['league'].astype('category'))
            .assign(id=lambda x: x['id'].astype('category'))
            .assign(leg=lambda x: x['leg'].astype('category'))
            .assign(round=lambda x: x['round'].astype('category'))
            .assign(status=lambda x: x['status'].astype('category'))
            .assign(team1=lambda x: x['team1'].astype('category'))
            .assign(team1_code=lambda x: x['team1_code'].astype('category'))
            .assign(team1_id=lambda x: x['team1_id'].astype('category'))
            .assign(team1_sdr_id=lambda x: x['team1_sdr_id'].astype('category'))
            .assign(team2=lambda x: x['team2'].astype('category'))
            .assign(team2_code=lambda x: x['team2_code'].astype('category'))
            .assign(team2_id=lambda x: x['team2_id'].astype('category'))
            .assign(team2_sdr_id=lambda x: x['team2_sdr_id'].astype('category'))
            .assign(datetime=lambda x: pd.to_datetime(x['datetime']))
            .set_index(['league', 'datetime', 'id']))

        return df.sort_index()

    def forecasts(self):
        keys = zip(self.league_ids, [l + '_forecast' for l in self.league_ids])

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
                .assign(league=lambda x: x['league'].astype('category'))
                .assign(name=lambda x: x['name'].astype('category'))
                .assign(code=lambda x: x['code'].astype('category'))
                .assign(conference=lambda x: x['conference'].astype('category'))
                .assign(group=lambda x: x['group'].astype('category'))
                .set_index(['league', 'last_updated', 'name'])
              )
        return df.sort_index()

    def clinches(self):
        keys = zip(self.league_ids, [l + '_clinches' for l in self.league_ids])

        df = (pd.concat([(pd.DataFrame.from_dict(self._data[ckey])
                          .assign(league=lkey)
                          ) for lkey, ckey in keys]
                        )
                .assign(date=lambda x: pd.to_datetime(x['dt']))
                .drop('dt', axis=1)
                .set_index(['league', 'date'])
                .sort_index()
              )

        return df

    @property
    def league_ids(self):
        return self._league_ids

    @league_ids.setter
    def league_ids(self, ids):
        if (ids is None) or (not hasattr(self, '_league_ids')):
            self._league_ids = ['premier-league', 'la-liga', 'bundesliga',
                                'serie-a', 'ligue-1', 'champions-league',
                                'mls', 'liga-mx', 'nwsl']

        if ids is not None:
            if len(ids) == 0:
                raise ValueError("Empty iterable not allowed for 'league_ids'")
            if isinstance(ids, str):
                ids = [ids]
            for x in ids:
                if x not in self._league_ids:
                    raise ValueError(
                        "Invalid league '{}'.\nValid leagues are:\n{}"
                        .format(x, pprint.pformat(self._league_ids)))
            self._league_ids = list(ids)

        self._league_ids.sort()
