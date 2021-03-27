from datetime import datetime as dt
from datetime import timedelta
from ..playitem import PlayItem
from .mixitem import MixItem
import collections
import xml.etree.ElementTree as ElementTree
import json

class Mix(object):
    """A static class for processing playlist mixing."""
    
    @staticmethod
    def Mix(playlist):
        mixlist = [MixItem(x) for x in playlist.Items]
        comaprator = None
    
        #pull data from database for each item in mixlist

        for item in mixlist:
            if not comparator:
                comparator = item
                continue
            _compatibility = Mix.compatibility(comparator, item)
            
        pass

    @staticmethod
    def compatibility(item_a, item_b):
        """ Compares two MixItem objects and returns their compatibiliy score float. """

        if not (item_a.__class__, item_b.__class__) == (MixItem, MixItem):
            raise TypeError('Both items must be of type pyresong.MixItem!')

        return 1.0
