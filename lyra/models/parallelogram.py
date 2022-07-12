from models.point import Point
from models.line import Line
from models._base_shape import _GeometricalShapeWithVertices

class Parallelogram(_GeometricalShapeWithVertices):

    #                               1
    #                   A      (side AB)       B
    #                    ____________________
    #                   /                   /
    #        2         /                   /      4
    #    (side AC)    /                   /   (side BD)
    #                /                   /
    #               ---------------------
    #              C     (side CD)       D
    #                        3

    def __init__(self, side_1: Line, side_2: Line, side_3: Line, side_4: Line) -> None:
        self._AB = side_1
        self._AC = side_2
        self._CD = side_3
        self._BD = side_4
        
    @staticmethod
    def _verify_sides():
        pass
        
    @classmethod
    def from_vertices(cls, point_A: Point, point_B: Point, point_C: Point, point_D: Point):
        side_1 = Line.from_AB_coordinates(point_B, point_A)
        side_2 = Line.from_AB_coordinates(point_A, point_C)
        side_3 = Line.from_AB_coordinates(point_C, point_D)
        side_4 = Line.from_AB_coordinates(point_D, point_B)
        
        return cls.from_sides(side_1, side_2, side_3, side_4)
        
    @classmethod
    def from_sides(cls, AB: Line, AC: Line, CD: Line, BD: Line):
        pass