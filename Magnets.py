from manim import *


def create_textbox(color_, string, string_color, height=1.5, width=3.5):
    result = VGroup()  # create a VGroup
    box = Rectangle(  # create a box
        height=height, width=width, fill_color=color_,
        fill_opacity=0.2, stroke_color=color_
    )
    text = Text(string, color=string_color).scale(0.7).move_to(box.get_center())  # create text
    result.add(box, text)  # add both objects to the VGroup
    return result


class Magnets(Scene):
    def construct(self):
        north_pole = create_textbox(RED, "N", WHITE).shift(UP * 2)
        south_pole = create_textbox(BLUE, "S", WHITE).shift(DOWN * 2)

        self.add(north_pole, south_pole)
