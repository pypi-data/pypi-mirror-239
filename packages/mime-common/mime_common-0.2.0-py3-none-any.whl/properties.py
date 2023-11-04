"""
Helper class for reading properties from file

"""
from __future__ import annotations
import logging
from typing import Iterator

PROPERTIES_DEFAULT_FILE = 'pyscript.properties'

class Properties:
    """
    Class for handling getting values from .properties file

    Attributes:
    -----------
    *BOOL_MAPPING* : dict[str, bool]
        Contains mapping from String to boolean value

    *LEVEL_MAPPING* : dict[str, bool]
        Contains mapping from level string to integer value

    *filename* : str
        Filename that's beeing opened
    """

    BOOL_MAPPING: dict[str, bool] = {
        'true': True,
        'false': False,
        'yes': True,
        'no': False,
        'ja': True,
        'nei': False,
        'sann': True,
        'usann': False,
        '1': True,
        '0': False,
    }
    
    #Levels: NOTSET=0, DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
    LEVEL_MAPPING: dict[str, int] = {
        'notset': logging.NOTSET,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    filename: str = None

    def __init__(self, filename=PROPERTIES_DEFAULT_FILE) -> None:
        """
        Parameters
        ----------
        *filename* : str, optional
            Which properties file to open.
        """
        self.filename: str = filename
#        self.more = None
        self.open()

    # Start of Iterator implementation
    def __getitem__(self, name):
        return self.props[name]
    def __iter__(self) -> Iterator:
        return iter(self.props)
    def keys(self):# -> dict_keys:
        """Get all property keys"""
        return self.props.keys()
    def items(self):# -> dict_items:
        """Get all property items"""
        return self.props.items()
    def values(self):
        """get all property values"""
        return self.props.values()
    # End of Iterator implementation

    def open(self) -> None:
        # TODO: Add error handling if file doesn't exist
        with open(self.filename) as f:
            self.props = {}
            for line in f:
                line = line.strip()
                if not line:
                    continue    # pragma: no cover
                if line.startswith('#'):
                    continue
                # TODO: Also support ' = ' with the spaces'
                key, value = line.split('=', 1)
                self.props[key] = value

    def get_str(self, prop:str, default='') -> str:
        """Read value from properties as string"""
        return self.props.get(prop, default)

    def get_int(self, prop:str, default=-1) -> int:
        """Read value from properties as integer"""
        return int(self.props.get(prop, default))

    def get_bol(self, prop:str, default=False) -> bool:
        """Read value from properties as boolean"""
        return self.BOOL_MAPPING.get(self.props.get(prop, 'false').lower(), default)

    def get_lvl(self, prop:str, default='notset') -> int:
        """Get logglevel integer value from string"""
        return self.LEVEL_MAPPING.get(self.props.get(prop, default).lower(), default)
