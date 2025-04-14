Unconfiguring event handlers
----------------------------

This package also supports unconfiguring event handlers.

  >>> import zope.component.eventtesting
  >>> zope.component.eventtesting.setUp()

Consider a bunch of event handlers configured in various ways:

  >>> zcml("""
  ... <configure xmlns="http://namespaces.zope.org/zope">
  ...   <include package="zope.component" file="meta.zcml" />
  ...
  ...   <subscriber handler=".handlers.regular" />
  ...   <subscriber handler=".handlers.trusted" trusted="yes" />
  ...   <subscriber handler=".handlers.located" locate="yes" />
  ...   <subscriber handler=".handlers.locatedtrusted"
  ...               trusted="yes" locate="yes" />
  ...
  ...   <include package="z3c.unconfigure" file="meta.zcml" />
  ...   <unconfigure>
  ...     <subscriber handler=".handlers.regular" />
  ...     <subscriber handler=".handlers.trusted" trusted="yes" />
  ...     <subscriber handler=".handlers.located" locate="yes" />
  ...     <subscriber handler=".handlers.locatedtrusted"
  ...                 trusted="yes" locate="yes" />
  ...   </unconfigure>
  ... </configure>
  ... """)

Since we've unconfigured the handlers, we expect that nothing will
happen when we send the event:

  >>> from zope.event import notify
  >>> from z3c.unconfigure.tests.fixtures.handlers import Event, Event2
  >>> notify(Event())

When unconfiguring handlers, the mechanism is careful enough to
distinguish multiple registrations of the same event handler (e.g. for
different event types). For instance, consider a handler that's
registered for its default event type and then registered again for
another event type:

  >>> zcml("""
  ... <configure xmlns="http://namespaces.zope.org/zope">
  ...   <include package="zope.component" file="meta.zcml" />
  ...
  ...   <subscriber handler=".handlers.regular" />
  ...   <subscriber handler=".handlers.regular" for=".handlers.Event2" />
  ...
  ...   <include package="z3c.unconfigure" file="meta.zcml" />
  ...   <unconfigure>
  ...     <subscriber handler=".handlers.regular" />
  ...   </unconfigure>
  ... </configure>
  ... """)

We've unconfigured it for the original event type, so nothing will
happen here:

  >>> notify(Event())

But for the other event, we'll get the subscriber just fine:

  >>> notify(Event2())
  Regular subscriber Event2
