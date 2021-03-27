from datetime import datetime as dt
from datetime import timedelta
from ..playitem import PlayItem
from xml.etree import ElementTree as ElementTree

class MixItem(PlayItem):
    """ Object containing data referenced while mixing PlayItems together. """
    def __new__(cls, *args, **kwargs):
        return super(MixItem, cls).__new__(cls, *args, **kwargs)

    def __init__(self, playitem=None):
        """ Initialize a MixItem by giving it a PlayItem to reference from. """
        if playitem:
            super(MixItem, self).__init__(playitem)
        


    ITERATIVE_DATA = {
            'Link':'At what point in the song does the transition happen', 
            'Border':'Is the transition on the start or end of the song. (is it a transition In or Out)',
            'Impact':['E', 'EM', 'M', 'MH', 'H'],
            'Type':['Swoope', 'Hard', ''],
            'Measure':'What measure in the time signature is the transition on.',
            'Acceleration':['Constant', 'Speedup', 'Slowdown'],
            'Volume':'Volume percentage on the fade slope where the link point should be.',
            'FadeLength':'The length of the fade.'}
    STATIC_DATA = ['VoxIn', 'VoxOut', 'Genre', 'Key', 'Style',]


class Transition(object):
    def __init__(self):
        pass
    
