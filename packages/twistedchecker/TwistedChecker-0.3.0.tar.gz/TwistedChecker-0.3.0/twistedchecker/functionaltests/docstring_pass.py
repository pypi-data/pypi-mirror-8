# enable: W9201,W9202,W9203,W9204,W9205,W9206,W9207
"""
A docstring with a wrong indentation.
Docstring should have consistent indentations.
"""

class foo:
    """
    The opening/closing of docstring should be on a line by themselves.
    """

    def a(self):
        """
        A docstring with a correct indentation.
        """
        pass


    def b(self, argument1):
        """
        This docstring should contain epytext markups of argument1.

        @param argument1: an argument
        @type argument1: C{int}
        """
        pass


    def c(self):
        """
        This docstring should contain a @return and @rtype markup.

        @return: return 1
        @rtype: C{int}
        """
        return 1


    def d(self, a):
        """
        There should be a blank line before epytext markups.

        @param a: a argument
        @type a: C{int}
        @return: return a
        @rtype: C{int}
        """
        return a


    def e(self):
        """
        A method contains a function k().
        No warning should be generated
        """
        def k():
            pass


    def f(self):
        """
        A method returns nothing.
        """
        return



class Bar(self):
    """
    A cvar is recognized as being the start of epytext markup.

    @cvar foo: bar baz
    @type foo: bax
    """

    def a(self):
        """
        A raises field is recognized as being the start of epytext markup.

        @raises FoobarException: An exception.
        @returns: C{int}
        """

    def b(self):
        """
        A raise (because we are inconsistent about stuff) should also be
        recognized as the start of epytext markup.

        @raise BarException: Another exception.
        @returns: C{int}
        """



class Baz(self):
    """
    An ivar is recognized as being the start of epytext markup.

    @ivar foo: bar baz
    @type foo: bax
    """
