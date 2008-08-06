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
from zope.security import adapter
import zope.component.zcml

def is_subscriber(discriminator, callable=None, args=(), kw={},
                  includepath=(), info='', order=0):
    """Determines whether an action has been emitted from the
    <subscriber /> directive.
    """
    return (discriminator is None and
            callable is zope.component.zcml.handler and
            args[0] == 'registerHandler')

def real_subscriber_factory(discriminator, callable=None, args=(), kw={},
                            includepath=(), info='', order=0):
    """Returns the real subscriber factory (<subscriber /> sometimes
    wraps them in some security-related adapter factory).

    This function assumes that the action in question is a subscriber
    action.  In other words, is_subscriber(*args) is True.
    """
    factory = args[1]
    if isinstance(factory, (adapter.LocatingTrustedAdapterFactory,
                            adapter.LocatingUntrustedAdapterFactory,
                            adapter.TrustedAdapterFactory)):
        factory = factory.factory
    return factory

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
        unique = dict((action[0], action) for action in self.context.actions
                      if action[0] is not None)

        # Find all subscriber actions and store them as factory -> action.
        # They're a special case because their discriminators are None,
        # so we can't pull the same trick as with other directives.
        subscribers = dict((real_subscriber_factory(*action), action)
                           for action in self.context.actions
                           if is_subscriber(*action))
        # XXX should make mapping (factory, required) -> action

        # Now let's go through the actions within 'unconfigure'
        # (hereafter called "unactions" :)) and use their
        # discriminator to remove the real actions
        for unaction in self.actions:
            # Special case subscriber actions.
            if is_subscriber(*unaction):
                factory = real_subscriber_factory(*unaction)
                action = subscribers.get(factory)
                if action is None:
                    continue
                self.remove_action(action)
                del subscribers[factory]

            # Generic from here
            discriminator = unaction[0]
            if discriminator is None:
                continue
            action = unique.get(discriminator)
            if action is None:
                # Trying to unconfigure something that hasn't been
                # configured in the first place.  Ignore.
                continue

            self.remove_action(action)
            del unique[discriminator]

    def remove_action(self, action):
        # We can't actually remove actions because we mustn't change
        # the length of the actions list.  The main reason is that
        # includeOverrides relies on the length of the action list
        # (and we could easily be included via includeOverrides and
        # therefore run into this problem).  So let's simply replace
        # actions with a null value.  Actions whose callable is None
        # won't be executed.
        i = self.context.actions.index(action)
        self.context.actions[i] = (None, None)
