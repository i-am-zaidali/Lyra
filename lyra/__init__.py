from models import Line, Point
from models import Triangle
    
l1 = Line(5, 7, -1)
l2 = Line(3, -2, 1)
    

def distance_bw_points(a: Point, b: Point):
    l = Line.from_AB_coordinates(a, b)
    return l.length

def find_ratio(a: Point, b: Point, c: Point):
    line = Line.from_AB_coordinates(a, b)
    return line.find_ratio_of_division_on_point(c)

def slope_from_points(a: Point, b: Point):
    return Line.from_AB_coordinates(a, b).slope

l1 = Line.from_AB_coordinates(Point(-2, 3), Point(6, -1))
l2 = Line.from_AB_coordinates(Point(4, 3), Point(0, -3))

print(l1, l2)

l3 = Line.from_AB_coordinates(l1.midpoint, l2.find_point_from_ratio((3, 4)))
print(l3)