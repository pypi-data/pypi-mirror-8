# -*- encoding: utf-8 -*-
#
# Copyright 2012 Martin Zimmermann <info@posativ.org>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Martin Zimmermann <info@posativ.org>.

import pkg_resources
dist = pkg_resources.get_distribution("acrylamid")

__author__ = 'Martin Zimmermann <info@posativ.org>'
__url__ = 'https://github.com/posativ/acrylamid/'

import sys, os
PY3 = sys.version_info[0] == 3

if sys.version_info > (3, 2) and 'test' not in sys.argv and not os.getenv('PYTHONHASHSEED'):
    os.putenv('PYTHONHASHSEED', '0')
    os.execvp(sys.argv[0], sys.argv)  # XXX very slow, move to she-bang if
                                      #     if fully python3 compatible.

import time
import argparse
import traceback
import signal

from os.path import dirname
from functools import partial

from acrylamid import log, commands, colors, tasks, core
from acrylamid.utils import Struct
from acrylamid.errors import AcrylamidException

signal.signal(signal.SIGINT, signal.SIG_DFL)
sys.path.append(dirname(__file__))


class AcrylFormatter(argparse.HelpFormatter):
    """Remove {a,b,c,d,e,...} subcommand listing from help."""

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            result = ''
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size

        return format


def Acryl():
    """The main function that dispatches the CLI.  We use :class:`AcrylFormatter`
    as custom help formatter that ommits the useless list of available subcommands
    and their aliases.

    All flags from acrylamid --help are also available in subcommands altough not
    explicitely printed in their help."""

    parser = argparse.ArgumentParser(
        parents=[], formatter_class=AcrylFormatter
    )
    parser.add_argument("-v", "--verbose", action="store_const", dest="verbosity",
        help="more verbose", const=log.SKIP, default=log.INFO)
    parser.add_argument("-q", "--quiet", action="store_const", dest="verbosity",
        help="less verbose", const=log.WARN)
    parser.add_argument("-C", "--no-color", action="store_false", dest="colors",
        help="disable color", default=True)
    parser.add_argument("--conf", dest="conf", help="alternate conf.py",
        default="conf.py", metavar="/path/to/conf")
    parser.add_argument("--version", action="version",
        version=colors.blue('Acrylamid ') + dist.version)

    subparsers = parser.add_subparsers(dest="parser")

    # a repeat yourself of default arguments but not visible on subcommand --help
    default = argparse.ArgumentParser(add_help=False)
    default.add_argument("-v", "--verbose", action="store_const", dest="verbosity",
        help=argparse.SUPPRESS, const=log.SKIP, default=log.INFO)
    default.add_argument("-q", "--quiet", action="store_const", dest="verbosity",
        help=argparse.SUPPRESS, const=log.WARN)
    default.add_argument("-C", "--no-color", action="store_false", dest="colors",
        help=argparse.SUPPRESS, default=True)

    # --- gen params --- #
    generate = subparsers.add_parser('compile', help='compile blog', parents=[default])
    generate.add_argument("-f", "--force", action="store_true", dest="force",
        help="clear cache before compilation", default=False)
    generate.add_argument("-n", "--dry-run", dest="dryrun", action='store_true',
        help="show what would have been compiled", default=False)
    generate.add_argument("--ignore", dest="ignore", action="store_true",
        help="ignore critical errors", default=False)
    generate.add_argument("--search", dest="search", action="store_true",
        help="build search index", default=False)

    # --- webserver params --- #
    view = subparsers.add_parser('view', help="fire up built-in webserver", parents=[default])
    view.add_argument("-p", "--port", dest="port", type=int, default=8000,
        help="webserver port")

    # --- aco params --- #
    autocompile = subparsers.add_parser('autocompile', help="automatic compilation and serving",
        parents=[default])
    autocompile.add_argument("-f", "--force", action="store_true", dest="force",
        help="clear cache before compilation", default=False)
    autocompile.add_argument("-n", "--dry-run", dest="dryrun", action='store_true',
        help="show what would have been compiled", default=False)
    autocompile.add_argument("--ignore", dest="ignore", action="store_true",
        help="ignore critical errors", default=False)
    autocompile.add_argument("--search", dest="search", action="store_true",
        help="build search index", default=False)
    autocompile.add_argument("-p", "--port", dest="port", type=int, default=8000,
        help="webserver port")

    for alias in ('co', 'gen', 'generate'):
        subparsers._name_parser_map[alias] = generate

    for alias in ('serve', 'srv'):
        subparsers._name_parser_map[alias] = view

    subparsers._name_parser_map['aco'] = autocompile

    # temporary log to catch issues during task initialization
    log.init('temporary', level=log.WARN, colors=False)

    # initialize other tasks
    tasks.initialize(subparsers, default)

    # parse args
    options = parser.parse_args()

    # initialize colored logger
    log.init('acrylamid', level=options.verbosity, colors=options.colors)

    env = core.Environment({'author': __author__, 'url': __url__,
        'options': options, 'globals': Struct()})

    # -- init -- #
    try:
        if options.parser in ('init', ):
            tasks.collected[options.parser](env, options)
            sys.exit(0)
    except AcrylamidException as e:
        log.fatal(e.args[0])
        sys.exit(1)

    try:
        conf = core.load(options.conf)
    except IOError:
        log.critical('no conf.py found. Try "acrylamid init".')
        sys.exit(1)
    except Exception as e:
        log.critical("%s in `conf.py`" % e.__class__.__name__)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


    # -- run -- #
    if options.parser in ('gen', 'generate', 'co', 'compile'):
        log.setLevel(options.verbosity)
        try:
            commands.compile(conf, env)
        except AcrylamidException as e:
            log.exception(e.args[0])
            sys.exit(1)

    elif options.parser in ('srv', 'serve', 'view'):
        from acrylamid.lib.httpd import Webserver
        ws = partial(Webserver, options.port, conf['output_dir'])
        ws = ws(log.info) if options.verbosity < 20 else ws(); ws.start()
        log.info(' * Running on http://127.0.0.1:%i/' % options.port)

        try:
            while True:
                time.sleep(1)
        except (SystemExit, KeyboardInterrupt) as e:
            ws.kill_received = True
            sys.exit(0)

    elif options.parser in ('aco', 'autocompile'):
        from acrylamid.lib.httpd import Webserver
        # XXX compile on request _or_ use inotify/fsevent
        ws = Webserver(options.port, conf['output_dir']); ws.start()
        log.info(' * Running on http://127.0.0.1:%i/' % options.port)

        try:
            commands.autocompile(ws, conf, env)
        except (SystemExit, KeyboardInterrupt) as e:
            ws.kill_received = True
            log.error(e.args[0])
            traceback.print_exc(file=sys.stdout)
            sys.exit(0)

    elif options.parser in tasks.collected:
        try:
            tasks.collected[options.parser](conf, env, options)
        except AcrylamidException as e:
            log.critical(e.args[0])
            sys.exit(1)
    else:
        log.critical('No such command!')
        sys.exit(2)

    sys.exit(0)
