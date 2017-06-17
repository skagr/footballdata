Football Data Analysis Toolkit
==============================

.. image:: https://img.shields.io/pypi/v/footballdata.svg
    :target: https://pypi.python.org/pypi/footballdata
    :alt: Latest PyPI version

Status: Pre-Alpha

A collection of wrappers over football [*]_ data from various websites / APIs. Data is downloaded when needed, cleaned up and presented as (mostly) Pandas dataframes. Example Jupyter Notebooks are in the Github repo.

Data sources:

- http://www.football-data.co.uk/
- http://clubelo.com
- https://projects.fivethirtyeight.com/soccer-predictions

.. [*] Soccer, if you're a heathen 

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
    current_elo = elo.by_date()
    club_elo_history = elo.club_history('Barcelona')

Compatibility
-------------

Tested against Python 3.5 and 3.6

Licence
-------

MIT

Authors
-------

`Football Data Analysis Toolkit <https://github.com/skagr/footballdata>`_ was written by `Skag Rijsdijk <skag.rijsdijk@gmail.com>`_.
