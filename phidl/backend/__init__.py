"""
phidl backend abstraction layer.

This package provides an abstraction layer that allows phidl to use
different GDS backends. Currently only gdspy is supported.

Usage
-----
The backend is loaded automatically when phidl is imported:

    from phidl import Device
    # Device uses the gdspy backend

Future backends (e.g., klayout) can be added by implementing the
interfaces in base.py and updating this module.
"""

from types import ModuleType
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import gdspy_backend

_backend_name: str = "gdspy"
_backend_module: Optional[ModuleType] = None
_backend_classes = ["Polygon", "PolygonSet", 
                    "Cell", "CellReference", "CellArray", 
                    "Label", "Library"]

__all__ = ['set_backend', 'get_backend'] + _backend_classes

def _load_backend():
    global _backend_module
    if _backend_module is not None:
        return

    if _backend_name == "gdspy":
        from . import gdspy_backend as mod
    else:
        raise ValueError(f"Backend {_backend_name} not implemented")
        
    _backend_module = mod

def __getattr__(name):
    if name in _backend_classes:
        _load_backend()
        return getattr(_backend_module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def get_backend():
    """Get the current backend module.
    
    Returns
    -------
    module
        The backend module (gdspy_backend).
    """
    _ensure_backend()
    return _backend_module

def set_backend(name: str):
    """Set the active backend.
    
    Currently only 'gdspy' is supported. This function is provided
    for forward compatibility with future klayout support.
    
    Parameters
    ----------
    name : str
        The backend to use (must be 'gdspy').
        
    Raises
    ------
    ValueError
        If an unsupported backend name is provided.
    NotImplementedError
        If trying to switch backends after initialization.
    """
    global _backend_name, _backend_module
    
    if _backend_module is not None and _backend_name != name:
        raise RuntimeError(
            f"Cannot set backend to '{name}'. The backend '{_backend_name}' "
            "is already loaded. You must call set_backend() before accessing "
            "any layout classes."
        )
    if name not in ["gdspy"]:
        raise ValueError(
            f"Unknown backend: {name}. Currently only 'gdspy' is supported. "
            "klayout support will be added in a future version."
        )
    
    _backend_name = name
