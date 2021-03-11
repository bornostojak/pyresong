from datetime import datetime as dt
from xml.etree import ElementTree as ElementTree
from datetime import timedelta
from collections import OrderedDict
from json import dumps
from os.path import isfile, splitext, basename
import mutagen


class PlayItem(object):
    """
    Object containing relevant song data.

    """

    def __new__(cls, *args, **kwargs):
        """
        Create the PlayItem instance and populate the default values.
        """

        instance = super(PlayItem, cls).__new__(cls, *args, **kwargs)
        instance.__dict__ = {'ID':-2,'Naziv':'','Autor':'','Album':'','Info':'','Tip':0,'Color':hex(0x9),'NaKanalu':0,'PathName':'','ItemType':3,'StartCue':0,'EndCue':0,'Pocetak':0,'Trajanje':0,'Vrijeme':Date.now(),'StvarnoVrijemePocetka':Date.min,'VrijemeMinTermin':Date.min,'VrijemeMaxTermin':Date.fromtimestamp(0),'PrviU_Bloku':0,'ZadnjiU_Bloku':0,'JediniU_Bloku':0,'FiksniU_Terminu':0,'Reklama':False,'WaveIn':False,'SoftIn':0,'SoftOut':0,'Volume':65536,'OriginalStartCue':0,'OriginalEndCue':0,'OriginalPocetak':0}
        
        return instance

    def __init__(self, data=None):
        """
        Initialize an empty PlayItem with no elements loaded.
        Can also parse from a dictionary of its items.

        """
        
        if type(data) is OrderedDict or type(data) is PlayItem: data = dict(data)
        if type(data) is dict :
            try:
                self.__dict__ = {key:val for key,val in tuple(data.items()) if key in self.__dict__.keys()}
            except:
                raise ValueError('The object contains invalid PlayItem data!')
            self._convert_attributes()

    def __str__(self):
        """
        Returns a XML string representation of the PlayItem.
        """

        try:
            return "<PlayItem>\n"+''.join([f"<{str(key)}>{str(val)}</{str(key)}>\n" if str(val).lower() != "none" else f"<{str(key)}/>\n" for key, val in self.__dict__.items()])+"</PlayItem>".replace('\\', '\\\\')
        except:
            return ""

    def __repr__(self):
        """
        Returns a simplified string version of the object with the following structure:

        'Author Name - Song Title @ Time Of Start'
        """

        try:
            return f"{self.Naziv+' by '+self.Autor if self.Autor else self.Naziv} @ {self.Vrijeme}"
        except:
            return "Empty item."

    def keys(self):
        """
        Returns all keys for given PlayItem.
        """
        return self.__dict__.keys()

    def __getitem__(self, key):
        """
        Returns the value for the given key.
        """
        return self.__dict__[key]
    
    def _convert_attributes(self):
        for key in list(self.__dict__):
            try:
                if 'Vrijeme'.lower() in key.lower():
                    self.__dict__[key] = Date.fromisoformat(self.__dict__[key])
                elif 'Color' == key:
                    continue
                elif str(self.__dict__[key]).lower() != "none":
                    place = eval(self.__dict__[key])
                    #if type(place) is float:
                    #    place = round(place, 4)
                    self.__dict__[key] = place
            except:
                place = self.__dict__[key]
                if type(place) is str:
                    place = place.replace('&', '&amp;')  #fixes issue with win paths
                self.__dict__[key] = place


    @property
    def Duration(self):
        """
        Returns a timedelta representation of the songs duration.
        It allows for simpler computing and calculating of song length with respect to datetime data.
        """
        return timedelta(seconds=self.Trajanje)

    @Duration.setter
    def Duration(self, value):
        self.Trajanje = value.total_seconds()
    
    @property
    def EndOfSongTime(self):
        """
        Returns the datetime data indicating when to pull the next item in the list.
        """
        return self.Vrijeme+self.Duration

    @classmethod
    def fromxml(cls, xmlitem):
        """
        Create a PlayItem from a xml.etree.ElementTree.Element containing PlayItem data.
        Will raise TypeException it value passed is not of type xml.etree.ElementTree.Element.
        Will raise KeyError it data passed contains incorrect or missing values!

        """
        if xmlitem.__class__ is str:
            try:
                xmlitem = ElementTree.fromstring(xmlitem)
            except:
                raise TypeError('The XML string doesn\'t contain valid PlayItem data')

        if xmlitem.__class__ is not ElementTree.Element:
            raise TypeError('The object is not a valid xml.etree.ElementTree.Element object!')

        try:
            self = cls()
            for i in range(len(xmlitem)):
                self.__dict__[xmlitem[i].tag] = xmlitem[i].text
            self._convert_attributes()
                
        except:
            raise KeyError('The PlayItem values are incorrect or missing!')
        return self
    
    @classmethod
    def fromdict(cls, data):
        """
        Create a PlayItem from a dictionary object containing PlayItem data.
        Will raise TypeError it value passed is not of dict or collections.OrderedDict!
        Will raise KeyError it data passed contains incorrect or missing values!

        """

        if data.__class__ is not dict and data.__class__ is not OrderedDict:
            raise TypeError('The object is not a valid dict or collections.OrderedDict object!')

        if 'PlayItem' in data:
            data = data['PlayItem']

        try:
            self = cls()
            for key in self.__dict__.keys():
                self.__dict__[key] = data[key]
            self._convert_attributes()
        except:
            raise KeyError('The PlayItem values are incorrect or missing!')
        
        return self

    @classmethod
    def frompath(cls, path):
        """ Creates a new playitem from a given file path. """
        temp = cls()
        try:
            if isfile(path): 
                temp.Trajanje = mutagen.File(path).info.length
                temp.OriginalTrajanje = temp.Trajanje
                temp.EndCue = temp.Trajanje
                temp.OriginalEndCue = temp.EndCue
                temp.Naziv = splitext(basename(path))[0]
                temp.PathName = path
                temp.Tip = 101
        except:
            pass

        return temp
        

    @staticmethod
    def tojson(playitem):
        """
        Returns a JSON string representation of the PlayItem.
        """
        return dumps({ str(key): str(val) for key, val in playitem.__dict__.items()})

    @staticmethod
    def toxml(playitem):
        """
        Returns a JSON string representation of the PlayItem.
        """
        return str(playitem)
        

class Date(dt):
    def __str__(self):
        return self.isoformat()

Date.min = Date.fromtimestamp(0)
Date.max = Date(9999,12,31)
