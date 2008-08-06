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
  ...   <print msg="I can has cheezburger?" />
  ...   <print msg="Goodbye World!" />
  ...   <print msg="LOL!" />
  ...
  ...   <unconfigure>
  ...     <print msg="I can has cheezburger?" />
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
