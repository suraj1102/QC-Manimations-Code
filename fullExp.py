from manim import *
import numpy as np
import random
from typing import List
from Magnets import Magnets
import vector_helpers

class Particle:
    def __init__(self, particleRadius:float,  boundaryRadius: float, boundaryPosition: np.array) -> None:
        # Generate a random 2D vector with components in the range [-0.5, 0.5]
        random_vector = np.random.rand(2) - 0.5
        normalized_direction = random_vector / np.linalg.norm(random_vector)
        self.direction = normalized_direction
        
        self.position = boundaryPosition + (np.random.rand(2) - 0.5) * (boundaryRadius - particleRadius)
        
        self.maxSpeed = 3.5

        self.particleRadius: float = particleRadius
        self.boundaryRadius: float = boundaryRadius
        self.boundaryPosition: np.array = boundaryPosition


    def updatePosition(self, dt) -> None:
        self.position += self.direction / np.linalg.norm(self.direction) * self.maxSpeed * dt


    def handleCollisions(self, particleArray: List['Particle']) -> None:
        self.handleBoudnaryCollisions()
        self.handleParticleCollisions(particleArray=particleArray)


    def handleBoudnaryCollisions(self) -> None:
        distanceFromCenter = np.linalg.norm((self.position - self.boundaryPosition))

        if (distanceFromCenter + self.particleRadius > self.boundaryRadius):
            collisionNormal = (self.position - self.boundaryPosition) / distanceFromCenter  # Normalized vector
            self.direction = self.direction - 2 * np.dot(self.direction, collisionNormal) * collisionNormal
            self.position = self.boundaryPosition + collisionNormal * (self.boundaryRadius - self.particleRadius)
        
    
    def handleParticleCollisions(self, particleArray: List['Particle']) -> None:
        for other in particleArray:
            if other is self:
                continue

            # Calculate the distance between the particles
            distance_vector = self.position - other.position
            distance = np.linalg.norm(distance_vector)
            radius_sum = self.particleRadius + other.particleRadius

            # Check if the particles are colliding
            if distance < radius_sum:
                # Normalize the distance vector to get the collision normal
                collisionNormal = distance_vector / distance

                # Reflect the directions of both particles
                self.direction = self.direction - 2 * np.dot(self.direction, collisionNormal) * collisionNormal
                other.direction = other.direction - 2 * np.dot(other.direction, collisionNormal) * collisionNormal

                # Move the particles so they are no longer overlapping
                overlap = radius_sum - distance
                correction = collisionNormal * overlap
                
                # Split the correction based on their mass or equally
                self.position += correction / 2
                other.position -= correction / 2

                # Damping factor to prevent immediate recollision
                damping_factor = 0.8
                self.direction *= damping_factor
                other.direction *= damping_factor

    def moveAlongPath(self, pointsArray: np.array, dt) -> None:
        for point in pointsArray:
            self.moveTo(point, dt)
        

    def moveTo(self, target: np.array, dt) -> None:
        while (np.linalg.norm(self.position - target) < 0.01):
            self.direction = (target - self.position) / np.linalg.norm(target - self.position)
            self.updatePosition(dt)

        self.position = target

    def generatePath(self, xStart: float = 0, xEnd: float = 10, stepSize: int = 150) -> np.array:
        steps: int = int(np.ceil((xEnd - xStart) / stepSize))
        path = np.zeros((steps, 2))
        
        for i in range(steps):
            x: float = xStart + i * stepSize
            y: float = self.pathFunction(x)
            path[i] = np.array([x, y])

        return path

    def pathFunction(self, x: float):
        return x


