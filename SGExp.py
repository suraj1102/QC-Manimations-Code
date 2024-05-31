from manim import *
from manim.animation.animation import Animation
from manim_cad_drawing_utils import *
import numpy as np

class Particle:
    def __init__(self, oven: Circle, color) -> None:
        self.oven = oven
        self.random_gen = np.random.default_rng()  # Create a unique random generator for each particle
        self.old_position = self.generate_position()
        self.new_position = self.generate_position()
        self.dot = Dot(color=color).scale(0.4)
        self.dot.move_to(self.old_position)
        self.transition_time = 2  # Time to move from old_position to new_position
        self.time_elapsed = 0
        self.random_gen = np.random.default_rng()  # Create a unique random generator for each particle

    def generate_position(self) -> np.array:
        oven = self.oven
        xpos = self.random_gen.uniform(-oven.radius, oven.radius)
        ypos = self.random_gen.uniform(-oven.radius, oven.radius)

        while(xpos * xpos + ypos * ypos >= oven.radius * oven.radius):
            xpos = self.random_gen.uniform(-oven.radius, oven.radius)
            ypos = self.random_gen.uniform(-oven.radius, oven.radius)

        return np.array([xpos, ypos, 0]) + oven.get_center()

    def update_position(self, dt):
        self.time_elapsed += dt
        alpha = min(self.time_elapsed / self.transition_time, 1)
        new_pos = interpolate(self.old_position, self.new_position, alpha)
        if alpha >= 1:
            self.old_position = self.new_position
            self.new_position = self.generate_position()
            self.time_elapsed = 0
        return new_pos

class Oven(Scene):
    def construct(self):
        oven = Circle(radius=1, color=RED, fill_opacity=0.2)
        oven_label = Text("Oven", color=RED).scale(0.8)
        oven_label.add_updater(lambda mob: mob.next_to(oven, DOWN))
        oven_label.update()

        oven_group = VGroup(oven, oven_label)
        self.add(oven_group)

        particles = VGroup()
        for _ in range(10):
            p = Particle(oven, LIGHT_GRAY)

            def particle_updater(mob: Mobject, dt):
                new_position = p.update_position(dt)
                mob.move_to(new_position)

            p.dot.add_updater(particle_updater)
            p.dot.update()
            particles.add(p.dot)

        self.add(particles)
        self.wait(5, frozen_frame=False)

def create_textbox(color, string, string_color, height=1, width=2):
    result = VGroup() # create a VGroup
    box = Rectangle(  # create a box
        height=height, width=width, fill_color=color, 
        fill_opacity=0.2, stroke_color=color
    )
    text = MathTex(string, color=string_color).scale(0.7).move_to(box.get_center()) # create text
    result.add(box, text) # add both objects to the VGroup
    return result

