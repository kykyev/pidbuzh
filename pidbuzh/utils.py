# -*- coding: utf-8 -*-

from contextlib import contextmanager

import os
import re
import shutil
import codecs


@contextmanager
def working_dir(path):
    oldcwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldcwd)


def write2file(path, content, encoding='utf-8'):
    try:
        with codecs.open(path, 'w', encoding) as fout:
                fout.write(content)
    except IOError as e:
        if e.errno == 2:
            # No such file or directory
            # Let's create it!
            os.makedirs(os.path.dirname(path))
            with codecs.open(path, 'w', encoding) as fout:
                fout.write(content)


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


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class FileTree(object):
    """ """
    def __init__(self, root):
        self.root = root

    def create(self, spec):
        """ """
        with working_dir(self.root):
            for path, content in spec.iteritems():
                if path[-1] == '/':
                    makedir(path)
                else:
                    write2file(path, content or '')
