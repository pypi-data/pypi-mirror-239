from __future__ import annotations

import functools
import typing as t
import weakref

R = t.TypeVar("R")
Self = t.TypeVar("Self")
P = t.ParamSpec("P")


@t.overload
def cached_method(
    func: t.Callable[t.Concatenate[Self, P], R]
) -> t.Callable[t.Concatenate[Self, P], R]:
    ...


@t.overload
def cached_method(
    maxsize: t.Optional[int] = 128, typed: bool = False
) -> t.Callable[
    [t.Callable[t.Concatenate[Self, P], R]], t.Callable[t.Concatenate[Self, P], R]
]:
    ...


def cached_method(*lru_args, **lru_kwargs):
    """Just like functools.lru_cache, but creates a new cache for each instance.

    Two benefits:
    - The cache is cleared when the instance is garbage collected (by using weakref)
    - The instance (self) is not used as key, so instances can be unhashable.

    Drawbacks:
    - The cache is not shared between instances.

    Based on:
    https://gist.github.com/pavelpy/69f8cdad94aaf59abcf879bda66bfd1a
    with the following improvements:
    - Can be called without parenthesis to use default lru_cache arguments.
    - Added type annotations.

    Usage:
    >>> class MyClass:
    ...     @cached_method
    ...     def my_method(self, arg):
    ...         print("Computing...")
    ...         return arg

    >>> mc1 = MyClass()
    >>> mc1.my_method(1)
    Computing...
    1
    >>> mc1.my_method(1)
    1
    >>> mc1.my_method(2)
    Computing...
    2
    >>> mc1.my_method(2)
    2

    Another class instance will have a different cache:
    >>> mc2 = MyClass()
    >>> mc2.my_method(1)
    Computing...
    1
    >>> mc2.my_method(1)
    1

    Cache can be cleared:
    >>> mc1.my_method.cache_clear()
    >>> mc1.my_method(1)
    Computing...
    1

    Cache is stored on the instance:
    >>> MyClass.my_method.cache_info()
    Traceback (most recent call last):
    ...
    AttributeError: 'function' object has no attribute 'cache_info'

    Garbage collection works:
    >>> mc1_weak = weakref.ref(mc1)
    >>> del mc1
    >>> mc1_weak() is None  # Instance has been garbage collected
    True
    """
    if len(lru_args) == 1 and callable(lru_args[0]) and not lru_kwargs:
        # No arguments were passed, so we're being called as @cached_method without parenthesis.
        func = lru_args[0]
        return cached_method()(func)

    def decorator(
        func: t.Callable[t.Concatenate[Self, P], R]
    ) -> t.Callable[t.Concatenate[Self, P], R]:
        @functools.wraps(func)
        def wrapped_func(self: Self, *args: P.args, **kwargs: P.kwargs) -> R:
            # We're storing the wrapped method inside the instance. If we had
            # a strong reference to self the instance would never die.
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @functools.lru_cache(*lru_args, **lru_kwargs)
            def cached_method(*args: P.args, **kwargs: P.kwargs):
                self = self_weak()
                assert self is not None, "Instance has been garbage collected"
                return func(self, *args, **kwargs)

            setattr(self, func.__name__, cached_method)
            return cached_method(*args, **kwargs)

        return wrapped_func

    return decorator
