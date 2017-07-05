# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import re
from unidecode import unidecode
from ._common import (BaseReader, Path, datadir,
                      TEAMNAME_REPLACEMENTS)


class ClubElo(BaseReader):
    """Provides pandas.DataFrames from CSV API at http://api.clubelo.com

    Data will be downloaded as necessary and cached locally in ./data

    Since the source does not provide league names, this class will
    not filter by league. League names will be inserted from the other
    sources where available. Leagues that are only covered by clubelo.com
    will have NaN values.
    """

    def __init__(self):
        super(ClubElo, self).__init__()

    def read_by_date(self, date=None):
        """Returns ELO scores for all teams at specified date in
        a pandas.DataFrame.

        If no date is specified, get today's scores

        Parameters
        ----------
        date : datetime object or string like 'YYYY-MM-DD'
        """

        if not date:
            date = datetime.today()
        elif isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        else:
            pass  # Assume datetime object

        datestring = date.strftime("%Y-%m-%d")
        filepath = Path(datadir(), 'ClubElo_{}.csv'.format(datestring))
        url = 'http://api.clubelo.com/{}'.format(datestring)

        if not filepath.exists():
            self._download_and_save(url, filepath)

        df = (pd.read_csv(str(filepath),
                          parse_dates=['From', 'To'],
                          infer_datetime_format=True,
                          dayfirst=False
                          )
              .rename(columns={'Club': 'team'})
              .replace({'team': TEAMNAME_REPLACEMENTS})
              .replace('None', np.nan)
              .assign(Rank=lambda x: x['Rank'].astype('float'))
              .assign(league=lambda x: x['Country'] + '_' + x['Level'].astype(str))
              .pipe(self._translate_league)
              .reset_index(drop=True)
              .set_index('team')
              )
        return df

    def read_team_history(self, team, max_age=1):
        """Downloads full ELO history for one team

        Returns pandas.DataFrame

        Parameters
        ----------
        team : string club name
        max_age : max. age of local file before re-download
                integer for age in days, or timedelta object
        """

        if isinstance(max_age, int):
            _max_age = timedelta(days=max_age)
        elif isinstance(max_age, timedelta):
            _max_age = max_age
        else:
            raise TypeError('max_age must be of type int or datetime.timedelta')

        teams_to_check = [k for k, v in TEAMNAME_REPLACEMENTS.items() if v == team]
        teams_to_check.append(team)

        for i, v in enumerate(teams_to_check):
            teams_to_check[i] = unidecode(teams_to_check[i])
            teams_to_check[i] = re.sub("[\s']", "", teams_to_check[i])

        for _team in teams_to_check:
            filepath = Path(datadir(), 'clubelo_{}.csv'.format(_team))
            url = 'http://api.clubelo.com/{}'.format(_team)

            if not filepath.exists():
                self._download_and_save(url, filepath)
            else:
                last_modified = datetime.fromtimestamp(filepath.stat().st_mtime)
                now = datetime.now()
                if (now - last_modified) > _max_age:
                    self._download_and_save(url, filepath)

            df = (pd.read_csv(str(filepath),
                              parse_dates=['From', 'To'],
                              infer_datetime_format=True,
                              dayfirst=False)
                  .rename(columns={'Club': 'team'})
                  .replace('None', np.nan)
                  .assign(Rank=lambda x: x['Rank'].astype('float'))
                  .set_index('From')
                  .sort_index()
                  )
            if len(df) > 0:
                df.replace({'team': TEAMNAME_REPLACEMENTS}, inplace=True)
                return df

        # clubelo.com returns a CSV with just a header for nonexistent club
        raise ValueError('No data found for team {}'.format(team))