class quantizedMM(Scene):
    def construct(self):
        # create text box
        oven = create_textbox(color=RED, string="Oven", string_color=WHITE)

        SGz = create_textbox(color=BLUE, string=r"SG\hat{z}", string_color=YELLOW).shift(LEFT * 1)


        boxes = VGroup(oven, SGz).arrange(RIGHT, buff=2).to_edge(LEFT, buff=1.5)

        for mob in boxes:
            self.play(DrawBorderThenFill(mob))

        silver_beam = Line(oven.get_right(), SGz.get_left(), color=WHITE)
        silver_atoms = Text("Silver Atoms", color=LIGHT_GRAY).scale(0.3).next_to(silver_beam, DOWN, buff=0.2)
        self.play(Create(silver_beam), Write(silver_atoms))

        spin_line_offset = 0.3
        sz_up_line = Line(SGz.get_right() + [0, spin_line_offset, 0], (SGz.get_right() + [0, spin_line_offset, 0]) + [4, 0, 0])
        sz_down_line = Line(SGz.get_right() + [0, -spin_line_offset, 0], (SGz.get_right() + [0, -spin_line_offset, 0]) + [4, 0, 0])

        self.play(
            Create(sz_up_line),
            Create(sz_down_line)
        )

        sz_up_text = MathTex(r"S_z+ component", substrings_to_isolate=["+", "z"], color=WHITE).scale(0.5).next_to(sz_up_line, UP)
        sz_down_text = MathTex(r"S_z- component", substrings_to_isolate=["-", "z"], color=WHITE).scale(0.5).next_to(sz_down_line, DOWN)
        sz_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("z", YELLOW)
        sz_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("z", YELLOW)

        self.play(
            Create(sz_up_text),
            Create(sz_down_text)
        )


        # Create a tall rectangle
        screen = Rectangle(height=3, width=1, color=DARK_GRAY, fill_opacity=0.5).align_to(sz_up_line.get_end(), RIGHT + [1, 0, 0]).shift(RIGHT)
        
        # Create the label "screen" and position it below the rectangle
        screen_label = Text("Screen", color=WHITE).scale(0.4).next_to(screen, DOWN)

        # Draw the rectangle and label on the screen
        self.play(DrawBorderThenFill(screen), Write(screen_label))

        # Adjust the appearance to illustrate upspin and downspin
        upspin_rect = Rectangle(height=0.1, width=1, color=BLUE, fill_opacity=0.5).next_to(sz_up_line.get_end(), RIGHT, buff=0)
        downspin_rect = Rectangle(height=0.1, width=1, color=TEAL, fill_opacity=0.5).next_to(sz_down_line.get_end(), RIGHT, buff=0)

        spin_up_text = Text("spin up", color=BLUE).scale(0.3).next_to(upspin_rect, UP, buff=0.1)
        spin_down_text = Text("spin down", color=TEAL).scale(0.3).next_to(downspin_rect, DOWN, buff=0.1)

        # Draw the upspin and downspin parts of the rectangle
        self.play(FadeIn(upspin_rect), FadeIn(downspin_rect), FadeIn(spin_up_text), FadeIn(spin_down_text))
        self.wait()

        all_mobs = VGroup()
        for mob in self.mobjects:
            if isinstance(mob, VMobject):
                all_mobs.add(mob)
        self.play(all_mobs.animate.shift(UP * 2))

        self.wait()

        """
        EXPLAINATION - Formalizing the observations
        """

        # Paragraph text
        text1 = Paragraph("The spin magnetic moment of \nthe electron is quantized.").scale(0.5).shift(DOWN + LEFT * 2)
        self.play(FadeIn(text1))

        # Sup and sup_text
        sup = MathTex(r"|z,+\rangle", substrings_to_isolate=["z"], color=BLUE).move_to(text1.get_center() + [5, 1, 0])
        sup.set_color_by_tex("z", YELLOW)
        sup_text = Text("spin up", color=BLUE).scale(0.3).next_to(sup, DOWN, buff=0.1)
        up = VGroup(sup, sup_text)

        # Sdown and sdown_text
        sdown = MathTex(r"|z,-\rangle", substrings_to_isolate=["z"], color=TEAL).move_to(text1.get_center() + [5, -1, 0])
        sdown.set_color_by_tex("z", YELLOW)
        sdown_text = Text("spin down", color=TEAL).scale(0.3).next_to(sdown, DOWN, buff=0.1)
        down = VGroup(sdown, sdown_text)

        # Arrows
        arr1 = Arrow(text1.get_right(), up.get_left(), stroke_width=2, max_tip_length_to_length_ratio=0.1)
        arr2 = Arrow(text1.get_right(), down.get_left(), stroke_width=2, max_tip_length_to_length_ratio=0.1)

        # Play animations
        self.play(
            DrawBorderThenFill(arr1),
            DrawBorderThenFill(arr2),
            Write(up),
            Write(down)
        )

        self.wait()

