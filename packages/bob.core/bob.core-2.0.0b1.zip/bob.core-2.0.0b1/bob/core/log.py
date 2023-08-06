#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Sat 19 Oct 12:51:01 2013 

"""Sets-up logging, centrally for Bob.
"""

import sys
import logging
from ._logging import reset

# get the default logger of Bob
logger = logging.getLogger('bob')

# by default, warning and error messages should be written to sys.stderr
warn_err = logging.StreamHandler(sys.stderr)
warn_err.setLevel(logging.WARNING)
logger.addHandler(warn_err)
del warn_err

# debug and info messages are written to sys.stdout
class InfoFilter:
  def filter(self, record): return record.levelno <= logging.INFO
debug_info = logging.StreamHandler(sys.stdout)
debug_info.setLevel(logging.DEBUG)
debug_info.addFilter(InfoFilter())
logger.addHandler(debug_info)
del debug_info, InfoFilter, logger

# this will setup divergence from C++ into python.logging correctly
reset(logging.getLogger('bob.c++'))

# this will make sure we don't fiddle with python callables after
# termination. See: http://stackoverflow.com/questions/18184209/holding-python-produced-value-in-a-c-static-boostshared-ptr
import atexit
atexit.register(reset)
del atexit

__all__ = ['reset']
