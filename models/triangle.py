from models.line import Line, Point

class Triangle:
    def __init__(self, side1: Line, side2: Line, side3: Line) -> None:
        self._AB = side1
        self._BC = side2
        self._AC = side3
        
    @property
    def side_A(self):
        return self._BC
    
    @property
    def side_B(self):
        return self._AC
    
    @property
    def side_C(self):
        return self._AB
    
    @property
    def vertex_A(self):
        return self.side_B.point_A
        
    @property
    def vertex_B(self):
        return self.side_A.point_A
    
    @property
    def vertex_C(self):
        return self.side_A.point_B
    
    def is_isoceles(self):
        return any([self.angle_AB() == self.angle_BC(), self.angle_AB() == self.angle_AC(), self.angle_BC() == self.angle_AC()])
    
    def is_equilateral(self):
        return all([self.angle_AB() == 60, self.angle_BC() == 60, self.angle_AC() == 60])
    
    def is_right_angled(self):
        return any([self.angle_AB() == 90, self.angle_BC() == 90, self.angle_AC() == 90])
    
    def is_scalene(self):
        return not self.is_isoceles() and not self.is_equilateral() # shorter than individually checking each angle's equality
    
    def __str__(self) -> str:
        return f"{self.side_AB}\n{self.side_BC}\n{self.side_AC}"
    
    def angle_AB(self):
        return self.side_A.angle_with_line(self.side_B)
    
    def angle_BC(self):
        return self.side_B.angle_with_line(self.side_C)
    
    def angle_AC(self):
        return self.side_C.angle_with_line(self.side_A)
    
    @classmethod
    def from_vertices(cls, A: Point, B: Point, C: Point) -> 'Triangle':
        return cls(Line.from_AB_coordinates(A, B), Line.from_AB_coordinates(B, C), Line.from_AB_coordinates(A, C))
    
    @property
    def area(self):
        x1, y1 = self.vertex_A.x, self.vertex_A.y
        x2, y2 = self.vertex_B.x, self.vertex_B.y
        x3, y3 = self.vertex_C.x, self.vertex_C.y
        
        return (x1 * (y2 - y3)) - (y1 * (x2 - x3)) + (x2 * y3) - (x3 * y2)