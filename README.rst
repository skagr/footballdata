Football Data Analysis Toolkit
==============================

.. image:: https://img.shields.io/pypi/v/footballdata.svg
    :target: https://pypi.python.org/pypi/footballdata
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/skagr/footballdata.png
   :target: https://travis-ci.org/skagr/footballdata
   :alt: Latest Travis CI build status


A collection of wrappers over football [*]_ data from various websites / APIs. You get: Pandas dataframes with sensible, matching column names and identifiers across datasets. Data is downloaded when needed and cached locally. Example Jupyter Notebooks are in the Github repo.

.. [*] Soccer, if you're a heathen

Data sources:
-------------

fivethirtyeight.com
~~~~~~~~~~~~~~~~~~~
(https://projects.fivethirtyeight.com/soccer-predictions)

Season 2016-17 predictions and results for the top European and American leagues.

football-data.co.uk
~~~~~~~~~~~~~~~~~~~
(http://www.football-data.co.uk/)

Historical results, betting odds and match statistics for English, Scottish, German, Italian, Spanish, French, Dutch, Belgian, Portuguese, Turkish and Greek leagues, including a number of lower divisions. Level of detail depends on league.

clubelo.com
~~~~~~~~~~~
(http://clubelo.com)

First team relative strengths, for all (?) European leagues. Recalculated after every round, includes history.

Roadmap:
--------

Add player stats, transfers, injuries and suspensions.


Installation
------------

.. code:: bash

    $ pip install footballdata

Dependencies
~~~~~~~~~~~~

- `Numpy <http://www.numpy.org/>`_
- `Pandas <http://pandas.pydata.org/>`_
- `Requests <http://docs.python-requests.org/en/master/>`_
- `Unidecode <https://pypi.python.org/pypi/Unidecode>`_

Usage
-----

.. code:: python

    import footballdata as foo

    # Create class instances
    five38 = foo.FiveThirtyEight()
    elo = foo.ClubElo()
    mhist = foo.MatchHistory('ENG-Premier League', '2016-17')

    # Create dataframes
    matches = five38.read_games()
    forecasts = five38.forecasts()
    current_elo = elo.read_by_date()
    team_elo_history = elo.read_team_history('Barcelona')
    epl_2016 = mhist.read_games()

See the Jupyter Notebooks here for more elaborate examples: https://github.com/skagr/footballdata/tree/master/notebooks

Compatibility
-------------

Tested against Python 2.7 and 3.4-3.6

Licence
-------

MIT
