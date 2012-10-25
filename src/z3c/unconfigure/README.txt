Introduction
------------

This package allows you to disable specific bits of ZCML configuration
that may occur in other packages.  For instance, let's consider a
simple ZCML directive that prints strings and a silly one that prints
lolcat messages:

  >>> zcml("""
  ... <print msg="Hello World!" />
  ... <lolcat who="I" canhas="cheezburger" />
  ... """)
  Hello World!
  I can has cheezburger?

Now let's say this directive were used a bunch of times, but we wanted
to prevent one or two of its occurrences.  To do that we simply repeat
the directive inside the ``unconfigure`` grouping directive.  This
grouping directive will look at all the previous directives and filter
out the ones we want to exclude:

  >>> zcml("""
  ... <configure>
  ...   <print msg="Hello World!" />
  ...   <lolcat who="I" canhas="cheezburger" />
  ...   <print msg="Goodbye World!" />
  ...   <print msg="LOL!" />
  ...
  ...   <include package="z3c.unconfigure" file="meta.zcml" />
  ...   <unconfigure>
  ...     <lolcat who="I" canhas="cheezburger" />
  ...     <print msg="LOL!" />
  ...   </unconfigure>
  ... </configure>
  ... """)
  Hello World!
  Goodbye World!

If you're trying to unconfigure something that hasn't been configured
in the first place, nothing will happen:

  >>> zcml("""
  ... <configure>
  ...   <include package="z3c.unconfigure" file="meta.zcml" />
  ...   <unconfigure>
  ...     <lolcat who="I" canhas="cheezburger" />
  ...   </unconfigure>
  ... </configure>
  ... """)

Where to place "unconfiguration"
--------------------------------

What's a good place to add the ``unconfigure`` directives, you may
ask.  Certainly, the example from above is not very realistic because
both the original directives and the filters are in one file.  What
typically happens is that you have some third party package that has
much configuration of which you'd like to disable just one or two
directives.  Like this file, for instance:

  >>> cat('lolcat.zcml')
  <configure>
    <print msg="Hello World!" />
    <print msg="Important configuration here." />
    <lolcat who="I" canhas="cheezburger" />
    <print msg="Goodbye World!" />
    <print msg="LOL!" />
    <print msg="This is the last directive" />
  </configure>

What you can do now is write a separate ZCML file in *your* package.
A good name for it would be ``overrides.zcml`` (which is the naming
convention for ZCML files containing overriding directives, a
technique not unlike to what ``unconfigure`` does).  For example,
let's say we wanted to undo some silly configuration in the above
third party file:

  >>> cat('overrides.zcml')
  <configure>
    <include package="z3c.unconfigure" file="meta.zcml" />
    <unconfigure>
      <lolcat who="I" canhas="cheezburger" />
      <print msg="LOL!" />
    </unconfigure>
  </configure>

What you would do now is include first that third party package's
configuration and then load your overrides (which is typically done
using ``includeOverrides``, either explicitly by you or for you by
``site.zcml``):

  >>> zcml("""
  ... <configure>
  ...   <include file="lolcat.zcml" />
  ...   <includeOverrides file="overrides.zcml" />
  ... </configure>
  ... """)
  Hello World!
  Important configuration here.
  Goodbye World!
  This is the last directive

In this case, simply including the file with the ``<include />``
directive would've sufficed as well.  What matters is that the
"unconfiguration" happens *after* the original configuration, and
override files are a good place to ensure this.

It can also be conveniend to unconfigure an entire zcml file. This can
be done by using an include statement inside an unconfigure block:

  >>> zcml("""
  ... <configure>
  ...   <print msg="The new hello" />
  ...   <include file="lolcat.zcml" />
  ...   <include package="z3c.unconfigure" file="meta.zcml" />
  ...   <unconfigure>
  ...     <include file="lolcat.zcml" />
  ...   </unconfigure>
  ...   <print msg="The final goodbye" />
  ... </configure>
  ... """)  # XXX this is currently broken, so the test fails
  The new hello
  The final goodbye


