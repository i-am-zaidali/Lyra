from models.point import Point
from models.line import Line

class _GeometricalShapeWithVertices:
    """A placeholder class representing a geometrical shape that has corners/vertices and sides.
    
    This is subclassed by models such as Triangle and Parallelogram.
    """
    def __new__(cls, *args, **kwargs):
        raise ValueError(f"{cls.__name__} can not be instantiated manually. Use the provided classmethods to create a proepr instance")
    
    @staticmethod
    def _verify_sides(*args: Line, **kwargs):
        return NotImplemented
    
    @classmethod
    def from_vertices(cls, *args: Point, **kwargs):
        return NotImplemented
    
    @classmethod
    def from_sides(cls, *args: Line, **kwargs):
        return NotImplemented