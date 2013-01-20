# -*- coding: utf-8 -*-

import pidbuzh.writer as pwrite
import pidbuzh.utils as putils
import os
import mock

from fabric.api import local, settings


class BaseTest(object):
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
            local("""echo '_' >> _ignore_me.j2""")

    def setUp(self):
        with settings(warn_only=True):
            local("rm -rf {}".format(self.target_dir))
            local("mkdir {}".format(self.target_dir))
        self.log = mock.Mock()


class TestWriter(BaseTest):
    """ """
    def test__gen_single(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('c.j2')
        assert open(os.path.join(self.target_dir, 'c.j2')).read() == "d|b|c\nd|c"

    def test__gen_list(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_list(['a.j2', 'b.j2'])
        assert open(os.path.join(self.target_dir, 'a.j2')).read() == "d|b|c\nd|c|a"
        assert open(os.path.join(self.target_dir, 'b.j2')).read() == "d|b"

    def test__gen_all(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_all()
        assert open(os.path.join(self.target_dir, 'a.j2')).read() == "d|b|c\nd|c|a"
        assert open(os.path.join(self.target_dir, 'b.j2')).read() == "d|b"
        assert open(os.path.join(self.target_dir, 'c.j2')).read() == "d|b|c\nd|c"
        assert open(os.path.join(self.target_dir, 'd.j2')).read() == "d"

    def test_logmsg(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('c.j2')
        self.log.assert_called_once_with("Regen file {}".format(os.path.join(self.target_dir, 'c.j2')))


class TestIgnorePrefix(BaseTest):
    def test_gen_single(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('_ignore_me.j2')
        with putils.working_dir(self.target_dir):
            with settings(warn_only=True):
                cmdout = local("ls _ignore_me.j2", capture=True)
                assert not cmdout

    def test_gen_all(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_all()
        with putils.working_dir(self.target_dir):
            with settings(warn_only=True):
                cmdout = local("ls _*", capture=True)
                assert not cmdout
