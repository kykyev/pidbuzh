# -*- coding: utf-8 -*-

import pidbuzh.utils as putils
from fabric.api import local, settings


class TestClearDir(object):
    """ """
    @classmethod
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
