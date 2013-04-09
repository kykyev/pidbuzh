# -*- coding: utf-8 -*-

import pidbuzh.writer as pwrite
import pidbuzh.utils as putils
import os
import mock

from fabric.api import local, settings


class BaseTest(object):
    @classmethod
    def setupClass(klass):
        src = klass.source_dir = '/tmp/source-pidbuzh'
        klass.target_dir = '/tmp/target-pidbuzh'

        with settings(warn_only=True):
            local("rm -rf {}".format(src))
            local("mkdir {}".format(src))
        ft = putils.FileTree(src)
        ft.create({
            'a.j2': """{% include "c.j2" %}|a""",
            'b.j2': """{% include "d.j2" %}|b""",
            'c.j2': """{% include "b.j2" %}|c"""+'\n'+"""{% include "d.j2" %}|c""",
            'd.j2': 'd',
            '_ignore_me.j2': '_'
        })

    def setUp(self):
        with settings(warn_only=True):
            local("rm -rf {}".format(self.target_dir))
            local("mkdir {}".format(self.target_dir))
        self.log = mock.Mock()


class TestWriter(BaseTest):
    """ """
    def test__gen_single(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('c.j2')
        with putils.working_dir(self.target_dir):
            assert open('c.j2').read() == "d|b|c\nd|c"

    def test__gen_list(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_list(['a.j2', 'b.j2'])
        with putils.working_dir(self.target_dir):
            assert open('a.j2').read() == "d|b|c\nd|c|a"
            assert open('b.j2').read() == "d|b"

    def test__gen_all(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_all()
        with putils.working_dir(self.target_dir):
            assert open('a.j2').read() == "d|b|c\nd|c|a"
            assert open('b.j2').read() == "d|b"
            assert open('c.j2').read() == "d|b|c\nd|c"
            assert open('d.j2').read() == "d"

    def test_logmsg(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('c.j2')
        self.log.assert_called_once_with("Regen file {}".format(os.path.join(self.target_dir, 'c.j2')))


class TestIgnorePrefix(BaseTest):
    def test_gen_single(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('_ignore_me.j2')
        with putils.working_dir(self.target_dir):
            with settings(warn_only=True):
                cmdout = local("ls _ignore_me.j2", capture=True)
                assert not cmdout

    def test_gen_all(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_all()
        with putils.working_dir(self.target_dir):
            with settings(warn_only=True):
                cmdout = local("ls _*", capture=True)
                assert not cmdout


class TestWriteIntoSubdirectory(BaseTest):
    """
        Consider following folder structure:

        source/
            subdir/generate-me.html
        target/

        Writer should create directory target/subdir and then write into it.
    """
    @classmethod
    def setupClass(klass):
        BaseTest.setupClass()
        with putils.working_dir(klass.source_dir):
            local("""mkdir subdir""")
            local("""echo '!' > subdir/generate-me.html""")

    def test__gen_single(self):
        wr = pwrite.Writer(source=self.source_dir, target=self.target_dir, logger=self.log)
        wr._gen_single('subdir/generate-me.html')
        assert open(os.path.join(self.target_dir,
                    'subdir/generate-me.html')).read() == "!"
