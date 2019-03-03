from functools import singledispatch, update_wrapper

__all__ = [
    'method_dispatch'
]


def method_dispatch(func):
    """Monkey patch to use functools.singledispatch inside class.

    Custom singledispatch looks at first argument which in class will be always
    `self` type.

    The function simply dispatches by second argument (so it can be also used
    as non class method.
    """

    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper
