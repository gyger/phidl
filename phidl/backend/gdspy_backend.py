"""
gdspy backend implementation for phidl.

This module provides thin wrappers around gdspy classes that implement
the abstract backend interface. Since phidl was originally built on gdspy,
most functionality is inherited directly.
"""

import gdspy
import gdspy.library
from gdspy import PolygonSet

from typing import List, Tuple, Optional, Any, Dict

from . import base

# Disable gdspy's automatic current_library behavior
gdspy.library.use_current_library = False


class GdspyPolygon(gdspy.Polygon, base.Polygon):
    """gdspy Polygon implementation.
    
    Inherits from gdspy.Polygon and implements base.Polygon interface.
    Most methods are inherited directly from gdspy.
    """
    
    def __init__(self, points, layer: int = 0, datatype: int = 0):
        """Create a gdspy polygon.
        
        Parameters
        ----------
        points : array-like[N][2]
            Coordinates of polygon vertices.
        layer : int
            GDSII layer number.
        datatype : int
            GDSII datatype number.
        """
        super().__init__(points=points, layer=layer, datatype=datatype)


class GdspyCell(gdspy.Cell, base.Cell):
    """gdspy Cell implementation.
    
    Inherits from gdspy.Cell and implements base.Cell interface.
    """
    
    def __init__(self, name: str, exclude_from_current: bool = True):
        """Create a gdspy cell.
        
        Parameters
        ----------
        name : str
            Cell name.
        exclude_from_current : bool
            If True, don't add to gdspy's current library (phidl manages this).
        """
        super().__init__(name=name, exclude_from_current=exclude_from_current)


class GdspyCellReference(gdspy.CellReference, base.CellReference):
    """gdspy CellReference implementation.
    
    Inherits from gdspy.CellReference and implements base.CellReference interface.
    """
    
    def __init__(
        self,
        ref_cell,
        origin: Tuple[float, float] = (0, 0),
        rotation: float = 0,
        magnification: Optional[float] = None,
        x_reflection: bool = False,
        ignore_missing: bool = False,
    ):
        """Create a gdspy cell reference.
        
        Parameters
        ----------
        ref_cell : GdspyCell
            The cell to reference.
        origin : tuple
            Reference position.
        rotation : float
            Rotation angle in degrees.
        magnification : float or None
            Magnification factor.
        x_reflection : bool
            Whether to reflect across x-axis.
        ignore_missing : bool
            Whether to ignore missing cells.
        """
        super().__init__(
            ref_cell=ref_cell,
            origin=origin,
            rotation=rotation,
            magnification=magnification,
            x_reflection=x_reflection,
            ignore_missing=ignore_missing,
        )


class GdspyCellArray(gdspy.CellArray, base.CellArray):
    """gdspy CellArray implementation.
    
    Inherits from gdspy.CellArray and implements base.CellArray interface.
    """
    
    def __init__(
        self,
        ref_cell,
        columns: int,
        rows: int,
        spacing: Tuple[float, float],
        origin: Tuple[float, float] = (0, 0),
        rotation: float = 0,
        magnification: Optional[float] = None,
        x_reflection: bool = False,
        ignore_missing: bool = False,
    ):
        """Create a gdspy cell array.
        
        Parameters
        ----------
        ref_cell : GdspyCell
            The cell to reference.
        columns : int
            Number of columns.
        rows : int  
            Number of rows.
        spacing : tuple
            (x, y) spacing between instances.
        origin : tuple
            Array origin position.
        rotation : float
            Rotation angle in degrees.
        magnification : float or None
            Magnification factor.
        x_reflection : bool
            Whether to reflect across x-axis.
        ignore_missing : bool
            Whether to ignore missing cells.
        """
        super().__init__(
            ref_cell=ref_cell,
            columns=columns,
            rows=rows,
            spacing=spacing,
            origin=origin,
            rotation=rotation,
            magnification=magnification,
            x_reflection=x_reflection,
            ignore_missing=ignore_missing,
        )


class GdspyLabel(gdspy.Label, base.Label):
    """gdspy Label implementation.
    
    Inherits from gdspy.Label and implements base.Label interface.
    """
    
    def __init__(
        self,
        text: str,
        position: Tuple[float, float],
        anchor: str = "o",
        rotation: float = 0,
        magnification: Optional[float] = None,
        x_reflection: bool = False,
        layer: int = 0,
        texttype: int = 0,
    ):
        """Create a gdspy label.
        
        Parameters
        ----------
        text : str
            Label text.
        position : tuple
            Label position.
        anchor : str
            Anchor point.
        rotation : float
            Rotation angle.
        magnification : float or None
            Magnification factor.
        x_reflection : bool
            Whether to reflect.
        layer : int
            GDSII layer.
        texttype : int
            GDSII texttype.
        """
        super().__init__(
            text=text,
            position=position,
            anchor=anchor,
            rotation=rotation,
            magnification=magnification,
            x_reflection=x_reflection,
            layer=layer,
            texttype=texttype,
        )


class GdspyLibrary(base.Library):
    """gdspy GdsLibrary wrapper implementing base.Library interface."""
    
    def __init__(
        self,
        name: str = "library",
        unit: float = 1e-6,
        precision: float = 1e-9,
    ):
        """Create a gdspy library.
        
        Parameters
        ----------
        name : str
            Library name.
        unit : float
            Database unit in meters.
        precision : float
            Database precision in meters.
        """
        self._lib = gdspy.GdsLibrary(name=name, unit=unit, precision=precision)
        self.unit = unit
        self.precision = precision
    
    def write_gds(self, filename: str, cells: List[Any]) -> str:
        """Write cells to a GDS file.
        
        Parameters
        ----------
        filename : str
            Output filename.
        cells : list
            List of cells to write.
            
        Returns
        -------
        filename : str
            The filename written to.
        """
        self._lib.write_gds(filename, cells=cells)
        return filename
    
    def read_gds(
        self,
        filename: str,
        cellname: Optional[str] = None,
        flatten: bool = False,
    ) -> Dict[str, Any]:
        """Read cells from a GDS file.
        
        Parameters
        ----------
        filename : str
            Input filename.
        cellname : str or None
            Specific cell to read, or None for all cells.
        flatten : bool
            Whether to flatten the hierarchy.
            
        Returns
        -------
        cells : dict
            Dictionary mapping cell names to cell objects.
        """
        self._lib.read_gds(filename)
        return self._lib.cells


# Aliases matching the backend interface names
Polygon = GdspyPolygon
Cell = GdspyCell
CellReference = GdspyCellReference
CellArray = GdspyCellArray
Label = GdspyLabel
Library = GdspyLibrary