#!/usr/bin/env python2

from os.path import exists, splitext
from random import randint


_depth = lambda x, y, z=1: z

_invert_dict = lambda d: dict((v, k) for k, v in d.iteritems())

_PREFERRED_RGB = {
    'R': 0,
    'G': 1,
    'B': 2,
}


def depth(array):
    '''Return the depth (the third dimension) of an array.'''
    return _depth(*array.shape)


def rand_filename(filename, ext=None):
    '''Return a unique file name based on the given file name.'''
    file_name, file_ext = splitext(filename)
    if ext is None:
        ext = file_ext
    while True:
        rand_file_name = file_name
        rand_file_name += '-'
        rand_file_name += str(randint(0, 10000))
        rand_file_name += ext
        if not exists(rand_file_name):
            break
    return rand_file_name


if __name__ == '__main__':
    pass
