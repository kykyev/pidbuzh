# -*- coding: utf-8 -*-
"""
"""

from __future__ import print_function

import pyinotify as pyi
import pidbuzh.reactor as preactor
import pidbuzh.writer as pwrite
import os


def run(rootpath, source_dir='source', target_dir='target'):
    """ """
    events = (pyi.IN_MODIFY |
              pyi.IN_CREATE |
              pyi.IN_DELETE |
              pyi.IN_MOVED_FROM |
              pyi.IN_MOVED_TO)

    writer = pwrite.Writer(target_dir)
    writer.generate()

    wm = pyi.WatchManager()
    evh = preactor.EventHandler(rootpath=rootpath, source_dir=source_dir, target_dir=target_dir)
    notifier = pyi.Notifier(wm, default_proc_fun=evh)
    wm.add_watch(os.path.join(rootpath, source_dir), events, rec=True, auto_add=True)
    print('==> Start monitoring %s (type c^c to exit)' % os.path.join(rootpath, source_dir))
    notifier.loop()


if __name__ == '__main__':
    run('/tmp')
