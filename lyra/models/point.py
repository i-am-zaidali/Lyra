from dataclasses import dataclass
from typing import Union

@dataclass
class Point:
    """A dataclass representing Cartesian Coordinates in a 2D plane.
    
    .. container:: operations
    
        .. describe:: str(x)
    
            Returns the coordinates as a string.
    
        .. describe:: x == y
    
            Checks if the point is equal to another point.
    
        .. describe:: x != y
    
            Checks if the point is not equal to another point.
            
        .. describe:: x + y

            Adds the abscissa and ordinate of two points.
            
        .. describe:: x - y

            Subtracts the abscissa and ordinate of two points.
    
    Attributes
    ----------
    
    x: Union[:class:`int`, :class:`float`]
        The x-coordinate of the point. Also known as the horizontal coordinate or the abscissa.
        
    y: Union[:class:`int`, :class:`float`]
        The y-coordinate of the point. Also known as the vertical coordinate or the ordinate.
    """
    x: Union[int, float]
    y: Union[int, float]
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __add__(self, other: object):
        if not isinstance(other, Point):
            return NotImplemented
        
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: object):
        if not isinstance(other, Point):
            return NotImplemented
        
        return Point(self.x - other.x, self.y - other.y)
    
    @classmethod
    def origin(cls) -> 'Point':
        """Returns a new Point object representing the origin of a 2d space (0, 0).
        
        Returns
        -------
        :class:`.Point`
            A new Point object.
        """
        return cls(0, 0)
    
    @classmethod
    def y_intercept(cls, value: Union[int, float]) -> "Point":
        """Returns a new Point object representing the y-intercept of a line.
        
        Parameters
        ----------
        value: Union[:class:`int`, :class:`float`]
            The y-intercept of the line.
        
        Returns
        -------
        :class:`.Point`
            A new Point object.
        """
        return cls(0, value)
    
    @classmethod
    def x_intercept(cls, value: Union[int, float]) -> "Point":
        """Returns a new Point object representing the x-intercept of a line.
        
        Parameters
        ----------
        value: Union[:class:`int`, :class:`float`]
            The x-intercept of the line.
        
        Returns
        -------
        :class:`.Point`
            A new Point object.
        """
        return cls(value, 0)
    