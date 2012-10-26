import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    'Documentation\n' +
    '=============\n\n' +
    read('src', 'z3c', 'unconfigure', 'README.txt')
    + '\n' +
    read('CHANGES.txt')
    )

setup(
    name='z3c.unconfigure',
    version='1.1',
    description=("Disable specific ZCML directives in other package's "
                 "configuration"),
    long_description=long_description,
    author='Philipp von Weitershausen',
    author_email='philipp@weitershausen.de',
    url='http://pypi.python.org/pypi/z3c.unconfigure',
    license='ZPL',
    classifiers=["Programming Language :: Python",
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'zope.configuration >= 3.8.0',
                      'zope.component', # technically [zcml]
                      'zope.security',
                      'zope.event',
                      'zope.testing',
                      ],
    )
