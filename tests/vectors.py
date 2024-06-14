from manim import *
import random
import math
import numpy as np

"""
Script to test 
1. Drawing and animating vectors
2. Rotating vectors 
3. Manim Animation Transformations
"""

class vectors(Scene):
    def construct(self):
        v = self.randomDirection()
        vector = Vector(v)
        self.add(vector)

        self.add(Circle(1))
        func = FunctionGraph(lambda t: 0 * t + 0)
        self.add(func)

        quadrant = self.findQuadtrant(v)
        targetDir = UP if quadrant in [0, 1] else DOWN
        angle = self.angle_between(targetDir, v)

        if quadrant in [1, 3]:
            angle = -angle
        
        self.play(Rotate(vector, angle , about_point=vector.get_start()))
        
    


    def findQuadtrant(self, directionVector: np.array, xOffset:float = 0, yOffset: float = 0):
        # Checks if vector is pointing up or down
        # refer to https://math.stackexchange.com/questions/324589/detecting-whether-a-point-is-above-or-below-a-slope
        isUp = directionVector[1] > yOffset
        isRight = directionVector[0] > xOffset
        
        if (isUp and isRight):
            return 0
        elif (isUp and not isRight):
            return 1
        elif (not isUp and not isRight):
            return 2
        else:
            return 3

    def randomDirection(self):
        r = 1
        t = random.random()
        u = random.random()
        x = r * math.sqrt(t) * math.cos(2 * math.pi * u)
        y = r * math.sqrt(t) * math.sin(2 * math.pi * u)

        v1 = np.array([x, y, 0]) / np.linalg.norm([x, y, 0])
        return v1
    
    def angle_between(self, v1: np.array, v2: np.array):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::
                >>> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >>> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >>> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """

        def unit_vector(vector):
            """ Returns the unit vector of the vector.  """
            return vector / np.linalg.norm(vector)

        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    