import math
from dataclasses import dataclass
from typing import Literal, Optional, Tuple, Union

@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]
    
class Line:
    def __init__(self, x_coefficient: Union[int, float], y_coefficient: Union[int, float], constant: Union[int, float]):
        self._x = x_coefficient
        self._y = y_coefficient
        self._c = constant
        
    def __str__(self) -> str:
        x = f"{self.x_coefficient:+}x " if self.x_coefficient > 1 else 'x ' if self.x_coefficient != 0 else ""
        y = f"{self.y_coefficient:=+3d}y "  if self.x_coefficient > 1 else 'x ' if self.y_coefficient != 0 else ""
        c = f"{self.constant:=+4d} " if self.constant != 0 else ""
        return f"{x}{y}{c}= 0"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def x_coefficient(self):
        return self._x
    
    @property
    def y_coefficient(self):
        return self._y
    
    @property
    def constant(self):
        return self._c
    
    @property
    def point_A(self) -> Point:
        return self._A
    
    @property
    def point_B(self) -> Point:
        return self._B
    
    @property
    def slope(self):
        try:
            return -self.x_coefficient / self.y_coefficient
        except ZeroDivisionError: # incase the line is vertical, when slope is infinity
            return math.inf 
    
    @property
    def x_intercept(self):
        try:
            return Point(-self.constant / self.x_coefficient, 0)
        except ZeroDivisionError:
            return Point(0, 0)
    
    @property
    def y_intercept(self):
        try:
            return Point(0, -self.constant / self.y_coefficient)
        except ZeroDivisionError: # when line is present on x-axis, where y-intercept would be 0
            return Point(0, 0)
    
    @property
    def length(self):
        return math.sqrt(((self.point_B.x - self.point_A.x)**2) + ((self.point_B.y - self.point_A.y)**2))
    
    @property
    def midpoint(self):
        return Point((self.point_A.x + self.point_B.x)/2, (self.point_A.y+self.point_B.y)/2)
    
    @property
    def equation(self):
        return self.__str__()
    
    @classmethod
    def from_AB_coordinates(cls, A_coords: Point, B_coords: Point, /) -> 'Line':
        slope = (B_coords.y - A_coords.y) / (B_coords.x - A_coords.x)
        
        x_coeff = int(slope)
        y_coeff = -1
        
        constant = -(slope * A_coords.x) + A_coords.y
        
        return cls(x_coeff, y_coeff, constant, A_coords, B_coords)
    
    @classmethod
    def from_slope_and_point(cls, point: Point, slope: float):
        x = slope
        y = -1
        c = -(slope*point.x) + point.y
        return cls(x, y, c )
    
    @classmethod
    def from_coefficients(cls, x_coefficient: int, y_coefficient: int, constant: int, point_A: Optional[Point] = None, point_B: Optional[Point] = None):
        if all(v == 0 for v in [x_coefficient, y_coefficient, constant]):
            raise ValueError("Cannot create line with all values equal to 0.")
        
        self = cls(x_coefficient, y_coefficient, constant)
        
        if not point_A or not point_B:
            if self.x_coefficient == 0:
                self._A = Point(0, -self.constant)
                self._B = Point(0, 0)
                
            elif self.y_coefficient == 0:
                self._A = Point(-self.constant, 0)
                self._B = Point(0, 0)
                
        else:
            gen = self.points_on_line()
            self._A = point_A or next(gen)
            self._B = point_B or next(gen)
            gen.close()
    
    def angle_with_line(self, line: "Line"):
        return math.degrees(math.atan((self.slope - line.slope)/(1+self.slope*line.slope)))
    
    def points_on_line(self, range_: Optional[int] = None):
        r = range_ or 100
        return (p for i in range(r) if ((y:=0) if self.slope is math.inf else (y:=self.slope*i + self.y_intercept.y).is_integer()) and self.contains_point((p:=Point(i, int(y)))))
    
    def find_point_from_ratio(self, ratio: Tuple[int, int], i_or_ex: Literal["internally", "externally"] = "internally"):
        m1 = ratio[0]
        m2 = ratio[1]
        x1 = self.point_A.x
        x2 = self.point_B.x
        y1 = self.point_A.y
        y2 = self.point_B.y
        if i_or_ex == "internally":
            x = ((m1*x2) + (m2*x1)) / (m1 + m2)
            y = ((m1*y2) + (m2*y1)) / (m1 + m2)
            return Point(x, y)
        
        else:
            x = ((m1*x2) - (m2*x1)) / (m1 - m2)
            y = ((m1*y2) - (m2*y1)) / (m1 - m2)
            return Point(x, y)

    def find_ratio_of_division_on_point(self, point: Point, point_A: Optional[Point] = None, point_B: Optional[Point] = None):
        if (point_A and point_B) and not all(self.contains_point(p) for p in [point_A, point_B]):
            raise ValueError("Given start and end points are not present on line.")
        
        a = point_A or self.point_A
        b = point_B or self.point_B
        c = point
        
        if self.contains_point(c):
            ratio = ((c.x - a.x) / (b.x - c.x))
            return ratio.as_integer_ratio()
            
        else:
            ratio = ((a.x + c.x) / (c.x + b.x))
            return ratio.as_integer_ratio()
    
    def is_parallel_to(self, line: "Line"):
        return self.slope == line.slope
    
    def is_perpendicular_to(self, line: "Line"):
        return self.slope == (-1/line.slope)
    
    def intersects_with_line_on_point(self, line: "Line"):
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
        return ((self.x_coefficient * Point.x) + (self.y_coefficient * Point.y) + (self.constant)) == 0