from zope.interface import Interface
from zope.schema import Text

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
