from manim import *
import numpy as np
from typing import List


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
        boundary = Circle(2, RED, fill_opacity=0.3).shift(LEFT * 3)
        boundaryRadius = boundary.radius
        boundaryPosition = np.array([boundary.get_x(), boundary.get_y()])
        self.add(boundary)

        numParticles = 5

        dots = VGroup(*[Dot().scale(1.2) for _ in range(numParticles)])
        particles = [Particle(dots[0].radius, boundaryRadius, boundaryPosition) for _ in range(numParticles)]

        path = particles[0].generatePath(0, 5)

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
        dotIndex = 0
        dots[dotIndex].clear_updaters()

        startPoint = dots[dotIndex].get_center()
        endPoint = boundary.get_center() + np.array([boundaryRadius, 0, 0])
        startHandle = np.array([
            startPoint[0], 
            startPoint[1] - (startPoint[1] - endPoint[1]) / 2, 
            0])
        endHandle = np.array([
            startPoint[0] - (startPoint[0] - endPoint[0]) / 2, 
            endPoint[1], 
            0])
        
        
        pathToEdge = CubicBezier(startPoint, startHandle, endHandle, endPoint)
        # self.add(pathToEdge)
        self.play(
            MoveAlongPath(dots[dotIndex], pathToEdge),
            run_time = pathToEdge.get_arc_length() /  particles[dotIndex].maxSpeed,
            rate_func = rate_functions.linear
        )

        isSpinUp = np.random.randint(0, 2) == 0
        function = ParametricFunction(self.spinUpFunction if isSpinUp  else self.spinDownFunction, t_range=[0, 5.5])
        if isSpinUp:
            function.move_to(boundary.get_edge_center(RIGHT) + np.array([boundaryRadius, function.height / 2, 0]))
        else:
            function.move_to(boundary.get_edge_center(RIGHT) + np.array([boundaryRadius, -function.height / 2, 0]))
        self.add(function)

        self.play(
            MoveAlongPath(dots[dotIndex], function),
            run_time = function.get_arc_length() /  particles[dotIndex].maxSpeed,
            rate_func = rate_functions.ease_out_sine
        )

        self.wait(10)
        
    def spinUpFunction(self, t):
        return np.array([t, 0.2 * (t - 2) ** 2 if t > 2 else 0, 0])

    def spinDownFunction(self, t):
        return np.array([t, -0.2 * (t - 2) ** 2 if t > 2 else 0, 0])