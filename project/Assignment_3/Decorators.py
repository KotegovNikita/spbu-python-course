import copy
import inspect
from typing import Callable, Any


def curry_explicit(function, arity):
    """
    Converts a function of multiple parameters into a chain of functions of one parameter.
    Args:
        function: The function to curry.
        arity: The number of arguments the function takes.
    Returns:
        The curried function.
    Raises:
        ValueError: If the arity is negative.
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    if arity == 0:
        return lambda: function()

    def curried(*args):
        if len(args) == 0:
            raise ValueError(f"Expected {arity} argument(s), got 0")

        if len(args) > 1:
            raise ValueError(
                f"Curried function only accepts 1 argument at a time, got {len(args)}"
            )

        collected = list(args)

        def collector(arg):
            collected.append(arg)

            if len(collected) == arity:
                return function(*collected)
            elif len(collected) < arity:
                return collector
            else:
                raise ValueError(
                    f"Too many arguments: expected {arity}, got {len(collected)}"
                )

        if arity == 1:
            return function(collected[0])
        else:
            return collector

    return curried


def uncurry_explicit(function, arity):
    """
    The inverse operation of curry_explicit: converts a curried function
    back into a function of multiple parameters.

    Args:
        function: The curried function.
        arity: The number of arguments.
    Returns:
        The uncurried function.
    Raises:
        ValueError: If the arity is negative or an incorrect number of arguments is passed.
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    def uncurried(*args):
        if len(args) != arity:
            raise ValueError(f"Expected {arity} argument(s), got {len(args)}")

        if arity == 0:
            return function()

        result = function
        for arg in args:
            result = result(arg)

        return result

    return uncurried


class _EvaluatedWrapper:
    """
    Internal wrapper class to store a function that needs to be called.
    """

    def __init__(self, func: Callable[[], Any]):
        if not callable(func):
            raise TypeError("Evaluated must be initialized with a callable (function)")
        self.func = func

    def get_value(self):
        """Computes and returns the value."""
        return self.func()


class _IsolatedWrapper:
    """
    Internal marker class for Isolated.
    """

    def __init__(self):
        pass


def Evaluated(func: Callable[[], Any]):
    """
    A function to create a default value that is computed at call time.
    It takes a function with no arguments that returns a value.

    Args:
        func: A function with no arguments that returns a value.

    Returns:
        A wrapper for delayed evaluation.
    """
    return _EvaluatedWrapper(func)


def Isolated():
    """
    A function to create a placeholder default value.

    Returns:
        A marker for argument isolation.
    """
    return _IsolatedWrapper()


def smart_args(func):
    """
    A decorator that analyzes the default value types of a function's arguments and,
    depending on the type, copies and/or computes them before executing the function:
    - For Evaluated: computes the value at call time.
    - For Isolated: creates a deep copy of the passed argument.

    Supports keyword-only arguments.
    """
    sig = inspect.signature(func)
    for param_name, param in sig.parameters.items():
        default = param.default

        if isinstance(default, (_EvaluatedWrapper, _IsolatedWrapper)):
            if param.kind != inspect.Parameter.KEYWORD_ONLY:
                raise AssertionError(
                    f"Parameter '{param_name}' with Evaluated/Isolated must be keyword-only "
                )

    def wrapper(*args, **kwargs):
        if args:
            for param_name, param in sig.parameters.items():
                if isinstance(param.default, (_EvaluatedWrapper, _IsolatedWrapper)):
                    raise AssertionError(
                        "Positional arguments are not allowed for functions "
                        "with Evaluated/Isolated parameters"
                    )

        processed_kwargs = {}

        for param_name, param in sig.parameters.items():
            default = param.default

            if param_name in kwargs:
                value = kwargs[param_name]

                if isinstance(default, _IsolatedWrapper):
                    processed_kwargs[param_name] = copy.deepcopy(value)
                else:
                    processed_kwargs[param_name] = value
            else:
                if isinstance(default, _EvaluatedWrapper):
                    processed_kwargs[param_name] = default.get_value()
                elif isinstance(default, _IsolatedWrapper):
                    raise TypeError(
                        f"Parameter '{param_name}' with Isolated() requires a value to be passed"
                    )
                elif default != inspect.Parameter.empty:
                    processed_kwargs[param_name] = default

        return func(*args, **processed_kwargs)

    return wrapper
