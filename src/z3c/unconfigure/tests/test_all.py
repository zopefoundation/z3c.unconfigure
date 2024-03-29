##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests
"""
import unittest

from z3c.unconfigure.testing import DocFileSuite


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(DocFileSuite('../README.txt'))
    suite.addTest(DocFileSuite('overrides.txt'))
    suite.addTest(DocFileSuite('subscribers.txt'))
    return suite
