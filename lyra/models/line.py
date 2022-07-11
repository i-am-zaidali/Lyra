from models.infinity import INFINITY
from models.point import Point
import math
from typing import Literal, Optional, Tuple, Union, Generator
from fractions import Fraction
import logging

log = logging.getLogger(__name__)

# if you see some weirdly done calcualtions, it's probably because i dont wanna be dealing with floats
# so im trying my best to make it work with ints

class Line:
    """A dataclass representing a line in a 2D plane.
    This class is based on the general equation of line:
        `ax + by + c = 0`
    
    .. note::
        This class should not be manually instantiated. 
        Instead, use the provided class methods to create a new Line object.
    
    .. container:: operations

        .. describe:: str(x)

            Returns the general equaion form of the line.

        .. describe:: x == y

            Checks if the line is equal to another line.

        .. describe:: x != y

            Checks if the line is not equal to another line.
            
        .. describe:: x + y

            Adds the coefficients of the two lines.
            
        .. describe:: x - y

            Subtracts the coefficients of the two lines.
    """
    
    # below variables are defined to just typehint, they get set in any of the classmethods avalable
    # incase the classmethods are not called, these won't be set and cause errors in most of the 
    # methods and proeprties of the class.
    _rng : bool
    _A : Point
    _B : Point
    
    def __init__(self, x_coefficient: Union[int, float], y_coefficient: Union[int, float], constant: Union[int, float]):
        self._x = x_coefficient
        self._y = y_coefficient
        self._c = constant
        
    def __str__(self) -> str:
        x, y, c = self.x_coefficient, self.y_coefficient, self.constant
        x = f"{x:+}x " if x > 1 or y < -1 else 'x ' if y == 1 else "-x " if x != 0 else ""
        y = f"{y:=+{len(str(y)) + (1 if y < 0 else 2)}}y " if y > 1 or y < -1 else '+ y ' if y == 1 else "- y " if y != 0 else ""
        c = f"{c:=+{len(str(c)) + (1 if c < 0 else 2)}} " if c != 0 else ""
        return f"{x}{y}{c}= 0"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        
        return all(getattr(self, attr) == getattr(other, attr) for attr in ["slope", "y_intercept", "x_intercept"])
    
    def __add__(self, other: object):
        if not isinstance(other, Line):
            return NotImplemented
        
        x, y, c = self.x_coefficient + other.x_coefficient, self.y_coefficient + other.y_coefficient, self.constant + other.constant
        return self.from_coefficients(x, y, c)
    
    def __sub__(self, other: object):
        if not isinstance(other, Line):
            return NotImplemented
        
        x, y, c = self.x_coefficient - other.x_coefficient, self.y_coefficient - other.y_coefficient, self.constant - other.constant
        return self.from_coefficients(x, y, c)
    
    @property
    def x_coefficient(self):
        """Union[:class:`int`, :class:`float`]: The coefficient of x of the line's equation."""
        return self._x
    
    @property
    def y_coefficient(self):
        """Union[:class:`int`, :class:`float`]: The coefficient of y of the line's equation."""
        return self._y
    
    @property
    def constant(self):
        """Union[:class:`int`, :class:`float`]: The constant of the line's equation."""
        return self._c
    
    @property
    def point_A(self) -> Point:
        """:class:`.Point`: Point A on the line. 
        
        This is automatically generated if not passed in the `Line.from_AB_coordinates` or `Line.from_coefficients` class method.
        """
        return self._A
    
    @property
    def point_B(self) -> Point:
        """:class:`.Point`: Point B on the line. 
        
        This is automatically generated if not passed in the `Line.from_AB_coordinates` or `Line.from_coefficients` class method.
        """
        return self._B
    
    @property
    def slope(self):
        """:class:`float`: The slope of the line.
        
        Returns a special `.INFINITY` object (subclass of float) if the line is vertical (AKA `Line.y_coefficient` is 0).
        """
        if self._rng:
            try:
                slope = -self.x_coefficient / self.y_coefficient
            except ZeroDivisionError: # incase the line is vertical, when slope is infinity
                slope = INFINITY
            
        else:
            slope = (self.point_B.y - self.point_A.y) / (self.point_B.x - self.point_A.x)
        
        return slope
    
    @property
    def x_intercept(self):
        """:class:`.Point`: The coordiantes of the x-intercept of the line."""
        try:
            return Point(-self.constant / self.x_coefficient, 0)
        except ZeroDivisionError:
            return Point(INFINITY, 0)
    
    @property
    def y_intercept(self):
        """:class:`.Point`: The coordiantes of the y-intercept of the line."""
        try:
            return Point(0, -(self.constant / self.y_coefficient))
        except ZeroDivisionError:
            return Point(0, INFINITY)
    
    @property
    def length(self):
        """:class:`float`: The length of the line from point A to point B."""
        return math.sqrt(((self.point_B.x - self.point_A.x)**2) + ((self.point_B.y - self.point_A.y)**2))
    
    @property
    def midpoint(self):
        """:class:`.Point`: The midpoint of the lne from point A to point B."""
        return Point((self.point_A.x + self.point_B.x)/2, (self.point_A.y+self.point_B.y)/2)
    
    @property
    def equation(self):
        """:class:`str`: The general equation of the line."""
        return self.__str__()
    
    @classmethod
    def from_intercepts(cls, x_intercept: Point, y_intercept: Point) -> "Line":
        """Create a line object from the x-intercept and y-intercept of the line.

        Parameters
        ----------
        x_intercept : :class:`.Point`
            the intercept of the line on the x-axis
        y_intercept : :class:`.Point`
            the intercept of the line on the y-axis

        Returns
        -------
        :class:`.Line`
            The newly created line object
        """
        intercepts_prod = x_intercept.x * y_intercept.y
        x_coeff = y_intercept.y
        y_coeff = x_intercept.x
        
        # using the two intercepts formula: x/a + y/b = 1
        # where a = x_intercept and b = y_intercept
        
        return cls.from_coefficients(x_coeff, y_coeff, -intercepts_prod, x_intercept, y_intercept)
    
    @classmethod
    def from_AB_coordinates(cls, point_A: Point, point_B: Point, /) -> 'Line':
        """Create a line from two points present on the line which will be it's start and end point

        Parameters
        ----------
        point_A : :class:`.Point`
            A point present on the line from which it starts.
        point_B : :class:`.Point`
            A point present on the line where it ends

        Returns
        -------
        :class:`.Line`
            The newly created line object
        """
        slope = (point_B.y - point_A.y) / (point_B.x - point_A.x)
        
        self = cls.from_slope_and_point(slope, point_A)
        self._rng = False
        self._B = point_B
        
        return self
    
    @classmethod
    def from_slope_and_point(cls, slope: Union[float, int], point: Point) -> 'Line':
        """Create a line from it's slope and a point on the line.

        Parameters
        ----------
        slope : Union[:class:`float`, :class:`int`]
            The slope of the line.
        point : :class:`.Point`
            A point present on the line.

        Returns
        -------
        :class:`.Line`
            The newly created line object
        """
        # the below might be confusing but to put it in simple words
        # I'm trying to keep integers in the equation only isntead of floats.
        # so the following just uses the integer ratio of the floats
        # and finds the lcm to use as the y value
        
        # for example: let p/q be the slope of the line (m)
        # and r/s be the y-intercent (b) where q and s can be equal to 1
        
        # thus the equation `y = mx + b` becomes:
        # `(q*s)y = (p*s)x + (q*r)b` ( can be written as `(p*s)x - (q*s)y + (q*r)b = 0`)
        # this partially ensures that we only have integer values available and not floats.
        
        p, q = Fraction(slope).limit_denominator(1000).as_integer_ratio() if isinstance(slope, float) else (slope, 1)
        # to limit the emission of huge af integers that just don't make sense.
        r, s = Fraction((point.y - (slope * point.x))).limit_denominator(1000).as_integer_ratio()
        
        x = p * s
        y = -(q*s)
        c = q*r
        
        return cls.from_coefficients(x, y, c, point)
    
    @classmethod
    def from_coefficients(cls, x_coefficient: Union[int, float], y_coefficient: Union[int, float], constant: Union[int, float], point_A: Optional[Point] = None, point_B: Optional[Point] = None):
        """Create a new line from the coefficients of it's equation. Optionally a start and end point can also be passed in.

        Parameters
        ----------
        x_coefficient : Union[:class:`int`, :class:`float`]
            The coefficient of x of the line's equation.
        y_coefficient : Union[:class:`int`, :class:`float`]
            The coefficient of y of the line's equation.
        constant : Union[:class:`int`, :class:`float`]
            The constant of the line's equation.
        point_A : Optional[:class:`.Point`]
            A point present on the line from which it starts.
        point_B : Optional[:class:`.Point`]
            A point present on the line where it ends.

        Raises
        ------
        ValueError
            If all coefficients provided are equal to zero.
        """
        if all(v == 0 for v in [x_coefficient, y_coefficient, constant]):
            raise ValueError("Cannot create line with all values equal to 0.")
        
        self = cls(x_coefficient, y_coefficient, constant)
        
        if not point_A or not point_B:
            self._rng = True
            if self.x_coefficient == 0:
                self._A = point_A or Point(0, -self.constant)
                self._B = point_B or Point(0, 0)
                
            elif self.y_coefficient == 0:
                self._A = point_A or Point(-self.constant, 0)
                self._B = point_B or Point(0, 0)
                
            else:
                gen = self.points_on_line()
                self._A = point_A or next(gen)
                self._B = point_B or next(gen)
                gen.close()
                
        else:
            self._A = point_A
            self._B = point_B
            
        return self
    
    
    
    def angle_with_line(self, line: "Line"):
        """Returns the angle between the two lines.

        Parameters
        ----------
        line : :class:`.Line`
            The line to find the angle with.

        Returns
        -------
        :class:`float`
            The angle in degrees between the lines.
        """
        
        if self.is_parallel_to(line):
            return 0
        
        elif self.is_perpendicular_to(line):
            return 90
        
        # eliminating known cases pre calculation
        
        slope_prod = self.slope * line.slope
        slope_diff = self.slope - line.slope
        try:
            val = slope_diff/(1+slope_prod)
        except ZeroDivisionError:
            val = INFINITY
            
        angle = abs(math.degrees(math.atan(val)))
        
        return angle
        # abs since angles are supposed to be positive and math.atan only return between pi/2 and -pi/2
        # thus abs()-ing the result allows us to get accurate angles
    
    def points_on_line(self, range_: int = 100):
        """Returns a Generator yielding points that are present on the line.
        
        .. note::
            This method only returns absolute points on the line.
            Which means that the coordinates will only be integers and not floats.
            This can result in 0 results somethings since a line can only contain partial points sometimes.

        Parameters
        ----------
        range_ : :class:`int`
            An optional range int to check upto for points, by default 100

        Returns
        -------
        :class:`Generator`
            a Generator object yielding :class:`.Point` objects.
        """
        r = range_ or 100
        return (p for i in range(r) if self.contains_point((p:=Point(i, (0 if self.slope is INFINITY else (self.slope*i + self.y_intercept.y))))))
        
    
    def find_point_from_ratio(self, ratio: Tuple[int, int], in_or_ex: Literal["internally", "externally"] = "internally"):
        """Returns a point that divides the line in the given ratio.

        Parameters
        ----------
        ratio : Tuple[:class:`int`, :class:`int`]
            the ratio in which the line is divided at that point.
        in_or_ex : Literal[&quot;internally&quot;, &quot;externally&quot;]
            Whether the point is on the line or not.

        Returns
        -------
        :class:`.Point`
            The point that divides the line.
        """
        # the excessive variables are here to improve theoretical reading for both me and whoever decides to read this code.
        m1 = ratio[0]
        m2 = ratio[1]
        x1 = self.point_A.x
        x2 = self.point_B.x
        y1 = self.point_A.y
        y2 = self.point_B.y
        if in_or_ex == "internally":
            x = ((m1*x2) + (m2*x1)) / (m1 + m2)
            y = ((m1*y2) + (m2*y1)) / (m1 + m2)
            point = Point(x, y)
            if self.contains_point(point): # just a safety check
                return Point(x, y)
        
        x = ((m1*x2) - (m2*x1)) / (m1 - m2)
        y = ((m1*y2) - (m2*y1)) / (m1 - m2)
        return Point(x, y)

    def find_ratio_of_division_on_point(self, point: Point):
        """Opposite of `Line.find_point_from_ratio`. This returns the ratio a point divides the line in.

        Parameters
        ----------
        point : :class:`Point`
            The point that divides the line.

        Returns
        -------
        Tuple[:class:`int`, :class:`int`]
            the ratio in which the line is divided.
        """
        a = self.point_A
        b = self.point_B
        c = point
        
        if self.contains_point(c):
            ratio = ((c.x - a.x) / (b.x - c.x))
            return Fraction(ratio).limit_denominator(1000).as_integer_ratio()
            
        else:
            ratio = ((a.x + c.x) / (c.x + b.x))
            return Fraction(ratio).limit_denominator(1000).as_integer_ratio()
    
    def is_parallel_to(self, line: "Line"):
        """Checks if the line is parallel to another line

        Parameters
        ----------
        line : :class:`Line`
            The line to check

        Returns
        -------
        :class:`bool`
            A boolean value indicating whether the lines are parallel or not
        """
        return (self.slope == line.slope and self.angle_with_line(line) == 0)
    
    def is_perpendicular_to(self, line: "Line"):
        """Checks if the line is perpendicular to another line

        Parameters
        ----------
        line : :class`Line`
            The line to check

        Returns
        -------
        :class:`bool`
            A boolean value indicating whether the lines are parallel or not
        """
        return self.slope == (-1/line.slope)
    
    def intersects_with_line_on_point(self, line: "Line"):
        """Get the point at which the line intersects with another line

        Parameters
        ----------
        line : :class:`Line`
            The line that intersects

        Returns
        -------
        Optional[:class:`.Point`]
            A :class:`.Point` object representing the coordinates at which the lines intersect or None if they are parallel. 
        """
        if self.is_parallel_to(line):
            return None
        
        a1 = self.x_coefficient
        a2 = line.x_coefficient
        
        b1 = self.y_coefficient
        b2 = line.y_coefficient
        
        c1 = self.constant
        c2 = line.constant
        
        x = (((b1*c2) - (b2*c1))/((a1*b2) - (a2*b1)))
        y = (((c1*a2) - (c2*a1))/((a1*b2) - (a2*b1)))
        
        x = int(x) if x.is_integer() else x
        y = int(y) if y.is_integer() else y
        
        return Point(x, y)
    
    def contains_point(self, Point: Point):
        """Check whether the line contains the given point.

        Parameters
        ----------
        Point : :class:`Point`
            The point to check

        Returns
        -------
        :class:`bool`
            A boolean value indicating whether the point is present on the line or not.
        """
        return ((self.x_coefficient * Point.x) + (self.y_coefficient * Point.y) + (self.constant)) == 0