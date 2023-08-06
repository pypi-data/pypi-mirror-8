# Copyright (C) 2014 New York University
# This file is part of ReproZip which is released under the Revised BSD License
# See file LICENSE for full license details.

"""Entry point for the reprounzip utility.

This contains :func:`~reprounzip.reprounzip.main`, which is the entry point
declared to setuptools. It is also callable directly.

It dispatchs to plugins registered through pkg_resources as entry point
``reprounzip.unpackers``.
"""

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import codecs
import locale
from pkg_resources import iter_entry_points
import sys
import traceback

from reprounzip.common import setup_logging
from reprounzip import signals


__version__ = '0.5'


unpackers = {}


def get_plugins(entry_point_name):
    for entry_point in iter_entry_points(entry_point_name):
        try:
            func = entry_point.load()
        except Exception:
            print("Plugin %s from %s %s failed to initialize!" % (
                  entry_point.name,
                  entry_point.dist.project_name, entry_point.dist.version),
                  file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            continue
        name = entry_point.name
        # Docstring is used as description (used for detailed help)
        descr = func.__doc__.strip()
        # First line of docstring is the help (used for general help)
        descr_1 = descr.split('\n', 1)[0]

        yield name, func, descr, descr_1


def main():
    """Entry point when called on the command-line.
    """
    # Locale
    locale.setlocale(locale.LC_ALL, '')

    # Encoding for output streams
    if str == bytes:  # PY2
        writer = codecs.getwriter(locale.getpreferredencoding())
        o_stdout, o_stderr = sys.stdout, sys.stderr
        sys.stdout = writer(sys.stdout)
        sys.stdout.buffer = o_stdout
        sys.stderr = writer(sys.stderr)
        sys.stderr.buffer = o_stderr
    else:
        sys.stdin = sys.stdin.buffer

    # http://bugs.python.org/issue13676
    # This prevents reprozip from reading argv and envp arrays from trace
    if sys.version_info < (2, 7, 3):
        sys.stderr.write("Error: your version of Python, %s, is not "
                         "supported\nVersions before 2.7.3 are affected by "
                         "bug 13676 and will not work with ReproZip\n" %
                         sys.version.split(' ', 1)[0])
        sys.exit(1)

    # Parses command-line

    # General options
    options = argparse.ArgumentParser(add_help=False)
    options.add_argument('--version', action='version',
                         version="reprounzip version %s" % __version__)
    options.add_argument('-v', '--verbose', action='count', default=1,
                         dest='verbosity',
                         help="augments verbosity level")

    # Loads plugins
    for name, func, descr, descr_1 in get_plugins('reprounzip.plugins'):
        func()

    parser = argparse.ArgumentParser(
            description="reprounzip is the ReproZip component responsible for "
                        "unpacking and reproducing an experiment previously "
                        "packed with reprozip",
            epilog="Please report issues to reprozip-users@vgc.poly.edu",
            parents=[options])
    subparsers = parser.add_subparsers(title="subcommands", metavar='')

    # Loads unpackers
    for name, func, descr, descr_1 in get_plugins('reprounzip.unpackers'):
        plugin_parser = subparsers.add_parser(
                name, parents=[options],
                help=descr_1, description=descr,
                formatter_class=argparse.RawDescriptionHelpFormatter)
        info = func(plugin_parser)
        plugin_parser.set_defaults(selected_unpacker=name)
        if info is None:
            info = {}
        unpackers[name] = info

    signals.pre_parse_args(parser=parser, subparsers=subparsers)
    args = parser.parse_args()
    signals.post_parse_args(args=args)
    try:
        signals.unpacker = args.selected_unpacker
    except AttributeError:
        signals.unpacker = None
    setup_logging('REPROUNZIP', args.verbosity)
    try:
        args.func(args)
    except Exception as e:
        signals.application_finishing(reason=e)
        raise
    else:
        signals.application_finishing(reason=None)
    sys.exit(0)


if __name__ == '__main__':
    main()
