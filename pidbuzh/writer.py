# -*- coding: utf-8 -*-
"""
This module contains all related to writer to target directory.
"""
from __future__ import print_function

import jinja2 as jin
import pidbuzh.utils as putils
import os

pjoin = os.path.join


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
        if relpath.rpartition('/')[2][0] != "_":
            tmpl = self.env.get_template(relpath)
            content = tmpl.render()
            self.logger("Regen file {}".format(pjoin(self.target, relpath)))
            putils.write2file(pjoin(self.target, relpath), content)

    def _gen_list(self, relpaths):
        for path in set(relpaths):
            self._gen_single(path)

    def _gen_all(self):
        for path in putils.file_walker(self.source, self.regexp):
            self._gen_single(path)
