from zope.component import adapter

class Event(object):
    pass

class Event2(object):
    pass

@adapter(Event)
def regular(event):
    print "Regular subscriber", event.__class__.__name__

@adapter(Event)
def trusted(event):
    print "Trusted subscriber"

@adapter(Event)
def located(event):
    print "Located subscriber"

@adapter(Event)
def locatedtrusted(event):
    print "Located trusted subscriber"

