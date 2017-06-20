import requests
import sys


if sys.version_info >= (3, 4):
    from pathlib import Path
else:
    from pathlib2 import Path


TEAMNAME_REPLACEMENTS = {
    'Alkmaar': 'AZ',
    'AZ Alkmaar': 'AZ',
    'Den Haag': 'ADO',
    'Nijmegen': 'NEC',
    'PSV Eindhoven': 'PSV',
    'Roda': 'Roda JC',
    'Sparta Rotterdam': 'Sparta',
    'Twente': 'FC Twente',
    'Zwolle': 'PEC Zwolle'
}


def datadir(dir='data'):
    """Return pathlib.Path to <cwd>/data
    Creates this directory if it doesn't exist
    """
    path = Path(dir)
    if not path.exists():
        path.mkdir()
    return path


def download_and_save(url, filepath):
    """Downloads file at url to filepath
    Overwrites if filepath exists
    """
    r = requests.get(url)
    r.raise_for_status()
    with filepath.open(mode='wb') as f:
        f.write(r.content)
