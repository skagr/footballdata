"""
A collection of tools to read and process football data
from various sources.
"""


__version__ = '0.1.0'
__author__ = 'Skag Rijsdijk <skag.rijsdijk@gmail.com>'
__all__ = ['FiveThirtyEight', 'ClubElo', 'MatchHistory']

from .FiveThirtyEight import FiveThirtyEight
from .ClubElo import ClubElo
from .MatchHistory import MatchHistory
