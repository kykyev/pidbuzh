# -*- coding: utf-8 -*-
"""
This module contains all related to writer to target directory.
"""
from __future__ import print_function

import jinja2 as jin
import pidbuzh.utils as putils
import os


def write2file(file, content):
    file.seek(0)
    file.write(content)
    file.truncate()


class Writer(object):
    """ """
    def __init__(self, source, target, regexp=None, logger=print):
        self.source = source
        self.target = target
        self.regexp = regexp
        self.ignore_prefix = "_"
        self.logger = logger
        self.loader = jin.FileSystemLoader(source)
        self.env = jin.Environment(loader=self.loader, cache_size=0)

    def generate(self, paths=None):
        """ """
        if paths is None:
            self._gen_all()
        if isinstance(paths, list):
            self._gen_list(paths)
        if isinstance(paths, basestring):
            self._get_single()

    def _gen_single(self, relpath):
        tmpl = self.env.get_template(relpath)
        content = tmpl.render()
        fileobj = open(os.path.join(self.target, relpath), 'w')
        self.logger("Regen file {}".format(os.path.join(self.target, relpath)))
        write2file(fileobj, content)

    def _gen_list(self, relpaths):
        for path in set(relpaths):
            self._gen_single(path)

    def _gen_all(self):
        for path in putils.file_walker(self.source, self.regexp):
            if path.rpartition('/')[2][0] != "_":
                self._gen_single(path)
