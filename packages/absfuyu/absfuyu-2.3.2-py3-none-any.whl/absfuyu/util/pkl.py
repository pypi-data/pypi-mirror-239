"""
Absfuyu: Pickle
---
`pickle` wrapper

Version: 1.0.1
Last update: 17/08/2023 (dd/mm/yyyy)
"""


# Module level
###########################################################################
__all__ = [
    "Pickler"
]


# Library
###########################################################################
from pathlib import Path
import pickle
from typing import Any


# Class
###########################################################################
class Pickler:
    """Save and load pickle file"""
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def save(location: Path, data: Any) -> None:
        """
        Save to pickle format
        
        :param location: Save location
        :param data: Data want to saved
        """
        with open(location, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def load(location: Path) -> Any:
        """
        Load pickled file
        
        :param location: Load location
        """
        with open(location, "rb") as file:
            data = pickle.load(file)
        return data


# Run
###########################################################################
if __name__ == "__main__":
    pass