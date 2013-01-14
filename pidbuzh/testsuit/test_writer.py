# -*- coding: utf-8 -*-

import pidbuzh.writer as pwrite
import pidbuzh.utils as putils
import os

from fabric.api import local, settings
from ipdb import set_trace as ST


class TestWriter(object):
    """ """
    @classmethod
    def setupClass(klass):
        src = klass.source_dir = '/tmp/source-pidbuzh'
        klass.target_dir = '/tmp/target-pidbuzh'

        with settings(warn_only=True):
            local("rm -rf {}".format(src))
            local("mkdir {}".format(src))
        with putils.working_dir(src):
            local("""echo '{% include "c.j2" %}|a' > a.j2""")
            local("""echo '{% include "d.j2" %}|b' > b.j2""")
            local("""echo '{% include "b.j2" %}|c' > c.j2""")
            local("""echo '{% include "d.j2" %}|c' >> c.j2""")
            local("""echo 'd' >> d.j2""")

    def setUp(self):
        with settings(warn_only=True):
            local("rm -rf {}".format(self.target_dir))
            local("mkdir {}".format(self.target_dir))

    def test__gen_single(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir)
        wr._gen_single('c.j2')
        assert open(os.path.join(self.target_dir, 'c.j2')).read() == "d|b|c\nd|c"

    def test__gen_list(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir)
        wr._gen_list(['a.j2', 'b.j2'])
        assert open(os.path.join(self.target_dir, 'a.j2')).read() == "d|b|c\nd|c|a"
        assert open(os.path.join(self.target_dir, 'b.j2')).read() == "d|b"

    def test__gen_all(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir)
        wr._gen_all()
        assert open(os.path.join(self.target_dir, 'a.j2')).read() == "d|b|c\nd|c|a"
        assert open(os.path.join(self.target_dir, 'b.j2')).read() == "d|b"
        assert open(os.path.join(self.target_dir, 'c.j2')).read() == "d|b|c\nd|c"
        assert open(os.path.join(self.target_dir, 'd.j2')).read() == "d"
