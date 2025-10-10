from functools import reduce
from typing import Callable, Iterable, Generator, Any, Sequence
import random


def generate_data(count: int, min_val: int, max_val: int) -> Generator[int, None, None]:
    """
    Генерирует ограниченное количество случайных целых чисел в заданном диапазоне.

    Args:
        count (int): Количество случайных чисел для генерации.
        min_val (int): Минимальное возможное значение (включительно).
        max_val (int): Максимальное возможное значение (включительно).

    Yields:
        Generator[int, None, None]: Случайное целое число в указанном диапазоне.
    """
    for _ in range(count):
        yield random.randint(min_val, max_val)


def pipeline(source_data: Iterable[Any], *operations: Callable | tuple) -> Generator:
    """
    Применяет последовательность операций к потоку данных.

    Операции могут быть двух видов:
    1.  Простая функция (Callable), которая принимает и возвращает итератор.
    2.  Кортеж (tuple), где первый элемент - функция (map, filter),
        а последующие - её "замороженные" аргументы. Поток данных
        будет подставлен последним аргументом.

    Args:
        source_data (Iterable[Any]): Исходный поток данных.
        *operations (Callable | tuple): Последовательность операций.

    Returns:
        Generator: Генератор с обработанными данными.
    """
    stream = source_data
    for op in operations:
        if isinstance(op, tuple):
            op_func, *op_args = op
            stream = op_func(*op_args, stream)
        elif callable(op):
            stream = op(stream)
        else:
            raise TypeError(f"Unsupported operation type: {type(op)}")

    yield from stream


def aggregator(source_data: Iterable[Any], output_type: Callable = list) -> Sequence:
    """Collects all items from a data stream into a collection.

    This function triggers the execution of a lazy pipeline by iterating over
    the source data stream and storing the results in a specified collection type.

    Args:
        source_data (Iterable[Any]): The data stream (typically the output of a
            pipeline) to be consumed.
        output_type (Callable, optional): The constructor for the desired output
            collection. Defaults to list. Can be set, tuple, etc.

    Returns:
        Sequence: A collection (e.g., a list, tuple, set) containing all the
            processed items from the source data stream.
    """
    return output_type(source_data)
