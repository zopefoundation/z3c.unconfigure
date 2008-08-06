This package allows you to disable specific bits of ZCML configuration
that may occur in other packages.  For instance, let's consider a
simple ZCML directive that prints strings:

  >>> zcml("""
  ... <print msg="Hello World!" />
  ... """)
  Hello World!

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
  ...   <unconfigure>
  ...     <lolcat who="I" canhas="cheezburger?" />
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
  ...   <unconfigure>
  ...     <print msg="I can has cheezburger?" />
  ...   </unconfigure>
  ... </configure>
  ... """)

What's a good place to add the ``unconfigure`` directives, you may
ask.  Certainly, the example from above is a not very realistic
because both the original directives and the filters are in one file.
What typically happens is that you have some third party package that
has much configuration of which you'd like to disable just one or two
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
A good name for it would be ``overrides.zcml`` (which is the
convention for overriding ZCML directives, a technique not far from
what ``unconfigure`` does).  For example:

  >>> cat('overrides.zcml')
  <unconfigure>
    <lolcat who="I" canhas="cheezburger" />
    <print msg="LOL!" />
  </unconfigure>

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
