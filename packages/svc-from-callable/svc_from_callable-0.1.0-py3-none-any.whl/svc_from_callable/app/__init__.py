"""__init__.py."""
import inspect
from importlib.util import find_spec, module_from_spec
from typing import Callable, ParamSpec

from strangeworks_core.config.config import Config

_cfg = Config()

# better way to provide a parameter spec for a Callable parameter types
# see https://docs.python.org/3/library/typing.html#typing.ParamSpec
P = ParamSpec("P")
AppFunction = Callable[P, any]


def _get_callable(module: str, callable_name: str) -> AppFunction:
    """Loads Callable.

    Load the Callable/Function specified by callable_name defined in module.
    Imitates `from module import callable_name` at runtime.

    Parameters
    ----------
    module: str
        fully qualified name of the module where the callable is implemented.
    callable_name: str
        name of the function.

    Returns
    -------
    :AppFunction
        Callable to be used as the implementation of the service.
    """
    mod_spec = find_spec(module)
    if mod_spec is None:
        raise ValueError(f"unable to find the {module} module.")
    mod = module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)

    _functions = inspect.getmembers(mod, inspect.isfunction)

    for name, _fn in _functions:
        if name == callable_name:
            return _fn
    return None


#from sample.callable import example

_CALLABLE_NAME = _cfg.get("name", profile="callable_svc")
_CALLABLE_MODULE = _cfg.get("module", profile="callable_svc")
CallableImplenmetation: AppFunction = _get_callable(
    module=_CALLABLE_MODULE, callable_name=_CALLABLE_NAME
)
