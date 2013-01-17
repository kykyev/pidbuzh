# -*- coding: utf-8 -*-

from contextlib import contextmanager

import os
import re
import shutil


@contextmanager
def working_dir(path):
    oldcwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldcwd)


def file_walker(rootpath, regexp=None):
    """
    Generator that recursively yields files.

        :rootpath:
        :regexp:
    """
    pjoin = os.path.join
    rpath = os.path.relpath
    regobj = re.compile(regexp) if regexp else None

    if regobj:
        for path, subfolders, files in os.walk(rootpath):
            for fl in files:
                if regobj.match(fl):
                    yield rpath(pjoin(path, fl), rootpath)
    else:
        for path, subfolders, files in os.walk(rootpath):
            for fl in files:
                yield rpath(pjoin(path, fl), rootpath)


def clear_dir(path):
    """TODO """
    pjoin = os.path.join
    isfile = os.path.isfile
    isdir = os.path.isdir
    unlink = os.unlink
    rmtree = shutil.rmtree

    for file_or_dir in (pjoin(path, _) for _ in os.listdir(path)):
        if isfile(file_or_dir):
            unlink(file_or_dir)
        elif isdir(file_or_dir):
            rmtree(file_or_dir)
