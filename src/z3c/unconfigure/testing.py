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
"""Test fixtures
"""
import os
import zope.testing.cleanup
from zope.interface import Interface
from zope.schema import Text, TextLine
from zope.testing import doctest
from zope.configuration import config
from zope.configuration import xmlconfig

class IPrint(Interface):
    msg = Text(title=u'Message')

def print_(_context, msg):
    _context.action(
        discriminator=('print', msg),
        callable=do_print,
        args=(msg,),
        )

def do_print(msg):
    print msg


class ILolCat(Interface):
    who = TextLine(title=u'Who')
    canhas = TextLine(title=u'Can has?')

def lolcat(_context, who, canhas):
    _context.action(
        discriminator=('lolcat', who,),
        callable=do_print,
        args=(who + ' can has ' + canhas + '?',),
        )

def tearDown(test):
    zope.testing.cleanup.cleanUp()

def zcml(source):
    context = config.ConfigurationMachine()
    xmlconfig.registerCommonDirectives(context)

    # Test directives
    config.defineSimpleDirective(
        context, "print", IPrint, print_, namespace="*")
    config.defineSimpleDirective(
        context, "lolcat", ILolCat, lolcat, namespace="*")

    source = '''\
<configure package="z3c.unconfigure.tests.fixtures">
%s
</configure>''' % source

    xmlconfig.string(source, context)

def cat(filename):
    here = os.path.dirname(__file__)
    filename = os.path.join(here, 'tests', 'fixtures', filename)
    print open(filename).read()

def DocFileSuite(filename):
    return doctest.DocFileSuite(filename,
                                package='z3c.unconfigure.tests',
                                globs={'zcml': zcml,
                                       'cat': cat},
                                tearDown=tearDown,
                                optionflags=doctest.NORMALIZE_WHITESPACE,
                                )
