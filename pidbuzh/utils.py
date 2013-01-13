# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os
import re
from ipdb import set_trace as ST


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
