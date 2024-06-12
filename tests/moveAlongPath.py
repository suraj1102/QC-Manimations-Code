from manim import * 

class Move(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 0.3],
            y_range=[-3, 3, 0.3]
        ).shift(UP * 3)

        function = axes.plot(lambda x: 0.5 * (x - 1) * (x - 1) if x > 1 else 0)

        dot = Dot(color=YELLOW).scale(1.5)

        self.add(function, dot)

        self.play(
            MoveAlongPath(dot, function),
            run_time = 3,
            rate_func = smooth
        )

class MovingFunction(Scene):
    def construct(self):
        function = ParametricFunction(self.sampleFunction, t_range=[0, 4])

        func_center = Dot(color=YELLOW).add_updater(lambda mob: mob.move_to(function.get_center()))
        func_center.update()

        surr_rect = SurroundingRectangle(function)

        self.add(function, func_center, surr_rect)

        


    def sampleFunction(self, t):
        return np.array([t, 0.2 * (t - 1) ** 2 if t > 1 else 0, 0])