class fig1_3a(Scene):
    def construct(self):
        oven = create_textbox(color=RED, string="Oven", string_color=RED)
        SGz = create_textbox(color=BLUE, string=r"SG\hat{z}", string_color=YELLOW)
        grp1 = VGroup(oven, SGz).arrange(RIGHT, buff=1).to_edge(LEFT, buff=0.7)
        SGz2 = create_textbox(color=BLUE, string=r"SG\hat{z}", string_color=YELLOW).shift(LEFT * 1).next_to(grp1, RIGHT, buff=3)

        silver_beam = Line(oven.get_right(), SGz.get_left(), color=WHITE)
        silver_atoms = MathTex(r"Ag\,Atoms", color=LIGHT_GRAY).scale(0.3).next_to(silver_beam, DOWN, buff=0.2)

        spin_line_offset = 0.3
        sz_up_line = Line(SGz.get_right() + [0, spin_line_offset, 0], SGz2.get_left() + [0, spin_line_offset, 0])
        sz_down_line = Line(SGz.get_right() + [0, -spin_line_offset, 0], (SGz2.get_left()/2 + [-0.5, 0, 0]) + [0, -spin_line_offset, 0])

        obsticle = Rectangle(WHITE, 0.5, 0.2, )
        obsticle.move_to(sz_down_line.get_end() + [obsticle.width / 2, 0, 0])
        hatch1 = Hatch_lines(obsticle, angle=PI / 6, offset=0.1, stroke_width=2)
        hatch2 = Hatch_lines(obsticle, angle=PI / 6 + PI / 2, offset=0.1, stroke_width=2)

        sz_up_text = MathTex(r"S_z+ comp.", substrings_to_isolate=["+", "z"], color=WHITE).scale(0.5).next_to(sz_up_line, UP)
        sz_down_text = MathTex(r"S_z- comp.", substrings_to_isolate=["-", "z"], color=WHITE).scale(0.5).next_to(sz_down_line, DOWN)
        sz_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("z", YELLOW)
        sz_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("z", YELLOW)

        sz2_up_line = Line(SGz2.get_right() + [0, spin_line_offset, 0], SGz2.get_right() + [2.5, spin_line_offset, 0])
        sz2_down_line = DashedLine(
            SGz2.get_right() + [0, -spin_line_offset, 0], 
            SGz2.get_right() + [2.5, -spin_line_offset, 0],
            )

        sz2_up_text = MathTex(r"S_z+ comp.", substrings_to_isolate=["+", "z"], color=WHITE).scale(0.5).next_to(sz2_up_line, UP)
        sz2_down_text = MathTex(r"\text{No} \,\; S_z- comp.", substrings_to_isolate=["-", "z"], color=WHITE).scale(0.5).next_to(sz2_down_line, DOWN)
        sz2_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("z", YELLOW)
        sz2_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("z", YELLOW)

        ## Explaination Bit
        sup = MathTex(r"|z,+\rangle", substrings_to_isolate=["z"], color=BLUE).move_to(sz_up_text.get_center() + [0, 1, 0])
        sup.set_color_by_tex("z", YELLOW)
        sup.scale(0.6)

        sdown = MathTex(r"|z,-\rangle", substrings_to_isolate=["z"], color=TEAL).move_to(sz_down_text.get_center() + [0, -1, 0])
        sdown.set_color_by_tex("z", YELLOW)
        sdown.scale(0.6)

         # Create individual parts with different colors
        part1 = MathTex(r"|z,-\rangle", color=TEAL, substrings_to_isolate=["z"])
        part1.set_color_by_tex("z", YELLOW)
        part2 = Tex(r" is blocked and only ")
        part3 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"])
        part3.set_color_by_tex("z", YELLOW)
        part4 = Tex(r" is passed through second ")
        part5 = Tex(r"$ SG\hat{z} $", color=YELLOW)
        part6 = Tex(r" setup")
        
        # Arrange them in a single line
        sentence1 = VGroup(part1, part2, part3, part4, part5, part6).arrange(RIGHT)

        sentence1.scale(0.6)
        sentence1.shift(UP * 3)

        part1 = Tex(r"We see only ")
        part2 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"])
        part2.set_color_by_tex("z", YELLOW)
        part3 = Tex(r" state again")
        
        sentence2 = VGroup(part1, part2, part3).arrange(RIGHT)
        sentence2.scale(0.6)
        sentence2.next_to(sentence1, DOWN)

        part1 = MathTex(r"\Rightarrow |z,-\rangle", color=TEAL, substrings_to_isolate=["z", r"\Rightarrow"])
        part1.set_color_by_tex("z", YELLOW)
        part1.set_color_by_tex(r"\Rightarrow", WHITE)
        part2 = Tex(r" has no component of ")
        part3 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"])
        part3.set_color_by_tex("z", YELLOW)
        
        # Arrange them in a single line
        sentence3 = VGroup(part1, part2, part3).arrange(RIGHT)
        sentence3.scale(0.6)
        sentence3.next_to(sentence2, DOWN)


        ## Playing out the animations
        self.play(DrawBorderThenFill(VGroup(grp1, SGz2)))
        
        self.wait()

        self.play(Create(silver_beam), Write(silver_atoms))

        self.wait()

        self.play(Create(sz_up_line))
        self.play(Write(sz_up_text))

        self.play(Create(sz2_up_line))
        self.play(Write(sz2_up_text))

        self.wait()
        
        self.play(DrawBorderThenFill(VGroup(obsticle, hatch1, hatch2)))

        self.play(Create(sz_down_line))
        self.play(Write(sz_down_text))

        self.play(Create(sz2_down_line))
        self.play(Write(sz2_down_text))

        self.wait()

        self.play(Write(sup), Write(sdown))
        self.play(Write(sentence1))
        self.play(Write(sentence2))
        self.play(Write(sentence3))

        self.wait()

