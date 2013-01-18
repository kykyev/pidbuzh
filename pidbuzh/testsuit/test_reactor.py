# -*- coding: utf-8 -*-

import pidbuzh.reactor as preact
import pidbuzh.utils as putils
import fabric.api as fapi
import os


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
            fapi.local("""echo '{% include "c.j2" %}|a' > a.j2""")
            fapi.local("""echo '{% include "d.j2" %}|b' > b.j2""")
            fapi.local("""echo '{% include "b.j2" %}|c' > c.j2""")
            fapi.local("""echo '{% include "d.j2" %}|c' >> c.j2""")
            fapi.local("""echo 'd' >> d.j2""")
            fapi.local("""echo '_' >> _ignore_me.j2""")


class TestEventHandlerNodeIdFromEvent(BaseTest):
    """ """
    def test_1(self):
        eh = preact.EventHandler(
                rootpath='/tmp/pidbuzh',
                source_dir=self.source_dir,
                target_dir=self.target_dir
            )
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/lib/a.j2'
        node_id = eh._node_id_from_event(evt)
        assert node_id == 'lib/a.j2'

    def test_2(self):
        eh = preact.EventHandler(
                rootpath='/tmp/pidbuzh',
                source_dir=self.source_dir,
                target_dir=self.target_dir
            )
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/b.j2'
        node_id = eh._node_id_from_event(evt)
        assert node_id == 'b.j2'


class TestEventHandler_RebuildAll(BaseTest2):
    """ """
    def test_1(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir
        )
        eh._rebuild_all()
        assert open(os.path.join(self.target_dir, 'a.j2')).read() == "d|b|c\nd|c|a"
        assert open(os.path.join(self.target_dir, 'b.j2')).read() == "d|b"
        assert open(os.path.join(self.target_dir, 'c.j2')).read() == "d|b|c\nd|c"
        assert open(os.path.join(self.target_dir, 'd.j2')).read() == "d"


class TestEventHandler_IsChangeDeps(BaseTest2):
    """ """
    def test_no_change(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir
        )
        eh.rebuild_graph()
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/b.j2'
        assert not eh._is_change_deps(evt)

    def test_change(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir
        )
        eh.rebuild_graph()
        # make change
        with putils.working_dir(self.source_dir):
            fapi.local("""echo '{% include "_ignore_me.j2" %}' > b.j2""")
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/b.j2'
        assert eh._is_change_deps(evt)
