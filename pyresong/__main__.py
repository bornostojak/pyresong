from .loadsave import *
from functools import reduce
from sys import argv
from os import path


def merge(files, savefile, overwrite=False):
    save(reduce(lambda x,y: x+y, (load(x) for x in files)), savefile, overwrite)

def main():
    if 'merge' in argv:
        merge([x for x in argv[1:-1] if path.exists(x)], argv[-1], '-O' in argv)




if __name__ == '__main__':
    main()

