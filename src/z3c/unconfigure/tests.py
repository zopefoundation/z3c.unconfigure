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
    config.defineSimpleDirective(
        context, "print", testing.IPrint, testing.print_, namespace="*")

    xmlconfig.string(source, context)


def test_suite():
    return doctest.DocFileSuite('README.txt',
                                package='z3c.unconfigure',
                                globs={'zcml': zcml},
                                tearDown=tearDown)
