from models.line import Line, Point
    
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