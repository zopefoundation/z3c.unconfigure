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
"""Test fixtures
"""
from zope.interface import Interface
from zope.schema import Text, TextLine

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