class first(Scene):
    def construct(self):
        boundaryRadius = 1.75
        boundary = Circle(boundaryRadius, RED, fill_opacity=0.3).shift(LEFT * 4)
        boundaryPosition = np.array([boundary.get_x(), boundary.get_y()])
        self.add(boundary)

        magnets = Magnets().createMagnets().scale(0.65).shift(RIGHT * 1)
        self.add(magnets)

        numParticles = 5

        dots = VGroup(*[Dot().scale(1.5) for _ in range(numParticles)])
        particles = [Particle(dots[0].radius, boundaryRadius, boundaryPosition) for _ in range(numParticles)]

        shoot_button = Magnets().create_textbox(BLUE, "Shoot", YELLOW, 1, 3.5).scale(0.3).next_to(boundary, DOWN, buff=1)
        self.add(shoot_button)

        mmVector = Vector(vector_helpers.randomDirection(), color=GREEN).scale(0.6, scale_tips=True)
        mmVector.next_to(boundary, UP, buff=1)
        mmVectorLabel = Text("Spin", color=GREEN).scale(0.3).next_to(mmVector, DOWN)
        self.add(mmVector, mmVectorLabel)

        def dot_updater(dot: Mobject, dt, particle_index):
            particles[particle_index].updatePosition(dt)
            particles[particle_index].handleCollisions(particles)
            pos_x = particles[particle_index].position[0]
            pos_y = particles[particle_index].position[1]
            dot.move_to(np.array([pos_x, pos_y, 0]))


        for i, dot in enumerate(dots):
            dot.add_updater(lambda d, dt, i=i: dot_updater(d, dt, i))
            dot.update()

        self.add(dots)

        self.wait(3)

        # Move one dot along path
        for dotIndex in range(len(dots)):
            self.play(Indicate(shoot_button))
            dots[dotIndex].clear_updaters()
            self.shootDot(dots[dotIndex], particles[dotIndex], boundary)

        self.wait()


    def shootDot(self, dot: Mobject, particle: Particle, boundary: Mobject):
        pathToEdge = self.pathToEdge(dot, boundary)
        # self.add(pathToEdge)


        vectorDir = vector_helpers.randomDirection()
        quadrant = vector_helpers.findQuadtrant(vectorDir)
        up = quadrant in [0, 1]
        v = Vector(vectorDir, color=GREEN)
        v.scale(0.6, scale_tips=True)

        v.add_updater(lambda mob: mob.move_to(dot.get_center()))
        v.update()

        targetDir = UP if quadrant in [0, 1] else DOWN
        angle = vector_helpers.angle_between(targetDir, vectorDir)

        if quadrant in [1, 3]:
            angle = -angle

        path = self.generatePath(up)
        # Move the path such that the start point is at the right edge of the circle
        # I don't know why this works but it somehow does
        path.shift(RIGHT * boundary.get_edge_center(RIGHT)[0] + UP * boundary.get_edge_center(RIGHT)[1])
        path.set_stroke(opacity=0.3)

        self.play(
            MoveAlongPath(dot, pathToEdge),
            FadeIn(v),
            run_time = pathToEdge.get_arc_length() /  particle.maxSpeed,
            rate_func = rate_functions.linear
        )

        self.play(
            MoveAlongPath(dot, path),
            v.animate.rotate(angle , about_point=v.get_start()),
            run_time = path.get_arc_length() /  particle.maxSpeed,
            rate_func = rate_functions.linear,
        )

        self.play(FadeOut(v))

        
    def pathToEdge(self, dot: Mobject, boundary: Mobject):
        startPoint = dot.get_center()
        endPoint = boundary.get_center() + np.array([boundary.radius, 0, 0])
        startHandle = np.array([
            startPoint[0], 
            startPoint[1] - (startPoint[1] - endPoint[1]) / 2, 
            0])
        endHandle = np.array([
            startPoint[0] - (startPoint[0] - endPoint[0]) / 2, 
            endPoint[1], 
            0])
    
        pathToEdge = CubicBezier(startPoint, startHandle, endHandle, endPoint)
        return pathToEdge
        

    def generatePath(self, up=None):
        if up == True:
            isSpinUp = True
        elif up == False:
            isSpinUp = False
        else: 
            isSpinUp = np.random.randint(0, 2) == 0
        function = ParametricFunction(self.spinUpFunction if isSpinUp else self.spinDownFunction, t_range=[0, 7])
        return function

    def generateRandomPath(self):
        multiplier = np.random.uniform(-0.1, 0.1)
        function = ParametricFunction(lambda t: self.randomSpinFunction(t, multiplier), t_range=[0, 7])
        return function
        
    def spinUpFunction(self, t):
        return np.array([t, 0.1 * (t - 2.5) ** 2 if t > 2.5 else 0, 0])

    def spinDownFunction(self, t):
        return np.array([t, -0.1 * (t - 2.5) ** 2 if t > 2.5 else 0, 0])
    
    def randomSpinFunction(self, t, multiplier):
        return np.array([t, multiplier * (t - 2.5) ** 2 if t > 2.5 else 0, 0])