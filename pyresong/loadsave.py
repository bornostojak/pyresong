from .playlist import PlayList
from os.path import isfile, isdir, dirname, basename, splitext
from os import makedirs, getcwd
from platform import system as plsys

_SEPARATOR = '/'
if plsys().lower() == 'windows':
    _SEPARATOR = '\\'

def load(path):
    """Load a playlist from a file."""
    if not isfile(path):
        raise FileNotFoundError('The file could not be found')
    pl = None
    try:
        with open(path, 'rb') as file:
            pl = PlayList.frompath(path)
    except:
        raise ValueError('Make sure the file is not corrupt or missing')

    return pl

def save(playlist, path, overwrite=False):
    """Save a playlist to a file."""
    if not path:
        raise ValueError('The path cannot be empty!')

    directory = dirname(path)
    name, ext = splitext(basename(path))

    if not ext:
        ext = '.fps.xml'
    if not directory:
        #TODO: create a config to pull default save dir from and else use getcwd()
        directory = getcwd()
    if not isdir(directory):
        makedirs(directory)

    path = directory+_SEPARATOR+name+ext

    if isdir(path):
        raise ValueError('The path is a directory. Please pass a valid file path.')

    if isfile(path) and not overwrite:
        raise FileExistsError('The file already exists. User "overwrite=True to overwrite it."')

    prev=None
    for item in playlist:
        if prev:
            item.Vrijeme = prev.EndOfSongTime
        prev = item
    
    with open(path, 'wb') as file:
        file.write(str(playlist).encode('windows-1250'))
