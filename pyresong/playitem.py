from datetime import datetime as dt
from xml.etree import ElementTree as ElementTree
from datetime import timedelta
from collections import OrderedDict
from json import dumps
from os.path import isfile, splitext, basename
import mutagen
import re


class PlayItem(object):
    """
    Object containing relevant song data.

    """

    def __new__(cls, *args, **kwargs):
        """Create the PlayItem instance and populate the default values."""
        instance = super(PlayItem, cls).__new__(cls)
        instance.__dict__ = {'ID':-2,'Naziv':'','Autor':'','Album':'','Info':'','Tip':0,'Color':hex(0x9),'NaKanalu':0,'PathName':'','ItemType':3,'StartCue':0,'EndCue':0,'Pocetak':0,'Trajanje':0,'Vrijeme':DateTime.now(),'StvarnoVrijemePocetka':DateTime.min,'VrijemeMinTermin':DateTime.min,'VrijemeMaxTermin':DateTime.fromtimestamp(0),'PrviU_Bloku':0,'ZadnjiU_Bloku':0,'JediniU_Bloku':0,'FiksniU_Terminu':0,'Reklama':False,'WaveIn':False,'SoftIn':0,'SoftOut':0,'Volume':65536,'OriginalStartCue':0,'OriginalEndCue':0,'OriginalPocetak':0, 'OriginalTrajanje':0}
        return instance

    def __init__(self, data=None):
        """
        Initialize an empty PlayItem with no elements loaded.
        Can also parse from a dictionary of its items.

        """
        if data:
            self.__update(data)

    def __str__(self):
        """Returns a XML string representation of the PlayItem."""
        try:
            return "<PlayItem>\n"+''.join([f"<{str(key)}>{str(val).replace('&', '&amp;')}</{str(key)}>\n" if str(val).lower() != "none" else f"<{str(key)}/>\n" for key, val in self.__dict__.items()])+"</PlayItem>".replace('\\', '\\\\')
        except Exception:
            return ""

    def __repr__(self):
        """
        Returns a simplified string version of the object with the following structure:

        'Author Name - Song Title @ Time Of Start'
        """
        try:
            return f"{self.Naziv+' by '+self.Autor if self.Autor else self.Naziv} @ {self.Vrijeme}"
        except Exception:
            return "Empty item."

    def keys(self):
        """Returns all keys for given PlayItem."""
        return self.__dict__.keys()

    def __getitem__(self, key):
        """Returns the value for the given key."""
        return self.__dict__[key]
    
    def __convert_attributes(self):
        for key, val in self.__dict__.items():
            try:
                if 'Vrijeme'.lower() in key.lower():
                    val = DateTime.legacyisoformatparser(val)
                elif 'Color' == key:
                    continue
                elif str(val).lower() != "none":
                    val = eval(val)
            except Exception as e:
                if type(e) is ValueError:
                    raise e
                #if type(val) is str:
                    #val = val.replace('&', '&amp;')  #fixes issue with win paths
            self.__dict__[key] = val

    def __update(self, data):
        data=dict(data)
        if set(data) - set(self.__dict__):
            raise ValueError('The data passed to the item is invalid')
        try:
            self.__dict__.update({key:val for key,val in dict(data).items() if key in self.__dict__})
            self.__convert_attributes()
        except Exception:
            raise ValueError('The object contains invalid PlayItem data!')

    def clone(self):
        """Clone the item into separate item."""
        return PlayItem.fromdict(dict(self))

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
        """Returns the datetime data indicating when to pull the next item in the list."""
        return self.Vrijeme+self.Duration

    @classmethod
    def fromxml(cls, xmlitem):
        """
        Create a PlayItem from a xml.etree.ElementTree.Element containing PlayItem data.
        Will raise TypeException it value passed is not of type xml.etree.ElementTree.Element.
        Will raise KeyError it data passed contains incorrect or missing values!

        """
        if type(xmlitem) is str:
            try:
                xmlitem = ElementTree.fromstring(xmlitem)
            except Exception:
                raise TypeError('The XML string doesn\'t contain valid PlayItem data')

        if type(xmlitem) is not ElementTree.Element:
            raise TypeError('The object is not a valid xml.etree.ElementTree.Element object!')

        try:
            self = cls()
            for i in range(len(xmlitem)):
                self.__dict__[xmlitem[i].tag] = xmlitem[i].text
            self.__convert_attributes()
                
        except Exception:
            raise KeyError('The PlayItem values are incorrect or missing!')
        return self
    
    @classmethod
    def fromdict(cls, data):
        """Create a PlayItem from a dictionary object containing PlayItem data."""
        try:
            data = dict(data)
        except Exception:
            raise TypeError('The object is not a valid dict or collections.OrderedDict object!')

        if 'PlayItem' in data:
            data = data['PlayItem']

        try:
            self = cls()
            self.__update(data)
        except Exception:
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
        except Exception:
            pass

        return temp
        

    @staticmethod
    def tojson(playitem):
        """Returns a JSON string representation of the PlayItem."""
        return dumps({ str(key): str(val).replace('&', '&amp;') for key, val in playitem.__dict__.items()})

    @staticmethod
    def toxml(playitem):
        """Returns a xml Element for the given PlayItem."""
        return ElementTree.fromstring(str(playitem))
        

class DateTime(dt):
    UseTimeZoneStamp=True
    def __str__(self):
        return self.astimezone().isoformat() if DateTime.UseTimeZoneStamp else self.isoformat() 
    
    @staticmethod
    def legacyisoformatparser(string):
        parser=re.compile(r'(\d{4})-(\d{2})-(\d{2})(\w?)(\d{0,2})(:|\.?)(\d{0,2})(:|\.?)(\d{0,2})(:|\.?)(\d{6}|\d{0,3})(\d*)Z?(\+?.*)')
        if parser.match(string):
            return DateTime.fromisoformat(parser.sub(r'\1-\2-\3\4\5\6\7\8\9\10\11\13', string))
        else:
            raise ValueError('The time string is wrongly formatted')

DateTime.min = DateTime.fromtimestamp(0)
DateTime.max = DateTime(9999,12,31)

