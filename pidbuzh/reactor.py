# -*- coding: utf-8 -*-
"""
    touch foo.js => process_IN_CREATE:
        <Event dir=False mask=0x100 maskname=IN_CREATE name=foo.js
               path=/tmp/ololo pathname=/tmp/ololo/foo.js wd=1 >

    md lib => process_IN_CREATE:
        <Event dir=True mask=0x40000100 maskname=IN_CREATE|IN_ISDIR name=lib
               path=/tmp/ololo pathname=/tmp/ololo/lib wd=1 >

    rm foo.js => process_IN_DELETE:
        <Event dir=False mask=0x200 maskname=IN_DELETE name=foo.js
               path=/tmp/ololo pathname=/tmp/ololo/foo.js wd=1 >

    rmdir lib (empty dir) => process_IN_DELETE:
                <Event dir=True mask=0x40000200 maskname=IN_DELETE|IN_ISDIR name=lib
                       path=/tmp/ololo pathname=/tmp/ololo/lib wd=1 >

    rm -rf lib (dir with file bar.js) => process_IN_DELETE:
        <Event dir=False mask=0x200 maskname=IN_DELETE name=bar.js
               path=/tmp/ololo/lib pathname=/tmp/ololo/lib/bar.js wd=3 >
        <Event dir=True mask=0x40000200 maskname=IN_DELETE|IN_ISDIR name=lib
               path=/tmp/ololo pathname=/tmp/ololo/lib wd=1 >

    mv foo.js bar.js
        => process_IN_MOVED_FROM:
            <Event cookie=7567 dir=False mask=0x40 maskname=IN_MOVED_FROM name=foo.js
                   path=/tmp/ololo pathname=/tmp/ololo/foo.js wd=1 >
        => process_IN_MOVED_TO:
            <Event cookie=7567 dir=False mask=0x80 maskname=IN_MOVED_TO name=bar.js
                   path=/tmp/ololo pathname=/tmp/ololo/bar.js src_pathname=/tmp/ololo/foo.js wd=1 >

    cp bar.js lib/foo.js
        => process_IN_CREATE:
            <Event dir=False mask=0x100 maskname=IN_CREATE name=foo.js
                   path=/tmp/ololo/lib pathname=/tmp/ololo/lib/foo.js wd=4 >

    mv lib _lib
        => process_IN_MOVED_FROM:
            <Event cookie=9039 dir=True mask=0x40000040 maskname=IN_MOVED_FROM|IN_ISDIR name=lib
                   path=/tmp/ololo pathname=/tmp/ololo/lib wd=1 >
        => process_IN_MOVED_TO:
            <Event cookie=9039 dir=True mask=0x40000080 maskname=IN_MOVED_TO|IN_ISDIR name=_lib
                   path=/tmp/ololo pathname=/tmp/ololo/_lib src_pathname=/tmp/ololo/lib wd=1 >
"""

import pyinotify as pyi
import pidbuzh.graph as pgraph
import pidbuzh.reader as pread
import pidbuzh.writer as pwrite
import pidbuzh.utils as putils
from os.path import relpath


class EventHandler(pyi.ProcessEvent):
    """ File event handler.
    Reacts on file create, modify, delete and move.
    """
    def my_init(self, rootpath, source_dir, target_dir):
        self._myns = lambda: None
        self._myns.rootpath = rootpath
        self._myns.source_dir = source_dir
        self._myns.target_dir = target_dir
        self._myns.reader = pread.Reader(pread.Loader(source_dir))
        self._myns.writer = pwrite.Writer(source_dir, target_dir)

    def rebuild_graph(self):
        self._myns.graph = pgraph.DepGraph(self._myns.reader.graph())

    def process_IN_MODIFY(self, event):
        if self._is_change_deps(event):
            self._rebuild_all()
        else:
            me = self._node_id_from_event(event)
            depends_from_me = self._myns.graph.depends_from(me)
            depends_from_me.add(me)
            self._myns.writer.generate(list(depends_from_me))

    def process_IN_CREATE(self, event):
        """ """
        self._rebuild_all()

    def process_IN_DELETE(self, event):
        """ """
        self._rebuild_all()

    def process_IN_MOVED_FROM(self, event):
        """ """
        self._rebuild_all()

    def process_IN_MOVED_TO(self, event):
        self._rebuild_all()

    def _rebuild_all(self):
        putils.clear_dir(self._myns.target_dir)
        self.rebuild_graph()
        self._myns.writer.generate()

    def _node_id_from_event(self, event):
        return relpath(event.pathname, self._myns.source_dir)

    def _is_change_deps(self, event):
        node_id = self._node_id_from_event(event)
        deps = self._myns.reader._read(node_id)
        if deps == self._myns.graph._orig_dict_of_sets[node_id]:
            return False
        return True
