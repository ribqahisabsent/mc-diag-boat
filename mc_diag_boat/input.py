from typing import SupportsIndex, Type, TypeVar, overload
from .vec2 import Vec2


_T = TypeVar("_T", str, int, float)


@overload
def loop_input(msg: str, options: Type[_T] = str, default: _T | None = None) -> _T: ...
@overload
def loop_input(msg: str, options: set[_T], default: _T | None = None) -> _T: ...
def loop_input(
    msg: str,
    options: Type[_T] | set[_T] = str,
    default: _T | None = None
) -> str | _T:
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
    `default` : `_T`, optional
        The default return value if nothing is entered.
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
            inp = input(msg)
            if default is not None and inp == "":
                return default
            inp = typ(inp)
            if isinstance(options, set) and inp not in options:
                raise KeyError(f"{inp} is not an option")
        except Exception as e:
            print(f"{type(e).__name__}, {e}")
            continue
        return inp


@overload
def vec2_input(msg: str, t: Type[SupportsIndex]) -> Vec2[int]: ...
@overload
def vec2_input(msg: str, t: Type[float]) -> Vec2[float]: ...
def vec2_input(msg: str, t: Type[SupportsIndex | float]) -> Vec2:
    if issubclass(t, SupportsIndex):
        t = int
    print(msg)
    return Vec2(loop_input("    x: ", t), loop_input("    z: ", t))

