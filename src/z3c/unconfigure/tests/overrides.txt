Unconfiguration and other overrides
-----------------------------------

When placing an ``unconfigure`` grouping directive in an overrides
file together with other overrides, things should continue to work
like you'd expect: the overrides directives override things and the
``unconfigure`` directive filters actions.

Let's consider this configuration:

  >>> cat('lolcat.zcml')
  <configure>
    <print msg="Hello World!" />
    <print msg="Important configuration here." />
    <lolcat who="I" canhas="cheezburger" />
    <print msg="Goodbye World!" />
    <print msg="LOL!" />
    <print msg="This is the last directive" />
  </configure>

And a file with one override and one "unconfiguration":

  >>> cat('overrides2.zcml')
  <configure>
    <lolcat who="I" canhas="hamburger" />
    <include package="z3c.unconfigure" file="meta.zcml" />
    <unconfigure>
      <print msg="LOL!" />
    </unconfigure>
  </configure>

It works as you'd expect:

  >>> zcml("""
  ... <configure>
  ...   <include file="lolcat.zcml" />
  ...   <includeOverrides file="overrides2.zcml" />
  ... </configure>
  ... """)
  Hello World!
  Important configuration here.
  Goodbye World!
  This is the last directive
  I can has hamburger?
