Football Data Analysis Toolkit
==============================

.. image:: https://img.shields.io/pypi/v/footballdata.svg
    :target: https://pypi.python.org/pypi/footballdata
    :alt: Latest PyPI version

A collection of wrappers over football [*]_ data from various websites / APIs. You get: Pandas dataframes with sensible, matching column names across datasets. Data is downloaded when needed and cached locally. Example Jupyter Notebooks are in the Github repo.

Status: Pre-Alpha

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

- `Pandas <http://pandas.pydata.org/>`_
- `Requests <http://docs.python-requests.org/en/master/>`_

Usage
-----

.. code:: python

    import footballdata as foo

    # Create class instances
    five38 = foo.FiveThirtyEight()
    elo = foo.ClubElo()

    # Create dataframes
    matches = five38.matches()
    forecasts = five38.forecasts()
    current_elo = elo.by_date()
    club_elo_history = elo.club_history('Barcelona')

See the Jupyter Notebooks here for more elaborate examples: https://github.com/skagr/footballdata/tree/master/notebooks

Compatibility
-------------

Tested against Python 3.5 and 3.6

Licence
-------

MIT
