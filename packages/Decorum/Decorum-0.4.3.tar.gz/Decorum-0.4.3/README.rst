=======
Decorum
=======

Decorum is a simple tool which aims to make it easier to write flexible
and simple decorators. It can also act similarly to ``functools.wraps``.

Typical usage looks like this::

    from decorum import decorator

    @decorator
    class my_decorator:
        def wraps(self, f):
            print "I'm returning the function! You can keep it!"
            return f

Decorum lets you write decorators with and without arguments in a unified way.
Your decorator can be used with or without arguments, called or not, and it
will work the same way::

    @my_decorator
    def foo(x): print x

Is identical to::

    @my_decorator()
    def foo(x): print x

Writing decorators
==================

Decorum provides two easy ways to write your own decorators. You can use
``decorum.decorator`` to decorate decorator classes, or you can directly
subclass decorum.Decorum. There are only two methods to be aware of when
writing your own decorators. Define a ``wraps`` method to handle the actual
decoration and return the decorated function, and optionally define an ``init``
method to handle any arguments you want to accept, and handle basic setup (it's
called before decoration by ``__init__``, you can use it in a similar fashion
to a real ``__init__`` method). By default decorum will try to keep assign
certain attributes to the wrapped function for you, namely ``__doc__`` and
``__name__``. You can set ``keep_attrs`` to ``None`` to turn this off, or
provide it with a list of attributes you want applied to the returned decorated
function.

Here is a slightly fancier example::

    from decorum import decorator

    @decorator
    class fancy:
        def init(self, arg=None):
            self.arg = arg

        def wraps(self, f):
            if self.arg:
                def newf():
                    print self.arg
            else:
                def newf():
                    print 'wut'
            return newf

    @fancy
    def foo():
        pass
    foo()

    @fancy('woof')
    def foo():
        pass
    foo()

    # prints
    wut
    woof