class fig1_3b(Scene):
    def construct(self):
        oven = create_textbox(color=RED, string="Oven", string_color=RED)
        SGz = create_textbox(color=BLUE, string=r"SG\hat{z}", string_color=YELLOW)
        grp1 = VGroup(oven, SGz).arrange(RIGHT, buff=1).to_edge(LEFT, buff=0.7)
        SGx = create_textbox(color=PURPLE, string=r"SG\hat{x}", string_color=GREEN).shift(LEFT * 1).next_to(grp1, RIGHT, buff=3)

        silver_beam = Line(oven.get_right(), SGz.get_left(), color=WHITE)
        silver_atoms = MathTex(r"Ag\,Atoms", color=LIGHT_GRAY).scale(0.3).next_to(silver_beam, DOWN, buff=0.2)

        spin_line_offset = 0.3
        sz_up_line = Line(SGz.get_right() + [0, spin_line_offset, 0], SGx.get_left() + [0, spin_line_offset, 0])
        sz_down_line = Line(SGz.get_right() + [0, -spin_line_offset, 0], (SGx.get_left()/2 + [-0.5, 0, 0]) + [0, -spin_line_offset, 0])

        obsticle = Rectangle(WHITE, 0.5, 0.2, )
        obsticle.move_to(sz_down_line.get_end() + [obsticle.width / 2, 0, 0])
        hatch1 = Hatch_lines(obsticle, angle=PI / 6, offset=0.1, stroke_width=2)
        hatch2 = Hatch_lines(obsticle, angle=PI / 6 + PI / 2, offset=0.1, stroke_width=2)

        sz_up_text = MathTex(r"S_z+ comp.", substrings_to_isolate=["+", "z"], color=WHITE).scale(0.5).next_to(sz_up_line, UP)
        sz_down_text = MathTex(r"S_z- comp.", substrings_to_isolate=["-", "z"], color=WHITE).scale(0.5).next_to(sz_down_line, DOWN)
        sz_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("z", YELLOW)
        sz_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("z", YELLOW)

        sx_up_line = Line(SGx.get_right() + [0, spin_line_offset, 0], SGx.get_right() + [2.5, spin_line_offset, 0])
        sx_down_line = Line(
            SGx.get_right() + [0, -spin_line_offset, 0], 
            SGx.get_right() + [2.5, -spin_line_offset, 0],
            )

        sx_up_text = MathTex(r"S_x+ comp.", substrings_to_isolate=["+", "x"], color=WHITE).scale(0.5).next_to(sx_up_line, UP)
        sx_down_text = MathTex(r"S_x- comp.", substrings_to_isolate=["-", "x"], color=WHITE).scale(0.5).next_to(sx_down_line, DOWN)
        sx_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("x", YELLOW)
        sx_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("x", YELLOW)

        ## Explaination Bit

        # First part
        part1_1 = Tex(r"When the atoms in state ")
        part1_2 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"])
        part1_2.set_color_by_tex("z", YELLOW)
        part1_3 = Tex(r" are passed through a ")

        sentence1 = VGroup(part1_1, part1_2, part1_3).arrange(RIGHT)
        sentence1.scale(0.6)
        sentence1.shift(UP * 3)

        # Second part
        part2_1 = Tex(r"$SG\hat{x}$", color=GREEN)
        part2_2 = Tex(r", we again see only two discrete outcomes.")

        sentence2 = VGroup(part2_1, part2_2).arrange(RIGHT)
        sentence2.scale(0.6)
        sentence2.next_to(sentence1, DOWN)

        # Third part
        part3_1 = Tex(r"But now the states should be represented differently, say ")
        part3_2 = MathTex(r"|x,+\rangle", color=BLUE, substrings_to_isolate=["x"])
        part3_2.set_color_by_tex("x", YELLOW)
        part3_3 = Tex(r" and ")
        part3_4 = MathTex(r"|x,-\rangle .", color=TEAL, substrings_to_isolate=["x"])
        part3_4.set_color_by_tex("x", YELLOW)

        sentence3 = VGroup(part3_1, part3_2, part3_3, part3_4).arrange(RIGHT)
        sentence3.scale(0.6)
        sentence3.next_to(sentence2, DOWN)

        # Fourth part
        part4_1 = Tex(r"This observation is like saying that ")
        part4_2 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"])
        part4_2.set_color_by_tex("z", YELLOW)
        part4_3 = Tex(r" states are also states ")

        sentence4 = VGroup(part4_1, part4_2, part4_3).arrange(RIGHT)
        sentence4.scale(0.6)
        sentence4.next_to(sentence3, DOWN)

        # Fifth part
        part5_0 = Tex(r"with some amplitude along ")
        part5_1 = MathTex(r"|x,+\rangle", color=BLUE, substrings_to_isolate=["x"])
        part5_1.set_color_by_tex("x", YELLOW)
        part5_2 = Tex(r" and ")
        part5_3 = MathTex(r"|x,-\rangle", color=TEAL, substrings_to_isolate=["x"])
        part5_3.set_color_by_tex("x", YELLOW)
        part5_4 = Tex(r".")

        sentence5 = VGroup(part5_0, part5_1, part5_2, part5_3, part5_4).arrange(RIGHT)
        sentence5.scale(0.6)
        sentence5.next_to(sentence4, DOWN)


        ## Playing out the animations
        self.play(DrawBorderThenFill(VGroup(grp1, SGx)))
        
        self.wait()

        self.play(Create(silver_beam), Write(silver_atoms))

        self.wait()

        self.play(Create(sz_up_line))
        self.play(Write(sz_up_text))

        self.play(Create(sx_up_line))
        self.play(Write(sx_up_text))

        self.wait()
        
        self.play(DrawBorderThenFill(VGroup(obsticle, hatch1, hatch2)))

        self.play(Create(sz_down_line))
        self.play(Write(sz_down_text))

        self.play(Create(sx_down_line))
        self.play(Write(sx_down_text))

        self.wait()

        self.play(VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)]).animate.shift(DOWN * 1.5))

        self.play(Write(sentence1))
        self.play(Write(sentence2))
        self.play(Write(sentence3))
        self.play(Write(sentence4))
        self.play(Write(sentence5))

        self.wait()

class fig1_3c(ZoomedScene):
    def construct(self):
        # Define 4 boxes: oven, SGz, SGx, SGz2
        oven = create_textbox(color=RED, string="Oven", string_color=RED)
        SGz = create_textbox(color=BLUE, string=r"SG\hat{z}", string_color=YELLOW)
        grp1 = VGroup(oven, SGz).arrange(RIGHT, buff=0.7).to_edge(LEFT, buff=0.5)
        SGx = create_textbox(color=PURPLE, string=r"SG\hat{x}", string_color=GREEN).shift(LEFT * 1).next_to(grp1, RIGHT, buff=1.5)
        SGz2 = create_textbox(color=BLUE, string=r"SG\hat{z}", string_color=YELLOW).next_to(SGx, buff=1.5)

        # Silver Beam - Oven to SGz
        silver_beam = Line(oven.get_right(), SGz.get_left(), color=WHITE)
        silver_atoms = Tex(r"Ag\\Atoms", color=LIGHT_GRAY).scale(0.3).next_to(silver_beam, DOWN, buff=0.2)

        # Spin Lines - SGz to SGx
        spin_line_offset = 0.3
        sz_up_line = Line(SGz.get_right() + [0, spin_line_offset, 0], SGx.get_left() + [0, spin_line_offset, 0])
        sz_down_line = Line(SGz.get_right() + [0, -spin_line_offset, 0], (SGx.get_left() + [-sz_up_line.get_length() / 2,0,0]) + [0, -spin_line_offset, 0])

        obsticle = Rectangle(WHITE, 0.5, 0.2, )
        obsticle.move_to(sz_down_line.get_end() + [obsticle.width / 2, 0, 0])
        hatch1 = Hatch_lines(obsticle, angle=PI / 6, offset=0.1, stroke_width=2)
        hatch2 = Hatch_lines(obsticle, angle=PI / 6 + PI / 2, offset=0.1, stroke_width=2)

        sz_up_text = MathTex(r"S_z+ beam", substrings_to_isolate=["+", "z"], color=WHITE).scale(0.5).next_to(sz_up_line, UP)
        sz_down_text = MathTex(r"S_z- beam", substrings_to_isolate=["-", "z"], color=WHITE).scale(0.5).next_to(obsticle, DOWN)
        sz_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("z", YELLOW)
        sz_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("z", YELLOW)


        # Spin Lines - SGx to SGz2
        sx_up_line = Line(SGx.get_right() + [0, spin_line_offset, 0], SGz2.get_left() + [0, spin_line_offset, 0])
        sx_down_line = Line(SGx.get_right() + [0, -spin_line_offset, 0], (SGz2.get_left() + [-sx_up_line.get_length() / 2, 0, 0]) + [0, -spin_line_offset, 0])

        
        obsticle2 = Rectangle(WHITE, 0.5, 0.2, )
        obsticle2.move_to(sx_down_line.get_end() + [obsticle2.width / 2, 0, 0])
        hatch1_2 = Hatch_lines(obsticle2, angle=PI / 6, offset=0.1, stroke_width=2)
        hatch2_2 = Hatch_lines(obsticle2, angle=PI / 6 + PI / 2, offset=0.1, stroke_width=2)

        sx_up_text = MathTex(r"S_x+ beam", substrings_to_isolate=["+", "x"], color=WHITE).scale(0.5).next_to(sx_up_line, UP)
        sx_down_text = MathTex(r"S_x- beam", substrings_to_isolate=["-", "x"], color=WHITE).scale(0.5).next_to(obsticle2, DOWN)
        sx_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("x", YELLOW)
        sx_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("x", YELLOW)

        # Spin lines SGz2 to detector

        sz2_up_line = Line(SGz2.get_right() + [0, spin_line_offset, 0], SGz2.get_right() + [0.3, spin_line_offset, 0])
        sz2_down_line = Line(SGz2.get_right() + [0, -spin_line_offset, 0], SGz2.get_right() + [0.3, -spin_line_offset, 0])

        sz2_up_text = MathTex(r"S_z+ beam", substrings_to_isolate=["+", "z"], color=WHITE).scale(0.5).next_to(sz2_up_line, RIGHT, buff=0.1)
        sz2_down_text = MathTex(r"S_z- beam", substrings_to_isolate=["-", "z"], color=WHITE).scale(0.5).next_to(sz2_down_line, RIGHT, buff=0.1)
        sz2_up_text.set_color_by_tex("+", BLUE).set_color_by_tex("z", YELLOW)
        sz2_down_text.set_color_by_tex("-", TEAL).set_color_by_tex("z", YELLOW)

        # Brace 
        focus_group = VGroup(SGx, SGz2, sz2_up_text)
        brace = Brace(focus_group, DOWN, buff=0.8, color=YELLOW)

        ## EXPLAINATION 

        part1 = Tex(r"When atoms in state ")
        part2 = MathTex(r"|x,+\rangle", color=BLUE, substrings_to_isolate=["x"]).set_color_by_tex("x", YELLOW)
        part3 = Tex(r" go through ")
        part4 = MathTex(r"SG_z", substrings_to_isolate=["z"]).set_color_by_tex("z", YELLOW)
        sentence1 = VGroup(part1, part2, part3, part4).arrange(RIGHT).scale(0.6)
        sentence1.next_to(brace, DOWN, buff=0.5)

        sentence2 = Tex(r"we see equal number of atoms with states ").next_to(sentence1, DOWN).scale(0.6)
        
        part1 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"]).set_color_by_tex("z", YELLOW)
        part2 = Tex(" and ")
        part3 = MathTex(r"|z,-\rangle", color=TEAL, substrings_to_isolate=["z"]).set_color_by_tex("z", YELLOW)
        sentence3 = VGroup(part1, part2, part3).arrange(RIGHT).scale(0.6)
        sentence3.next_to(sentence2, DOWN)

        brace2 = Brace(VGroup(sentence1, sentence2, sentence3), LEFT, color=RED)

        sen1 = Tex(r"This is weird.").scale(0.6).align_to(brace2, UP).shift(LEFT * 3.5)
        sen1.set_color_by_gradient(BLUE, LIGHT_BROWN)
        
        part1 = Tex(r"Classically we would only except a ")
        part2 = MathTex(r"|z,+\rangle", color=BLUE, substrings_to_isolate=["z"]).set_color_by_tex("z", YELLOW)
        part3 = Tex(r" beam")
        sen2 = VGroup(part1, part2, part3).arrange(RIGHT).scale(0.6).next_to(sen1, DOWN)

        part1 = Tex(r"as the ")
        part2 = MathTex(r"|z,-\rangle", color=TEAL, substrings_to_isolate=["z"]).set_color_by_tex("z", YELLOW)
        part3 = Tex(" beam was earlier blocked.")
        sen3 = VGroup(part1, part2, part3).arrange(RIGHT).scale(0.6).next_to(sen2, DOWN)

        part1 = Tex(r"There is no memory of the first filter ")
        part2 = MathTex(r"SG_z", substrings_to_isolate=["z"], color=YELLOW)
        s1 = VGroup(part1, part2).arrange(RIGHT)

        part3 = Tex(r"and the particles coming from the second machine ")
        part4 = MathTex(r"SG_x", substrings_to_isolate=["x"], color=YELLOW)
        part5 = Tex(r" are not anymore ")
        part6 = MathTex(r"|z,+\rangle", substrings_to_isolate=["z", "+"], color=BLUE).set_color_by_tex("z", YELLOW)

        s2 = VGroup(part3, part4, part5, part6).arrange(RIGHT)

        last_line = VGroup(s1, s2).arrange(DOWN).scale(0.6).move_to(ORIGIN).shift(DOWN * 4.5)
        

        

        # Animations
        self.play(DrawBorderThenFill(VGroup(grp1, SGx, SGz2)))
        self.wait()
        self.play(Create(silver_beam), Write(silver_atoms))
        self.wait()

        self.play(Create(sz_up_line))
        self.play(Write(sz_up_text))
        
        self.play(DrawBorderThenFill(VGroup(obsticle, hatch1, hatch2)), Create(sz_down_line))
        self.play(Write(sz_down_text))

        self.wait()

        self.play(Create(sx_up_line))
        self.play(Write(sx_up_text))

        self.play(DrawBorderThenFill(VGroup(obsticle2, hatch1_2, hatch2_2)), Create(sx_down_line))
        self.play(Write(sx_down_text))

        self.wait()

        # self.play(self.camera.frame.animate.shift(RIGHT * 2))
        self.play(Create(sz2_up_line))
        self.play(Write(sz2_up_text))

        self.play(Create(sz2_down_line))
        self.play(Write(sz2_down_text))

        # self.play(self.camera.frame.animate.shift(DOWN * 2))

        self.wait()

        self.camera.frame.shift(DOWN * 2)
        self.camera.frame.save_state()
        self.camera.frame.shift(UP * 2)

        # self.camera.frame.set(width=focus_group.width * 2)
        self.play(self.camera.frame.animate.move_to(focus_group.get_center() + [0, -2, 0]))

        self.play(FadeIn(brace))
        self.play(Write(sentence1))
        self.play(Write(sentence2))
        self.play(Write(sentence3))

        self.wait()

        self.play(Restore(self.camera.frame))

        self.play(FadeIn(brace2))

        self.play(Write(sen1))
        self.play(Write(sen2))
        self.play(Write(sen3))

        self.wait()

        self.play(Write(last_line), run_time=2)

        self.wait()

       