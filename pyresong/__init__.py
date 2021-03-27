"""
PyreSong Radio Automation Software Python Support Package

This is a python package support for the PyreSong radio automation software suite.
With includedd features like loading simple xml playlists and data conversion suport.
"""

from .playitem import PlayItem
from .playlist import PlayList
from .loadsave import load, save

TEST_ITEM=PlayItem()
TEST_ITEM.Naziv='Monke'


__author__ = "Borno Stojak (borno.stojak@gmail.com)"
__credits__ = ["Borno Stojak"]

__version__ = "0.0.1"
__status__ = "Development"
