# -*- coding: utf-8 -*-
"""
This module contains all related to reader of source directory.
"""

import jinja2 as jin
import jinja2.meta as jinmeta
import pidbuzh.utils as putils


class Loader(object):
    """ """
    def __init__(self, root_path):
        self.root = root_path
        self.loader = jin.FileSystemLoader(self.root)
        self.env = jin.Environment(loader=self.loader)

    def __call__(self, relpath):
        return self.loader.get_source(self.env, relpath)[0]


class Reader(object):
    """ """
    def __init__(self, loader, regexp=None):
        self.loader = loader
        self.env = self.loader.env
        self.regexp = regexp

    def graph(self):
        d = {}
        for file_rel_path in putils.file_walker(self.loader.root, self.regexp):
            d[file_rel_path] = self._read(file_rel_path)
        return d

    def _read(self, relpath):
        ast = self.env.parse(self.loader(relpath))
        deps = set(jinmeta.find_referenced_templates(ast))
        return deps
