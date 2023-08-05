# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
import os
from argparse import ArgumentParser
from smoothtest.autotest.base import AutoTestBase
from smoothtest.autotest.Main import Main
from smoothtest.autotest.TestSearcher import TestSearcher
import sys


def is_valid_file(parser, path):
    '''
    Validate if a passed argument is a existing file (used by argsparse)
    '''
    abspath = os.path.abspath(path)
    if os.path.exists(abspath) and os.path.isfile(abspath):
        return path  # return the file path
    else:
        parser.error("The file %s does not exist!" % path)


def is_file_or_dir(parser, path):
    '''
    Validate if a passed argument is a existing file (used by argsparse)
    '''
    abspath = os.path.abspath(path)
    if os.path.exists(abspath) and (os.path.isfile(abspath) or os.path.isdir(abspath)):
        return path  # return the file path
    else:
        parser.error("The file %s does not exist!" % path)


class Command(AutoTestBase):
    def get_parser(self, file_checking=True):
        if file_checking:
            is_file = lambda x: is_valid_file(parser, x)
            is_dir_file = lambda x: is_file_or_dir(parser, x)
        else:
            is_file = lambda x: x
            is_dir_file = lambda x: x
        parser = ArgumentParser(description='Start a local sales vs'
                                'non-sales glidepath server')
        parser.add_argument('tests', type=is_file,
                            help='Tests to be monitored and run. Triggers'
                            ' partial_reloads',default=[], nargs='*')
        parser.add_argument('-r', '--methods-regex', type=str,
                            help='Specify regex for Methods matching',
                            default='')
        parser.add_argument('-n', '--no-ipython',
                            help='Do not use ipython interactive shell',
                            default=False, action='store_true')
        parser.add_argument('--smoke', help='Do not run tests. Simply test'
                            ' the whole monitoring system',default=None, 
                            action='store_true')
        parser.add_argument('-F', '--full-reloads', type=is_dir_file,
                            help='Files or directories to be monitored and'
                            ' triggers of full_reloads.', default=[], nargs='+')
        parser.add_argument('-R', '--full-regex', type=str, help='Regex to'
                            ' filter files in full reloads directories.',
                            default='.*')
        return parser

    def get_extension_parser(self):
        parser = self.get_parser(file_checking=False)
        parser.add_argument('-f', '--force',
                            help='force reloading tests (+ restarting webdriver)',
                            default=False, action='store_true')
        parser.add_argument('-u', '--update',
                            help='update test config',
                            default=False, action='store_true')
        parser.add_argument('--nosmoke',
                            help='force no-smoke for updating',
                            default=None, action='store_true')
        return parser

    def get_test_config(self, args, argv):
        searcher = TestSearcher()
        test_paths = set()
        partial_reloads = set()
        for tst in args.tests:
            tst = self._path_to_modstr(tst)
            paths, partial = searcher.solve_paths((tst, args.methods_regex))
            if paths:
                test_paths.update(paths)
                partial_reloads.update(partial)

        test_config = dict(test_paths=test_paths,
                           partial_reloads=partial_reloads,
                           full_reloads=args.full_reloads,
                           full_filter=args.full_regex,
                           smoke=args.smoke,
                           argv=argv,
                           )
        return test_config

    def main(self, argv=None):
        curdir = os.path.abspath(os.curdir)
        filedir = os.path.abspath(os.path.dirname(__file__))
        
        #Remove the dir of this file if we are not in this directory
        if curdir != filedir and filedir in sys.path:
            sys.path.remove(filedir)
        
        args, unkonwn = self.get_parser().parse_known_args(argv)

        main = Main(smoke=args.smoke)
        test_config = self.get_test_config(args, unkonwn)
        main.run(embed_ipython=not args.no_ipython, test_config=test_config)


def smoke_test_module():
    c = Command()
    c.get_parser()
    parser = c.get_extension_parser()
    args, unkown = parser.parse_known_args([])
    c.get_test_config(args, unkown)


def main(argv=None):
    Command().main(argv)

if __name__ == "__main__":
    main()
