# -*- coding: utf-8 -*-

import sys
import os

THISDIR = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(THISDIR, '..'))
sys.path.insert(0, ROOT)

import pidbuzh.run as prun


runner = prun.Runner(
        rootpath=THISDIR,
        source_dir='source',
        target_dir='target'
    )
import ipdb; ipdb.set_trace()
runner.start()
