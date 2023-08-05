#!/usr/bin/python
from __future__ import unicode_literals, division, absolute_import

__version__ = '1.2.194'

import logging
import os

from flexget import logger, plugin
from flexget.manager import Manager
from flexget.options import get_parser

log = logging.getLogger('main')


def main(args=None):
    """Main entry point for Command Line Interface"""

    logger.initialize()

    plugin.load_plugins()

    options = get_parser().parse_args(args)

    manager = Manager(options)

    if options.profile:
        try:
            import cProfile as profile
        except ImportError:
            import profile
        profile.runctx('manager.start()', globals(), locals(),
                       os.path.join(manager.config_base, options.profile))
    else:
        manager.start()
