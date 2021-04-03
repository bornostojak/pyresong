from .playlist import PlayList
from .loadsave import *
from functools import reduce
from sys import argv


def merge(files, savefile, overwrite=False):
    save(reduce(lambda x,y: x+y, (load(x) for x in files), savefile, overwrite)

def main():
    if 'merge' in argv:
        merge(argv[1:-1], argv[-1], '-O' in argv)




if __naem__ == '__main__':
    main()

