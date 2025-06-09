from typing import Type, TypeVar, overload


_T = TypeVar("_T", str, int, float)


@overload
def loop_input(msg: str) -> str: ...
@overload
def loop_input(msg: str, options: Type[_T]) -> _T: ...
@overload
def loop_input(msg: str, options: set[_T]) -> _T: ...
def loop_input(msg: str, options: Type[_T] | set[_T] | None = None) -> str | _T:
    """Request user input until a valid input is given.

    Invalid inputs will raise errors, which print to terminal
    and initate another input request.

    `_T` = `(str, int, float, tuple, list, set)`

    Parameters
    ----------
    `msg` : `str`
        The message to display to the user each looped request.
    `options` : `Type[_T]` or `set[_T]`, optional
        The filter for valid inputs. If `Type[_T]`, any input parseable to
        `_T` will be accepted, and the function will return in instance of `_T`.
        If `set[_T]`, only inputs contained in `options` will be accepted,
        and the function will return an instance of `_T`.
    """
    if isinstance(options, type):
        typ = options
    elif isinstance(options, set) and len(options) > 0:
        options_typ = {type(item) for item in options}
        if len(options_typ) > 1:
            raise TypeError("All items of `options` must be of the same type")
        typ = options_typ.pop()
    else:
        typ = str
    while True:
        try:
            inp = typ(input(msg))
            if isinstance(options, set) and inp not in options:
                raise KeyError(f"{inp} not in options")
        except Exception as e:
            print(f"{type(e).__name__}, {e}")
            continue
        return inp

