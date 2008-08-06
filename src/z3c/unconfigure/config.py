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
"""The 'unconfigure' grouping directive
"""
from zope.configuration.zopeconfigure import ZopeConfigure

class Unconfigure(ZopeConfigure):

    def __init__(self, context, **kw):
        super(Unconfigure, self).__init__(context, **kw)
        # Make a new actions list here.  This will shadow
        # context.actions which would otherwise be "inherited" by our
        # superclass's __getattr__.  By shadowing the original list,
        # all actions within 'unconfigure' will be added to this list
        # here, not the global actions list. 
        self.actions = []

    def after(self):
        # Get a discriminator -> action representation of all the
        # actions that have been churned out so far.
        unique = dict((action[0], action) for action in self.context.actions)

        # Now let's go through the actions within 'unconfigure'
        # (hereafter called "unactions" :)) and use their
        # discriminator to remove the real actions
        for unaction in self.actions:
            discriminator = unaction[0]
            if discriminator is None:
                # XXX apply special majyck for subscribers here
                continue
            action = unique.get(discriminator)
            if action is None:
                # Trying to unconfigure something that hasn't been
                # configured in the first place.  Ignore.
                continue

            # An action with the same discriminator has been found.
            # We can't remove it because we mustn't change the length
            # of the actions list (because includeOverrides relies on
            # this not to change and we could easily be included via
            # includeOverrides).
            i = self.context.actions.index(action)
            self.context.actions[i] = (None, None)

            # Action has been replaced, no longer need to remember.
            del unique[discriminator]
