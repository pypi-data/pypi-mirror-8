#!/usr/bin/python

from __future__ import unicode_literals, division, absolute_import

import logging
import os

from flexget import logger, plugin
from flexget.manager import Manager
from flexget.options import get_parser

__version__ = '1.2.181'

log = logging.getLogger('main')


def main(args=None):
    """Main entry point for Command Line Interface"""

    logger.initialize()

    plugin.load_plugins()

    options = get_parser().parse_args(args)

    manager = Manager(options)

    log_level = logging.getLevelName(options.loglevel.upper())
    log_file = os.path.expanduser(manager.options.logfile)
    # If an absolute path is not specified, use the config directory.
    if not os.path.isabs(log_file):
        log_file = os.path.join(manager.config_base, log_file)
    logger.start(log_file, log_level)
    if options.profile:
        try:
            import cProfile as profile
        except ImportError:
            import profile
        profile.runctx('manager.start()', globals(), locals(),
                       os.path.join(manager.config_base, options.profile))
    else:
        manager.start()
