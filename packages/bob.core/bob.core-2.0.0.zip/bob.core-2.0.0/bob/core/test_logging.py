#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Tue 09 Jul 2013 13:24:49 CEST

"""Tests for the logging subsystem
"""

from . import _logging

def test_from_cxx():

  _logging.__log_message__(1, 'error', 'this is a test message')

def test_from_cxx_multithreaded():

  _logging.__log_message_mt__(2, 1, 'error', 'this is a test message')
