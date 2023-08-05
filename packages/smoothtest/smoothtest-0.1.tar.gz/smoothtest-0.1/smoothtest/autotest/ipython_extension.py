# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''

from IPython.core.magic import Magics, magics_class, line_magic

import shlex
import subprocess
import glob


@magics_class
class AutotestMagics(Magics):
    main = None

    def expand_files(self, tests):
        paths = []
        for tst in tests:
            paths += glob.glob(tst)
        return paths

    @line_magic
    def autotest(self, line):
        '''
        
        :param line:
        '''
        from .Command import Command
        command = Command()
        parser = command.get_extension_parser()
        args = parser.parse_args(shlex.split(line))
        args.tests = self.expand_files(args.tests)
        args.full_reloads = self.expand_files(args.full_reloads)
        test_config = command.parcial(args)
        test_config.update(force=args.force)
        self.main.send_test(**test_config)
        return test_config


def load_extension(ipython, main):
    AutotestMagics.main = main
    ipython.register_magics(AutotestMagics)


def load_ipython_extension(ipython):
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(AutotestMagics)


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass


def smoke_test_module():
    am = AutotestMagics(None)
    from pprint import pprint
    pprint( am.expand_files(['./*.py']))


if __name__ == "__main__":
    smoke_test_module()
