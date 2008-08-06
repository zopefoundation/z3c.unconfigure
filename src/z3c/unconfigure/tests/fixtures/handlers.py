from zope.component import adapter

class Event(object):
    pass

@adapter(Event)
def regular(event):
    print "Regular subscriber"

@adapter(Event)
def trusted(event):
    print "Trusted subscriber"

@adapter(Event)
def located(event):
    print "Located subscriber"

@adapter(Event)
def locatedtrusted(event):
    print "Located trusted subscriber"

