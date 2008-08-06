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

            # An action by the same discriminator has been found,
            # let's remove it from the configuration machine's actions
            # list.
            self.context.actions.remove(action)
            del unique[discriminator]
