from models.line import Line, Point

class Triangle:
    """Represents a triangle in 2d space.
    
    .. note::
        This class should not be directly instantiated but instead should be created using the provided class methods.
    """
    def __init__(self, side1: Line, side2: Line, side3: Line) -> None:
        self._A = side1
        self._B = side2
        self._C = side3
        
    def __str__(self) -> str:
        return f"{self.side_A}\n{self.side_B}\n{self.side_C}"
        
    @property
    def side_A(self):
        """:class:`.Line`: The first side of the triangle from vertex B to vertex C."""
        return self._A
    
    @property
    def side_B(self):
        """:class:`.Line`: The second side of the triangle from vertex A to vertex C."""
        return self._B
    
    @property
    def side_C(self):
        """:class:`.Line`: The third side of the triangle from vertex A to vertex B."""
        return self._C
    
    @property
    def vertex_A(self):
        """:class:`.Point`: The first vertex of the triangle."""
        return self.side_A.point_A
        
    @property
    def vertex_B(self):
        """:class:`.Point`: The second vertex of the triangle."""
        return self.side_B.point_B
        
    
    @property
    def vertex_C(self):
        """:class:`.Point`: The third vertex of the triangle."""
        return self.side_C.point_A
    
    @property
    def area(self):
        A, B, C = self.vertex_A, self.vertex_B, self.vertex_C
        x1, y1 = A.x, A.y
        x2, y2 = B.x, B.y
        x3, y3 = C.x, C.y
        
        return (x1 * (y2 - y3)) - (x2 * (y1 - y3)) + (x3 * (y1 - y2))
    
    def is_isoceles(self):
        """Checks if the triangle is an isoceles triangle.

        Returns
        -------
        :class:`bool`
            A boolean indicating if the triangle is an isoceles triangle.
        """
        return any([self.angle_AB() == self.angle_BC(), self.angle_AB() == self.angle_AC(), self.angle_BC() == self.angle_AC()])
    
    def is_equilateral(self):
        """Checks if the triangle is an equilateral triangle.
        
        Returns
        -------
        :class:`bool`
            A boolean indicating if the triangle is an equilateral triangle."""
        return all([self.angle_AB() == 60, self.angle_BC() == 60, self.angle_AC() == 60])
    
    def is_right_angled(self):
        """Checks if the triangle is a right angled triangle.
        
        Returns
        -------
        :class:`bool`
            A boolean indicating if the triangle is a right angled triangle."""
        return any([self.angle_AB() == 90, self.angle_BC() == 90, self.angle_AC() == 90])
    
    def is_scalene(self):
        """Checks if the triangle is a scalene triangle.
        
        Returns
        -------
        :class:`bool`
            A boolean indicating if the triangle is a scalene triangle."""
        return not self.is_isoceles() and not self.is_equilateral() # shorter than individually checking each angle's equality
    
    def angle_AB(self):
        """Returns the angle between side A and side B

        Returns
        -------
        :class:`float`
            The angle between side A and side B in degrees.
        """
        return self.side_A.angle_with_line(self.side_B)
    
    def angle_BC(self):
        """Returns the angle between side B and side C

        Returns
        -------
        :class:`float`
            The angle between side B and side C in degrees.
        """
        return self.side_B.angle_with_line(self.side_C)
    
    def angle_AC(self):
        """Returns the angle between side A and side C

        Returns
        -------
        :class:`float`
            The angle between side A and side C in degrees.
        """
        return self.side_C.angle_with_line(self.side_A)
    
    @staticmethod
    def _verify_sides(side_a: Line, side_b: Line, side_c: Line):
        angle1 = side_a.angle_with_line(side_b)
        angle2 = side_a.angle_with_line(side_c)
        angle3 = side_b.angle_with_line(side_c)
        
        a_len = side_a.length
        b_len = side_b.length
        c_len = side_c.length
        
        return (sum([angle1, angle2, angle3]) == 180 and a_len + b_len > c_len and a_len + c_len > b_len and b_len + c_len > a_len)
    
    @classmethod
    def from_sides(cls, side_a: Line, side_b: Line, side_c: Line):
        """Creates a triangle from the three sides.

        Parameters
        ----------
        side_a : :class:`.Line`
            The first side of the triangle
        side_b : :class:`.Line`
            The second side of the triangle
        side_c : :class:`.Line`
            The third side of the triangle

        Returns
        -------
        :class:`.Triangle`
            The newly created Triangle object

        Raises
        ------
        ValueError
            If the total angle between the sides is not 180 degrees which means they are not a triangle.
        """
        if not cls._verify_sides(side_a, side_b, side_c):
            raise ValueError("Sides do not form a triangle.")
        
        return cls(side_a, side_b, side_c)
    
    @classmethod
    def from_vertices(cls, A: Point, B: Point, C: Point):# -> 'Triangle':
        """Creates a triangle from the three vertices.

        Parameters
        ----------
        A : :class:`.Point`
            The first vertex of the triangle
        B : :class:`.Point`
            The second vertex of the triangle
        C : :class:`.Point`
            The third vertex of the triangle

        Returns
        -------
        :class:`.Triangle`
            The newly created Triangle object
            
        Raises
        ------
        ValueError
            If the points do not form a proper triangle.
        """
        return cls.from_sides(Line.from_AB_coordinates(B, C), Line.from_AB_coordinates(A, C), Line.from_AB_coordinates(A, B))