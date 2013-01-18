# -*- coding: utf-8 -*-
"""
"""

from __future__ import print_function

import pyinotify as pyi
import pidbuzh.reactor as preactor
import pidbuzh.utils as putils
import operator
import os


EVENTS = reduce(
    operator.or_,
    [pyi.IN_MODIFY, pyi.IN_CREATE, pyi.IN_DELETE, pyi.IN_MOVED_FROM, pyi.IN_MOVED_TO]
  )

pjoin = os.path.join


class Runner(object):
    """ """
    def __init__(self, rootpath, source_dir='source', target_dir='target'):
        self.rootpath = rootpath
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.evh = preactor.EventHandler(rootpath=rootpath, source_dir=source_dir, target_dir=target_dir)
        self.wm = pyi.WatchManager()
        self.wm.add_watch(pjoin(rootpath, source_dir), EVENTS, rec=True, auto_add=True)
        self.notifier = pyi.Notifier(self.wm, default_proc_fun=self.evh)

    def start(self):
        with putils.working_dir(self.rootpath):
            putils.makedir(self.target_dir)
        self.evh._rebuild_all()
        print('==> Start monitoring %s (type c^c to exit)' % pjoin(self.rootpath, self.source_dir))
        print('==> Writing to %s' % pjoin(self.rootpath, self.target_dir))
        self.notifier.loop()
