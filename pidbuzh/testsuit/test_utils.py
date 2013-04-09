# -*- coding: utf-8 -*-

from fabric.api import local, settings

import pidbuzh.utils as putils
import os
import codecs


class TestClearDir(object):
    """ """
    def setUp(self):
        test_dir = self.test_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(test_dir))
            local("mkdir {}".format(test_dir))
        ft = putils.FileTree(test_dir)
        ft.create({
            'a.js': None,
            'z.js': None,
            'lib/b.js': None,
            'utils/': None
        })

    def test_all_is_deleted(self):
        putils.clear_dir(self.test_dir)
        cmdout = local("ls {}".format(self.test_dir), capture=True)
        assert not cmdout


class TestMakedir(object):
    def setUp(self):
        self.test_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(self.test_dir))

    def test_not_exists(self):
        putils.makedir(self.test_dir)
        assert os.path.exists(self.test_dir)

    def test_exists(self):
        local("mkdir {}".format(self.test_dir))
        putils.makedir(self.test_dir)
        assert os.path.exists(self.test_dir)

    def test_relative_path(self):
        with putils.working_dir('/tmp'):
            putils.makedir('test-pidbuzh')
        assert os.path.exists(self.test_dir)


class TestWrite2File(object):
    def setUp(self):
        self.test_dir = '/tmp/test-pidbuzh'
        with settings(warn_only=True):
            local("rm -rf {}".format(self.test_dir))
            local("mkdir {}".format(self.test_dir))
        with putils.working_dir(self.test_dir):
            local("""touch a.html""")

    def test_unicode(self):
        with putils.working_dir(self.test_dir):
            putils.write2file('a.html', u"привет")
            with codecs.open('a.html', 'r') as fin:
                assert fin.read() == "привет"

    def test_rewrite(self):
        with putils.working_dir(self.test_dir):
            putils.write2file('a.html', "A!")
            putils.write2file('a.html', "B!")
            with codecs.open('a.html', 'r') as fin:
                assert fin.read() == "B!"


class TestFileTree(object):
    def setUp(self):
        self.test_dir = '/tmp/test-pidbuzh'
        self.fmap = {
            'foo/bar/x.js': "x",
            'foo/bar/y.js': "y",
            'foo/lol/z.js': "z",
            'foo/w.js': None,
            'css/a.css': 'a.css',
            'css/lib/norm.css': 'norm.css',
            'css/dir/': None
        }

    def test_empty_dir_created(self):
        ft = putils.FileTree(self.test_dir)
        ft.create(self.fmap)
        with putils.working_dir(self.test_dir):
            assert os.path.isdir('css/dir/')

    def test_file_created_and_pupulated(self):
        ft = putils.FileTree(self.test_dir)
        ft.create(self.fmap)
        with putils.working_dir(self.test_dir):
            with codecs.open('foo/bar/x.js', 'r') as fin:
                assert fin.read() == "x"

    def test_empty_file(self):
        ft = putils.FileTree(self.test_dir)
        ft.create(self.fmap)
        with putils.working_dir(self.test_dir):
            with codecs.open('foo/w.js', 'r') as fin:
                assert fin.read() == ""
