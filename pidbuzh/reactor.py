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

from __future__ import print_function

import pyinotify as pyi
import pidbuzh.graph as pgraph

from ipdb import set_trace


class EventHandler(pyi.ProcessEvent):
    """ File event handler.
    Reacts on file create, modify, delete and move.
    """

    def process_IN_MODIFY(self, event):
        set_trace()

    def process_IN_CREATE(self, event):
        """ """
        set_trace()

    def process_IN_DELETE(self, event):
        """ """
        set_trace()

    def process_IN_MOVED_FROM(self, event):
        """ """
        set_trace()

    def process_IN_MOVED_TO(self, event):
        set_trace()


def run(path):
    """ """
    events = (pyi.IN_MODIFY
              | pyi.IN_CREATE
              | pyi.IN_DELETE
              | pyi.IN_MOVED_FROM
              | pyi.IN_MOVED_TO)

    wm = pyi.WatchManager()
    notifier = pyi.Notifier(wm, default_proc_fun=EventHandler())
    wm.add_watch(path, events, rec=True, auto_add=True)
    print('==> Start monitoring %s (type c^c to exit)' % path)
    notifier.loop()


if __name__ == '__main__':
    run('/tmp/ololo')
