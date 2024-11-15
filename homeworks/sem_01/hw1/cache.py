from typing import (
    Callable,
    TypeVar,
)

T = TypeVar("T")


def lru_cache(capacity: int) -> Callable[[T], T]:
    """
    Параметризованный декоратор для реализации LRU-кеширования.

    Args:
        capacity: целое число, максимальный возможный размер кеша.

    Returns:
        Декоратор для непосредственного использования.

    Raises:
        TypeError, если capacity не может быть округлено и использовано
            для получения целого числа.
        ValueError, если после округления capacity - число, меньшее 1.
    """
    capacity = round(capacity)
    if capacity < 1:
        raise ValueError("Bad capacity < 1")

    lru_cache = {}

    def decorator(func):
        def wrapper(*args, **kwargs):
            hash_key = hash(args) + hash(tuple(sorted(kwargs.items())))
            if hash_key in lru_cache:
                result = lru_cache.pop(hash_key)
                lru_cache[hash_key] = result
            else:
                result = func(*args, **kwargs)

                lru_cache[hash_key] = result

                if len(lru_cache) > capacity:
                    first_key = next(iter(lru_cache))
                    del (lru_cache[first_key])

            return result
        return wrapper
    return decorator
