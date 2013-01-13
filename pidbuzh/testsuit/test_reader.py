# -*- coding: utf-8 -*-

import pidbuzh.reader as pread
import pidbuzh.utils as putils

from fabric.api import local, settings
from ipdb import set_trace as ST


class TestLoader(object):
    @classmethod
    def setupClass(klass):
        p = klass.package_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(p))
            local("mkdir {}".format(p))
        with putils.working_dir(p):
            local("mkdir utils")
            local("""echo 'a' > a.j2""")
            local("""echo 'b' > utils/b.j2""")

    def test_loader_returns_file_content(self):
        loader = pread.Loader(self.package_dir)
        assert loader('a.j2').strip() == "a"


class TestReader(object):
    """ """
    @classmethod
    def setupClass(klass):
        p = klass.package_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(p))
            local("mkdir {}".format(p))
        with putils.working_dir(p):
            local("""echo '{% include "c.j2" %}' > a.j2""")
            local("""echo '{% include "d.j2" %}' > b.j2""")
            local("""echo '{% include "b.j2" %}' > c.j2""")
            local("""echo '{% include "d.j2" %}' >> c.j2""")
            local("""echo '' >> d.j2""")

    def test__reader(self):
        reader = pread.Reader(pread.Loader(self.package_dir))
        res = reader._read("c.j2")
        assert res == {'b.j2', 'd.j2'}

    def test_graph(self):
        reader = pread.Reader(pread.Loader(self.package_dir))
        gr = reader.graph()
        assert gr == {
            'a.j2': set(['c.j2']),
            'b.j2': set(['d.j2']),
            'c.j2': set(['b.j2', 'd.j2']),
            'd.j2': set([])
        }
