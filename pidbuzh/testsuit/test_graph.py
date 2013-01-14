# -*- coding: utf-8 -*-

import pidbuzh.graph as pgraph
import nose.tools as ntools
import numpy as np

from ipdb import set_trace as ST


def is_bijection(mapping):
    image, preimage = set(mapping.itervalues()), set(mapping.iterkeys())
    if len(image) != len(preimage):
        return False
    return True


class TestSanityCheck(object):
    """ """
    @ntools.raises(pgraph.GraphIsInvalid)
    def test_fail(self):
        bogus_graph = {
            'a': set(['b', 'c']),
            'b': set([])
        }
        pgraph.DepGraph.sanity_check(bogus_graph)

    def test_ok(self):
        good_graph = {
            'a': set(['b', 'c', 'd']),
            'b': set(['d']),
            'c': set(['d']),
            'd': set([])
        }
        x, x1, y = pgraph.DepGraph.sanity_check(good_graph)

        assert is_bijection(x)
        assert is_bijection(x1)
        assert set(x.itervalues()) == {1, 2, 3, 4}
        assert set(x1.itervalues()) == {'a', 'b', 'c', 'd'}
        assert y == {
            x['a']: set([x['b'], x['c'], x['d']]),
            x['b']: set([x['d']]),
            x['c']: set([x['d']]),
            x['d']: set([])
        }


class TestMakeDepsMatrix(object):
    """ """
    def test_1(self):
        dict_of_lists = {
            1: [2, 4],
            2: [3],
            3: [4],
            4: []
        }
        matrix = pgraph.DepGraph.make_deps_matrix(dict_of_lists)

        assert (matrix == np.matrix([
                [0, 1, 0, 1],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 0]
            ])).all()


class TestMakeTransitiveClosure(object):
    """ """
    def test_1(self):
        A = np.matrix([
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, 1, 0, 1],
                [0, 0, 0, 0]
            ])
        TC = pgraph.DepGraph.make_transitive_closure(A)

        assert (TC == np.matrix([
                [0, 1, 1, 2],
                [0, 0, 0, 1],
                [0, 1, 0, 2],
                [0, 0, 0, 0]
            ])).all()


class TestDependsFrom(object):
    """ """
    def test_1(self):
        dg = {
            'a': set(['c']),
            'b': set(['d']),
            'c': set(['b', 'd']),
            'd': set([])
        }
        depgr = pgraph.DepGraph(dg)
        assert depgr.depends_from('d') == {'a', 'b', 'c'}
