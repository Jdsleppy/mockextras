# mockextras.matchers
# Matchers and Stubs for mock.
# Copyright (C) 2012 Andrew Burrows
# E-mail: burrowsa AT gmail DOT com

# mockextras 0.0.0
# https://github.com/burrowsa/mockextras

# Released subject to the BSD License
# Please see https://github.com/burrowsa/mockextras/blob/master/LICENSE.txt


"""mockextras.matchers provides matchers that act as wildcards when testing call arguments.

for example, you can use a matcher, such as Any, when defining a stub:

>>> from mock import Mock, call
>>> from mockextras.stub import stub
>>> mock = Mock()
>>> mock.side_effect = stub((call("hello", "world"), 100),
...                         (call("bye bye", Any()), 200))
>>> mock("bye bye", "world")
200
>>> mock("bye bye", "Fred")
200
>>> mock("bye bye", range(100))
200
>>> mock("bye bye", { 'a' : 1000, 'b' : 2000})
200

or when asserting call arguments:

>>> from mock import Mock
>>> mock = Mock()
>>> mock("bye bye", "world")
<Mock name='mock()' id='...'>
>>> mock.assert_called_once_with("bye bye", Any())

>>> mock("bye bye", "Fred")
<Mock name='mock()' id='...'>
>>> assert mock.call_args_list == [call("bye bye", "world"),
...                                call("bye bye", Any())]


The following matchers are defined in this module:
    * Any
    * Contains
    * AnyOf

See their documentation for more info.
"""


class Any(object):
    """The Any matcher will match any object. 
    
    >>> whatever = Any()
    >>> assert whatever == 'hello'
    >>> assert whatever ==  100
    >>> assert whatever ==  range(10)
    
    You can optionally specify a type so that Any only matches objects of that type.
    
    >>> anystring = Any(basestring)
    >>> assert anystring == 'hello'
    >>> assert anystring == 'monkey'
    >>> assert anystring == u'bonjour'
    >>> assert anystring != ['hello', 'world']
    
    Any can be used when specifying stubs:
    
    >>> from mock import Mock, call
    >>> from mockextras.stub import stub
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello", "world"), 100),
    ...                         (call("bye bye", Any()), 200))
    >>> mock("bye bye", "world")
    200
    >>> mock("bye bye", "Fred")
    200
    >>> mock("bye bye", range(100))
    200
    >>> mock("bye bye", { 'a' : 1000, 'b' : 2000})
    200
    
    or when asserting call arguments:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock("bye bye", "world")
    <Mock name='mock()' id='...'>
    >>> mock.assert_called_once_with("bye bye", Any())
    
    >>> mock("bye bye", "Fred")
    <Mock name='mock()' id='...'>
    >>> assert mock.call_args_list == [call("bye bye", "world"),
    ...                                call("bye bye", Any())]
    """
    def __init__(self, cls=object):
        self._cls = cls
    
    def __eq__(self, other):
        return isinstance(other, self._cls)

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __repr__(self):
        return 'Any(%s)' % ('' if self._cls is object else self._cls)
    
    
class Contains(object):
    """The Contains matcher will match objects that contain the given value or
    substring.
    
    >>> contains_five = Contains(5)
    >>> assert contains_five == range(10)
    >>> assert contains_five != range(4)

    >>> contains_ello = Contains('ello')
    >>> assert contains_ello == "hello"
    >>> assert contains_ello != "bye bye"

    Contains can be used when specifying stubs:
    
    >>> from mock import Mock, call
    >>> from mockextras.stub import stub
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello", "world"), 100),
    ...                         (call("bye bye", Contains('monkey')), 200))
    >>> mock("bye bye", "uncle monkey")
    200
    
    or when asserting call arguments:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock("bye bye", "world")
    <Mock name='mock()' id='...'>
    >>> mock.assert_called_once_with("bye bye", Contains('or'))
    
    >>> mock("bye bye", "Fred")
    <Mock name='mock()' id='...'>
    >>> assert mock.call_args_list == [call("bye bye", "world"),
    ...                                call("bye bye", Contains('red'))]
    """
    def __init__(self, value):
        self._value = value
    
    def __eq__(self, other):
        return self._value in other

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return 'Contains(%r)' % self._value


class AnyOf(object):
    def __init__(self, *args):
        if len(args) > 1 or (len(args) > 0 and (not hasattr(args[0], '__iter__') or isinstance(args[0], basestring))):
            self._set = set(args)
        else:
            self._set = set(*args)
    
    def __eq__(self, other):
        return other in self._set

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return 'AnyOf(%r)' % self._set