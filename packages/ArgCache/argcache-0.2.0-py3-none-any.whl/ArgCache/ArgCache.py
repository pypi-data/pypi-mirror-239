"""Caching function decorator

The module is a Python implementation of a caching function 
that can be used to cache the results of a function call. 
The module defines a CacheFunc class that takes a function 
as input and returns a cached version of the function. 
The cached version of the function stores the results of 
previous function calls in a dictionary, and returns the 
cached result if the same function is called again with the 
same arguments. The module also defines a HashableDict class 
that can be used to create a hashable dictionary, which is 
used as the key for the cached results. The module includes 
three test functions that demonstrate the performance benefits 
of using the cached function.
"""

from typing import Callable
import timeit

class HashableDict(dict):
    """Hashable dictionary class"""

    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


class ArgCache:
    """Caching function decorator class"""

    def __init__(self, func: Callable):
        self.func = func
        self.cache = dict()


    def keyer(self, *args: tuple, **kwargs: dict):
        key = (
            "|"
            + "|".join([str(arg) for arg in args])
            + "|"
            + "|".join([str(kwarg) for kwarg in kwargs.items()])
            + "|"
        )
        return key

    def __call__(self, *args, **kwargs):
        key = self.keyer(*args, **kwargs)
        output = self.cache.get(key)

        if output is None:
            output = self.func(*args, **kwargs)
            self.cache[key] = output

        return output

class ArgCacheObjKey(ArgCache):
    def keyer(self, *args: tuple, **kwargs: dict):
        return args, HashableDict(kwargs)


def main():
    def test_no_cache(number):
        def fib(n):
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        def tests():
            assert fib(10) == 55
            assert fib(20) == 6765
            assert fib(30) == 832040

        return timeit.timeit(tests, number=number)

    def test_cache_func(number):
        @ArgCache
        def fib(n):
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        def tests():
            assert fib(10) == 55
            assert fib(20) == 6765
            assert fib(30) == 832040

        return timeit.timeit(tests, number=number)

    def test_cache_func_obj_key(number):
        @ArgCacheObjKey
        def fib(n):
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        def tests():
            assert fib(10) == 55
            assert fib(20) == 6765
            assert fib(30) == 832040

        return timeit.timeit(tests, number=number)

    no_cache_iterations = 10
    print("Testing no cache...")
    time_no_cache = test_no_cache(no_cache_iterations)
    print(
        f"Time taken for no cache: {time_no_cache:.6f} seconds, ran {no_cache_iterations} times"
    )
    print(
        f"Average time taken for no cache: {time_no_cache/no_cache_iterations:.6f} seconds"
    )

    cachefunc_iterations = 100000
    print("Testing CacheFunc...")
    time_cache_func = test_cache_func(cachefunc_iterations)
    print(
        f"Time taken for CacheFunc: {time_cache_func:.6f} seconds, ran {cachefunc_iterations} times"
    )
    print(
        f"Average time taken for CacheFunc: {time_cache_func/cachefunc_iterations:.6f} seconds"
    )

    cachefunc2_iterations = 100000
    print("Testing CacheFunc with object key...")
    time_cache_func2 = test_cache_func_obj_key(cachefunc2_iterations)
    print(
        f"Time taken for CacheFunc2: {time_cache_func2:.6f} seconds, ran {cachefunc2_iterations} times"
    )
    print(
        f"Average time taken for CacheFunc2: {time_cache_func2/cachefunc2_iterations:.6f} seconds"
    )


if __name__ == "__main__":
    main()
