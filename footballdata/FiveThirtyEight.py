import json
import pandas as pd
from pathlib import Path
import pprint

from footballdata.common import datadir, download_and_save


class FiveThirtyEight(object):
    """Provides pandas.DataFrames from 
    the fivethirtyeight.com project "2016-17 Club Soccer Predictions"

    Data will be downloaded as necessary and cached locally in ./data


    More info:
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

    @property
    def leagues(self):
        """A pandas.DataFrame of leagues"""
        df = (pd.DataFrame.from_dict(self._data['leagues'])
              .drop('id', axis=1)
              .rename(columns={'slug': 'id'})
              )

        df.set_index('id', inplace=True)
        df = df.loc[self._league_ids]
        return df.sort_index()

    @property
    def games(self):
        """A pandas.DataFrame of games"""
        keys = zip(self.league_ids, [l + '_matches' for l in self.league_ids])

        df = pd.concat([
            (pd.DataFrame.from_dict(self._data[mkey])
             .assign(league=lkey)
             .assign(datetime=lambda x: pd.to_datetime(x['datetime']))
             .set_index(['league', 'datetime', 'id'])
             ) for lkey, mkey in keys])

        return df.sort_index()

    @property
    def forecasts(self):
        """A pandas.DataFrame of forecasts"""
        keys = zip(self.league_ids, [l + '_forecast' for l in self.league_ids])

        for lkey, fkey in keys:
            forecast_by_date = self._data[fkey]['forecasts']
            df = pd.concat([
                (pd.DataFrame.from_dict(f['teams'])
                 .assign(league=lkey)
                 .assign(
                    last_updated=lambda x: pd.to_datetime(f['last_updated']))
                    .set_index(['last_updated', 'league', 'name'])
                 ) for f in forecast_by_date])

        return df.sort_index()

    @property
    def clinches(self):
        """A pandas.DataFrame of clinches"""
        keys = zip(self.league_ids, [l + '_clinches' for l in self.league_ids])

        df = pd.concat([
            (pd.DataFrame.from_dict(self._data[ckey])
             .assign(league=lkey)
             # This breaks pandas during pytest:
             # .assign(date=lambda x: pd.to_datetime(x['dt']))
             ) for lkey, ckey in keys])

        df['date'] = pd.to_datetime(df['dt'])
        df.drop('dt', axis=1, inplace=True)
        df.set_index(['league', 'date'], inplace=True)
        return df.sort_index()

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
