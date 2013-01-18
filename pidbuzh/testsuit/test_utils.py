# -*- coding: utf-8 -*-

from fabric.api import local, settings

import pidbuzh.utils as putils
import os


class TestClearDir(object):
    """ """
    def setUp(self):
        test_dir = self.test_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(test_dir))
            local("mkdir {}".format(test_dir))
        with putils.working_dir(test_dir):
            local("""touch a.js""")
            local("""touch z.js""")
            local("""mkdir lib""")
            local("""touch lib/b.js""")
            local("""mkdir utils""")

    def test_all_is_deleted(self):
        putils.clear_dir(self.test_dir)
        cmdout = local("ls {}".format(self.test_dir), capture=True)
        assert not cmdout


class TestMakedir(object):
    def setUp(self):
        self.test_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(self.test_dir))

    def test_not_exists(self):
        putils.makedir(self.test_dir)
        assert os.path.exists(self.test_dir)

    def test_exists(self):
        local("mkdir {}".format(self.test_dir))
        putils.makedir(self.test_dir)
        assert os.path.exists(self.test_dir)

    def test_relative_path(self):
        with putils.working_dir('/tmp'):
            putils.makedir('test-pidbuzh')
        assert os.path.exists(self.test_dir)
