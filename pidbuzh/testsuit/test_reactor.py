# -*- coding: utf-8 -*-

import pidbuzh.reactor as preact
import pidbuzh.utils as putils
import fabric.api as fapi
import os
import mock


class BaseTest(object):
    def setUp(self):
        src = self.source_dir = '/tmp/pidbuzh/from'
        tar = self.target_dir = '/tmp/pidbuzh/to'
        with fapi.settings(warn_only=True):
            fapi.local("rm -rf {}".format(src))
            fapi.local("rm -rf {}".format(tar))
        os.makedirs(src)
        os.makedirs(tar)
        self.log = mock.Mock()


class BaseTest2(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        ft = putils.FileTree(self.source_dir)
        ft.create({
            'a.j2': """{% include "c.j2" %}|a""",
            'b.j2': """{% include "d.j2" %}|b""",
            'c.j2': """{% include "b.j2" %}|c"""+'\n'+"""{% include "d.j2" %}|c""",
            'd.j2': 'd',
            '_ignore_me.j2': '_'
        })


class TestEventHandlerNodeIdFromEvent(BaseTest):
    """ """
    def test_1(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir,
            logger=self.log
        )
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/lib/a.j2'
        node_id = eh._node_id_from_event(evt)
        assert node_id == 'lib/a.j2'

    def test_2(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir,
            logger=self.log
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
            target_dir=self.target_dir,
            logger=self.log
        )
        eh._rebuild_all()
        with putils.working_dir(self.target_dir):
            assert open('a.j2').read() == "d|b|c\nd|c|a"
            assert open('b.j2').read() == "d|b"
            assert open('c.j2').read() == "d|b|c\nd|c"
            assert open('d.j2').read() == "d"


class TestEventHandler_IsChangeDeps(BaseTest2):
    """ """
    def test_no_change(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir,
            logger=self.log
        )
        eh.rebuild_graph()
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/b.j2'
        assert not eh._is_change_deps(evt)

    def test_change(self):
        eh = preact.EventHandler(
            rootpath='/tmp/pidbuzh',
            source_dir=self.source_dir,
            target_dir=self.target_dir,
            logger=self.log
        )
        eh.rebuild_graph()
        # make change
        with putils.working_dir(self.source_dir):
            fapi.local("""echo '{% include "_ignore_me.j2" %}' > b.j2""")
        evt = lambda: None
        evt.pathname = '/tmp/pidbuzh/from/b.j2'
        assert eh._is_change_deps(evt)
