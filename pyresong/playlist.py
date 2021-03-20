import xml.etree.ElementTree as ElementTree
from json import dumps
from datetime import datetime as dt
from datetime import timedelta
from .playitem import PlayItem
from os.path import isfile



class PlayList(object):
    """
    Object containing multiple PlayItems and supporting functions for playlist simple playlist manipulation.
    """

    DEFAULT_FRAGMENT_ACTIVATOR = '.'

    def __new__(cls, *args, **kwargs):
        """ Create an empty PlayList instance."""
        instance = super(PlayList, cls).__new__(cls, *args, **kwargs)
        instance.Items = []
        return instance

    def __init__(self):
        """
        Initialize an empty PlayList object.
        """
        pass

    def __str__(self):
        """
        Returns a XML string representation of the PlayList.
        """

        tmp = ""
        try:
            for i in self.Items:
                tmp+=str(i)+"\n"
        except Exception:
            pass
        return f"<PlayList>\n{tmp}</PlayList>"
     
    def __repr__(self):
        """
        Returns a simplified string version of the object with the following structure:

        'PlayList from (datetime_of_start) to (datetime_of_end)'
        """

        try:
            return f"Playlist from {self.Items[0].Vrijeme} to {self.Items[len(self.Items)-1].EndOfSongTime}"
        except Exception:
            try:
                return f"Playlist from {self.Items[0].Vrijeme}"
            except Exception:
                return "Empty playlist."
     
    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.Items):
            raise StopIteration

        result = self.Items[self._index]
        self._index += 1
        return result

    def __getitem__(self, key):
        return self.Items[key]
    
    def find(self, string, caps_sensitive=False, fragment_activator=DEFAULT_FRAGMENT_ACTIVATOR):
        """
        Find all items in the playlist if the string can be found in its Naziv, Autor, Album, Info or PathName.
        Returns generator with indexes of all items containing that string.
        
        Fragmented => the string is split by spaces, and each "fragments" is used as a search word
        To search by fragments define a "fragment_activator" (default is ".")
        """
        return [i for i in self.find_iter(string, caps_sensitive, fragment_activator)]

    def find_iter(self, string, caps_sensitive=False, fragment_activator=DEFAULT_FRAGMENT_ACTIVATOR):
        """
        Iteratively find all items in the playlist if the string can be found in its Naziv, Autor, Album, Info or PathName.
        Returns generator with indexes of all items containing that string.
        
        Fragmented => the string is split by spaces, and each "fragments" is used as a search word
        To search by fragments define a "fragment_activator" (default is ".")
        """
        fragment = False
        if string.startswith(fragment_activator):
            fragment = True
            string = string[len(fragment_activator):]
        string = string if caps_sensitive else string.lower()
        fragmented = string.split() if fragment else [string]
        loc=-1
        for i in self.Items:
            loc+=1
            params = [str(u) if caps_sensitive else str(u).lower() for u in [i.Naziv, i.Autor, i.Album, i.Info, i.PathName]]
            if True in [ True in [f in x for f in fragmented] for x in params]:
                yield loc

    def first(self, string, caps_sensitive=False, fragment_activator=DEFAULT_FRAGMENT_ACTIVATOR):
        """
        Search first item in the playlist if the string can be found in its Naziv, Autor, Album, Info or PathName.
        Returns the first item found.
        
        Fragmented => the string is split by spaces, and each "fragments" is used as a search word
        To search by fragments define a "fragment_activator" (default is ".")
        """

        #TODO: try/except
        return self.search(string, caps_sensitive, fragment_activator)[0]

    def search(self, string, caps_sensitive=False, fragment_activator=DEFAULT_FRAGMENT_ACTIVATOR):
        """
        Search all items in the playlist if the string can be found in its Naziv, Autor, Album, Info or PathName.
        Returns all items containing that string.
        
        Fragmented => the string is split by spaces, and each "fragments" is used as a search word
        To search by fragments define a "fragment_activator" (default is ".")
        """

        #TODO: try/except
        return [i for i in self.search_iter(string, caps_sensitive, fragment_activator)]

    def search_iter(self, string, caps_sensitive=False, fragment_activator=DEFAULT_FRAGMENT_ACTIVATOR):
        """
        Iteratively search all items in the playlist if the string can be found in its Naziv, Autor, Album, Info or PathName.
        Returns generator with all items containing that string.
        
        Fragmented => the string is split by spaces, and each "fragments" is used as a search word
        To search by fragments define a "fragment_activator" (default is ".")
        """
        for index in self.find_iter(string, caps_sensitive, fragment_activator):
            yield self.Items[index]

    @classmethod
    def fromxml(cls, xmltree):
        """
        Create a PlayList from a xml.etree.ElementTree.Element containing PlayList data.
        Will raise TypeException it value passed is not of type xml.etree.ElementTree.Element.

        """

        if xmltree.__class__ is str:
            try:
                xmltree= ElementTree.fromstring(xmltree)
            except Exception:
                raise TypeError('The XML string doesn\'t contain valid PlayList data')

        elif xmltree.__class__ is not ElementTree.Element:
            raise TypeError('The object is not a valid xml.etree.ElementTree.Element object!')

        self = cls()
        self.Items = [PlayItem.fromxml(item) for item in list(xmltree)]
        return self

    @classmethod
    def fromdict(cls, data):
        """
        Create a PlayList from a dictionary object containing PlayList data.
        Will raise TypeException it value passed is not of dict or collections.OrderedDict!

        """

        if data.__class__ is not dict and data.__class__ is not collections.OrderedDict:
            raise TypeError('The object is not a valid dict or collections.OrderedDict object!')

        self = cls()

        if 'PlayList' not in data:
            raise ValueError('data does not contain valid playlist data!')
        if 'PlayItem' in data['PlayList']:
            self.Items = [PlayItem.fromdict(item) for item in data['PlayList']['PlayItem']]
        elif data['PlayList'] is list:
            self.Items = [PlayItem.fromdict(item) for item in data['PlayList']]

        self.Items = [PlayItem.fromdict(item) for item in data['PlayList']['PlayItem']]
        return self

    @classmethod
    def frompath(cls, path):
        """
        Creates a PlayList instance from a given file path.
        """
        temp = cls()
        if not isfile(path):
            raise FileNotFoundError('The path is not a file')
        with open(path, 'br') as file:
            temp = PlayList.fromxml(file.read().decode('windows-1250'))
        return temp
    
    @staticmethod
    def get_xml_element(playlist):
        """
        Return the playlist object as a xml.etree.ElementTree.Element object.
        """

        return ElementTree.fromstring(PlayList.toxml(playlist))
    
    @staticmethod
    def tojson(playlist):
        """
        Returns a JSON string representation of the PlayList.
        """
        return json.dumps({'PlayList': {'PlayItem': [{str(key): str(val) for key,val in x.__dict__.items()} for x in playlist.Items]}})

    @staticmethod
    def toxml(playlist):
        """
        Returns a XML string representation of the PlayList.
        """
        return str(playlist)



