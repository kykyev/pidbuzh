# -*- coding: utf-8 -*-
"""
This module contains all related to reader of source directory.
"""

import jinja2 as jin
import jinja2.meta as jinmeta
import pidbuzh.utils as putils


class TemplateLoader(jin.BaseLoader):
    """ """
    def __init__(self, root_path):
        self.root_path = root_path
        self.loader = jin.FileSystemLoader(self.root_path)
        self.ext_loader = jin.PrefixLoader({})

    def get_source(self, environment, template):
        if template[0] != '!':
            return self.loader.get_source(environment, template)
        return self.ext_loader.get_source(environment, template[1:])

    def register_external_location(self, prefix, location):
        self.ext_loader.mapping[prefix] = jin.FileSystemLoader(location)


class Loader(object):
    """ """
    def __init__(self, root_path):
        self.root = root_path
        self.template_loader = TemplateLoader(self.root)
        self.env = jin.Environment(loader=self.template_loader)

    def __call__(self, relpath):
        return self.template_loader.get_source(self.env, relpath)[0]

    def do_load(self, relpath):
        return self.template_loader.get_source(self.env, relpath)[0]

    def register_external_location(self, prefix, location):
        self.template_loader.ext_loader.mapping[prefix] = jin.FileSystemLoader(location)


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
        deps = set(d for d in jinmeta.find_referenced_templates(ast) if d[0] != '!')
        return deps
