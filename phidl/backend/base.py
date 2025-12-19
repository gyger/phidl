"""
Abstract base classes defining the backend interface for phidl.

All backend implementations must implement these interfaces to ensure
compatibility with the phidl Device/Polygon/Reference classes.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any, Dict
import numpy as np


class Polygon(ABC):
    """Abstract polygon interface.
    
    A polygon stores geometry as point arrays with layer/datatype information.
    """
    
    @abstractmethod
    def __init__(self, points: np.ndarray, layer: int, datatype: int):
        """Create a polygon.
        
        Parameters
        ----------
        points : array-like[N][2]
            Coordinates of polygon vertices.
        layer : int
            GDSII layer number.
        datatype : int
            GDSII datatype number.
        """
        pass
    
    @abstractmethod
    def get_bounding_box(self) -> np.ndarray:
        """Return bounding box as [[xmin, ymin], [xmax, ymax]]."""
        pass
    
    @abstractmethod
    def rotate(self, angle: float, center: Tuple[float, float] = (0, 0)):
        """Rotate polygon by angle (radians) around center."""
        pass
    
    @abstractmethod
    def translate(self, dx: float, dy: float):
        """Translate polygon by (dx, dy)."""
        pass
    
    @property
    @abstractmethod
    def polygons(self) -> List[np.ndarray]:
        """Return list of point arrays (for multi-polygon support)."""
        pass
    
    @polygons.setter
    @abstractmethod
    def polygons(self, value: List[np.ndarray]):
        """Set polygon point arrays."""
        pass
    
    @property
    @abstractmethod
    def layers(self) -> List[int]:
        """Return list of layer numbers for each polygon."""
        pass
    
    @layers.setter
    @abstractmethod
    def layers(self, value: List[int]):
        """Set layers list."""
        pass
    
    @property
    @abstractmethod
    def datatypes(self) -> List[int]:
        """Return list of datatypes for each polygon."""
        pass
    
    @datatypes.setter
    @abstractmethod
    def datatypes(self, value: List[int]):
        """Set datatypes list."""
        pass


class Cell(ABC):
    """Abstract cell interface.
    
    A cell is a named container for polygons, labels, and references.
    """
    
    @abstractmethod
    def __init__(self, name: str):
        """Create a cell with the given name."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Cell name."""
        pass
    
    @name.setter
    @abstractmethod
    def name(self, value: str):
        """Set cell name."""
        pass
    
    @abstractmethod
    def add(self, element: Any) -> Any:
        """Add an element (polygon, reference, label) to the cell."""
        pass
    
    @abstractmethod
    def remove(self, element: Any):
        """Remove an element from the cell."""
        pass
    
    @abstractmethod
    def get_bounding_box(self) -> Optional[np.ndarray]:
        """Return bounding box as [[xmin, ymin], [xmax, ymax]] or None."""
        pass
    
    @abstractmethod
    def get_polygons(self, by_spec: bool = False, depth: Optional[int] = None) -> Any:
        """Get polygons, optionally organized by layer/datatype spec."""
        pass
    
    @abstractmethod
    def get_dependencies(self, recursive: bool = False) -> set:
        """Return set of cells this cell references."""
        pass
    
    @property
    @abstractmethod
    def polygons(self) -> List[Any]:
        """Return list of polygons in this cell."""
        pass
    
    @property
    @abstractmethod
    def references(self) -> List[Any]:
        """Return list of cell references in this cell."""
        pass
    
    @property
    @abstractmethod
    def labels(self) -> List[Any]:
        """Return list of labels in this cell."""
        pass


