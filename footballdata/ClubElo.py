from datetime import datetime, timedelta
import pandas as pd
from .common import (_BaseReader, Path, datadir, TEAMNAME_REPLACEMENTS)


class ClubElo(_BaseReader):
    """Provides pandas.DataFrames from CSV API at http://api.clubelo.com

    Data will be downloaded as necessary and cached locally in ./data
    """

    def read_by_date(self, date=None):
        """Returns ELO scores for all teams at specified date in
        a pandas.DataFrame.

        If no date is specified, get today's scores

        Parameters
        ----------
        date : datetime object or string like 'YYYY-MM-DD'
        """

        # TODO: filter by league (country, level)

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
              .rename(columns={'Club': 'Team'})
              )

        df.replace(
            {'Team': TEAMNAME_REPLACEMENTS},
            inplace=True
        )
        df = df.reset_index().set_index('Team')
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

        teams_to_check = [k.replace(' ', '') for k, v in TEAMNAME_REPLACEMENTS.items() if v == team]
        teams_to_check.append(team.replace(' ', ''))

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
                  .rename(columns={'Club': 'Team'})
                  .set_index('From')
                  .sort_index()
                  )
            if len(df) > 0:
                df.replace(
                    {'Team': TEAMNAME_REPLACEMENTS},
                    inplace=True
                )
                return df

        # clubelo.com returns a CSV with just a header for nonexistent club
        raise ValueError('No data found for club {}'.format(team))
