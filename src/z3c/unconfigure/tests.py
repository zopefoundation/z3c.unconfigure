##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
import os
import unittest
import zope.testing.cleanup
from zope.testing import doctest
from zope.configuration import config
from zope.configuration import xmlconfig
from zope.configuration import zopeconfigure
from z3c.unconfigure.config import Unconfigure
from z3c.unconfigure import testing

def tearDown(test):
    zope.testing.cleanup.cleanUp()

def zcml(source):
    context = config.ConfigurationMachine()
    xmlconfig.registerCommonDirectives(context)
    config.defineGroupingDirective(context,
                                   name='unconfigure',
                                   namespace="*",
                                   schema=zopeconfigure.IZopeConfigure,
                                   handler=Unconfigure)

    # Test directives
    config.defineSimpleDirective(
        context, "print", testing.IPrint, testing.print_, namespace="*")
    config.defineSimpleDirective(
        context, "lolcat", testing.ILolCat, testing.lolcat, namespace="*")

    source = '''\
<configure package="z3c.unconfigure.testfixtures">
%s
</configure>''' % source

    xmlconfig.string(source, context)

def cat(filename):
    here = os.path.dirname(__file__)
    filename = os.path.join(here, 'testfixtures', filename)
    print open(filename).read()

def DocFileSuite(filename):
    return doctest.DocFileSuite(filename,
                                package='z3c.unconfigure',
                                globs={'zcml': zcml,
                                       'cat': cat},
                                tearDown=tearDown,
                                optionflags=doctest.NORMALIZE_WHITESPACE,
                                )
    

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(DocFileSuite('README.txt'))
    return suite