class CellReference(ABC):
    """Abstract cell reference interface.
    
    A reference instantiates a cell with position/rotation/magnification.
    """
    
    @abstractmethod
    def __init__(
        self,
        ref_cell: Cell,
        origin: Tuple[float, float] = (0, 0),
        rotation: float = 0,
        magnification: Optional[float] = None,
        x_reflection: bool = False,
    ):
        """Create a cell reference."""
        pass
    
    @property
    @abstractmethod
    def ref_cell(self) -> Cell:
        """The referenced cell."""
        pass
    
    @ref_cell.setter
    @abstractmethod
    def ref_cell(self, value: Cell):
        """Set the referenced cell."""
        pass
    
    @property
    @abstractmethod
    def origin(self) -> np.ndarray:
        """Reference origin position."""
        pass
    
    @origin.setter
    @abstractmethod
    def origin(self, value: Tuple[float, float]):
        """Set origin position."""
        pass
    
    @property
    @abstractmethod
    def rotation(self) -> float:
        """Rotation angle in degrees."""
        pass
    
    @rotation.setter
    @abstractmethod
    def rotation(self, value: float):
        """Set rotation angle."""
        pass
    
    @property
    @abstractmethod
    def magnification(self) -> Optional[float]:
        """Magnification factor."""
        pass
    
    @magnification.setter
    @abstractmethod
    def magnification(self, value: Optional[float]):
        """Set magnification."""
        pass
    
    @property
    @abstractmethod
    def x_reflection(self) -> bool:
        """Whether reference is x-reflected."""
        pass
    
    @x_reflection.setter
    @abstractmethod
    def x_reflection(self, value: bool):
        """Set x-reflection."""
        pass
    
    @abstractmethod
    def get_bounding_box(self) -> Optional[np.ndarray]:
        """Return bounding box."""
        pass
    
    @abstractmethod
    def get_polygons(self, by_spec: bool = False, depth: Optional[int] = None) -> Any:
        """Get flattened polygons from this reference."""
        pass


class CellArray(ABC):
    """Abstract cell array interface.
    
    An array of cell instances in a regular grid pattern.
    """
    
    @abstractmethod
    def __init__(
        self,
        ref_cell: Cell,
        columns: int,
        rows: int,
        spacing: Tuple[float, float],
        origin: Tuple[float, float] = (0, 0),
        rotation: float = 0,
        magnification: Optional[float] = None,
        x_reflection: bool = False,
    ):
        """Create a cell array."""
        pass
    
    @property
    @abstractmethod
    def ref_cell(self) -> Cell:
        """The referenced cell."""
        pass
    
    @property
    @abstractmethod
    def origin(self) -> np.ndarray:
        """Array origin position."""
        pass
    
    @origin.setter
    @abstractmethod
    def origin(self, value):
        """Set origin."""
        pass
    
    @property
    @abstractmethod
    def rotation(self) -> float:
        """Rotation angle in degrees."""
        pass
    
    @rotation.setter
    @abstractmethod
    def rotation(self, value: float):
        """Set rotation."""
        pass
    
    @property
    @abstractmethod
    def x_reflection(self) -> bool:
        """Whether array is x-reflected."""
        pass
    
    @x_reflection.setter
    @abstractmethod
    def x_reflection(self, value: bool):
        """Set x-reflection."""
        pass
    
    @abstractmethod
    def get_bounding_box(self) -> Optional[np.ndarray]:
        """Return bounding box."""
        pass
    
    @abstractmethod
    def get_polygons(self, by_spec: bool = False, depth: Optional[int] = None) -> Any:
        """Get flattened polygons from this array."""
        pass


class Label(ABC):
    """Abstract label interface.
    
    A text label for annotation (not rendered as geometry).
    """
    
    @abstractmethod
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
        """Create a label."""
        pass
    
    @property
    @abstractmethod
    def text(self) -> str:
        """Label text."""
        pass
    
    @property
    @abstractmethod
    def position(self) -> np.ndarray:
        """Label position."""
        pass
    
    @position.setter
    @abstractmethod
    def position(self, value):
        """Set position."""
        pass
    
    @property
    @abstractmethod
    def layer(self) -> int:
        """Label layer."""
        pass
    
    @layer.setter
    @abstractmethod
    def layer(self, value: int):
        """Set layer."""
        pass
    
    @property
    @abstractmethod
    def texttype(self) -> int:
        """Label texttype."""
        pass
    
    @texttype.setter
    @abstractmethod
    def texttype(self, value: int):
        """Set texttype."""
        pass


class Library(ABC):
    """Abstract library interface for GDS file I/O."""
    
    @abstractmethod
    def __init__(self, name: str = "library", unit: float = 1e-6, precision: float = 1e-9):
        """Create a library."""
        pass
    
    @abstractmethod
    def write_gds(self, filename: str, cells: List[Cell]) -> str:
        """Write cells to a GDS file."""
        pass
    
    @abstractmethod
    def read_gds(
        self,
        filename: str,
        cellname: Optional[str] = None,
        flatten: bool = False,
    ) -> Dict[str, Cell]:
        """Read cells from a GDS file."""
        pass
