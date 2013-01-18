# -*- coding: utf-8 -*-

import pidbuzh.run as prun
import fabric.api as fapi
import pidbuzh.utils as putils
import os
import shutil


class BaseTest(object):
    def setUp(self):
        src = self.source_dir = '/tmp/pidbuzh/from'
        tar = self.target_dir = '/tmp/pidbuzh/to'
        with fapi.settings(warn_only=True):
            fapi.local("rm -rf {}".format(src))
            fapi.local("rm -rf {}".format(tar))
        os.makedirs(src)
        os.makedirs(tar)


class BaseTest2(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        with putils.working_dir(self.source_dir):
            fapi.local("""echo 'a|{% include "c.j2" %}' > a.j2""")
            fapi.local("""echo 'b|{% include "d.j2" %}' > b.j2""")
            fapi.local("""echo 'c|{% include "b.j2" %}' > c.j2""")
            fapi.local("""echo '{% include "d.j2" %}' >> c.j2""")
            fapi.local("""echo 'd|{% include "_i.j2" %}' > d.j2""")
            fapi.local("""echo '_i' > _i.j2""")


class TestInitialGeneration(BaseTest2):
    def test_target_dir_created_if_it_doesnt_exist(self):
        shutil.rmtree(self.target_dir)
        runner = prun.Runner(
                rootpath='/tmp/pidbuzh',
                source_dir=self.source_dir,
                target_dir=self.target_dir
            )
        runner.start()
        assert os.path.isdir(self.target_dir)

    def test_target_content_generated(self):
        pass
