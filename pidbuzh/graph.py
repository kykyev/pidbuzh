# -*- coding: utf-8 -*-
"""
This module contains all related to dependency graph.
"""

import itertools as it
import numpy as np


class GraphIsInvalid(Exception):
    pass


class DepGraph(object):
    """
    """
    def __init__(self, dict_of_sets):
        """
        Takes dict of lists:
            node_id => [list of dependencies]
        """
        self._orig_dict_of_sets = dict_of_sets

        self._node_to_index_map, self._index_to_node_map, self._dict_of_sets = \
            self.sanity_check(dict_of_sets)

        self._deps_matrix = self.make_deps_matrix(self._dict_of_sets)
        self._deps_matrix_tclos = self.make_transitive_closure(self._deps_matrix)

    @property
    def deps_matrix(self):
        return self.__deps_matrix

    def depends_from(self, node_id):
        """
        Returns topologically sorted list of node IDs that are depended from a given `node_id`.
        """
        id = self._node_to_index_map[node_id]
        col = self._deps_matrix_tclos.transpose()[id - 1]
        return set(self._index_to_node_map[i] for i, j in
                   enumerate(np.squeeze(np.asarray(col)), 1) if j > 0)

    @staticmethod
    def sanity_check(dict_of_sets):
        """
        Checks that all nodes that are in dependency sets actually exist.
        """
        nodes = set(dict_of_sets.iterkeys())
        deps = set(it.chain(*dict_of_sets.itervalues()))
        if deps - nodes:
            raise GraphIsInvalid

        mapping = dict((y, x) for x, y in enumerate(nodes, 1))
        rmapping = dict((y, x) for x, y in mapping.iteritems())
        renamed_dict = dict(
            (mapping[k], set(mapping[_] for _ in v)) for k, v in dict_of_sets.iteritems()
        )

        return mapping, rmapping, renamed_dict

    @staticmethod
    def make_deps_matrix(dict_of_sets):
        """
        Constucts matrix representation of dependency graph.
        """
        Np1 = len(dict_of_sets) + 1
        dim2list = [dict_of_sets[i] for i in range(1, Np1)]
        return np.matrix([
            [1 if i in s else 0 for i in range(1, Np1)] for s in dim2list
        ])

    @staticmethod
    def make_transitive_closure(deps_matrix):
        """ """
        P = deps_matrix
        TC = deps_matrix
        while P.any():
            P = P * deps_matrix
            TC = TC + P
        return TC
