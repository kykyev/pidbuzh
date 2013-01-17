# -*- coding: utf-8 -*-

import pidbuzh.reactor as preact
import pidbuzh.utils as putils
from fabric.api import local, settings


class TestNodeIdFromEvent(object):
    """ """
    @classmethod
    def setUp(self):
        src = self.source_dir = '/tmp/pidbuzh/source'
        self.target_dir = '/tmp/pidbuzh/target'
        with settings(warn_only=True):
            local("rm -rf {}".format(src))
            local("mkdir {}".format(src))
        with putils.working_dir(src):
            local("""echo '{% include "c.j2" %}|a' > a.j2""")
            local("""echo '{% include "d.j2" %}|b' > b.j2""")
            local("""echo '{% include "b.j2" %}|c' > c.j2""")
            local("""echo '{% include "d.j2" %}|c' >> c.j2""")
            local("""echo 'd' >> d.j2""")

    def test_(self):
        pass
