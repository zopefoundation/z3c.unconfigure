import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    "Documentation\n"
    + "=============\n\n"
    + read("src", "z3c", "unconfigure", "README.rst")
    + "\n"
    + read("CHANGES.rst")
)

setup(
    name="z3c.unconfigure",
    version="3.0",
    description=(
        "Disable specific ZCML directives in other package's configuration"),
    long_description=long_description,
    author="Philipp von Weitershausen",
    author_email="zope-dev@zope.dev",
    url="https://github.com/zopefoundation/z3c.unconfigure",
    license="ZPL",
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "setuptools",
        "zope.configuration >= 3.8.0",
        "zope.component",  # technically [zcml]
        "zope.security",
        "zope.event",
        "zope.testing",
    ],
)
