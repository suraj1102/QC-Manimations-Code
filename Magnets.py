from manim import *

class Magnets(Scene):
    def construct(self):
        magnets = self.createMagnets()
        self.add(magnets)

    def createMagnets(self):
        north_pole = self.create_textbox(RED, "N", WHITE)
        south_pole = self.create_textbox(BLUE, "S", WHITE)
        
        north = self.createNorthPole(north_pole)
        south = self.createSouthPole(south_pole)

        poles = VGroup(south, north).arrange(DOWN, buff=2.5)

        # Draw Magnetic Field Lines

        start1 = north.get_edge_center(UP)
        end1 = south.get_edge_center(DOWN)
        h11 = start1 + RIGHT
        h12 = end1 + LEFT

        # Tried to do it with bezier curve but you couldn't easily add a tip to it
        line1 = CubicBezier(start1, h11, h12, end1)
        
        carr = ArcBetweenPoints(start1, end1, PI, 100)
        carr2 = ArcBetweenPoints(start1, end1, PI / 10, 2).shift(RIGHT * 0.75)
        carr3 = ArcBetweenPoints(start1, end1, PI / 10, -2).shift(LEFT * 0.75)
        carr4 = ArcBetweenPoints(start1, end1, TAU / 4, 1.6).shift(RIGHT * 1.5)
        carr5 = ArcBetweenPoints(start1, end1, TAU / 4, -1.6).shift(LEFT * 1.5)

        mf_lines = VGroup(carr, carr2, carr3, carr4, carr5)
        mf_lines.set_color(GRAY)
        mf_lines.fill_opacity =0
        for line in mf_lines:
            line.add_tip(tip_length=0.3, tip_width=0.2)

        magnets = VGroup(mf_lines, north, south)
        return magnets


    def createNorthPole(self, north_pole: Mobject) -> Mobject:
        offset = 3.5
        positions = [
            north_pole.get_corner(UP + LEFT),
            north_pole.get_corner(UP + RIGHT),
            north_pole.get_corner(DOWN + RIGHT),
            north_pole.get_corner(DOWN + LEFT),
            north_pole.get_corner(UP + LEFT),
            north_pole.get_corner(UP + LEFT) + np.array([north_pole.height / offset, north_pole.height / offset, 0]),
            north_pole.get_corner(UP + RIGHT) + np.array([north_pole.height / offset, north_pole.height / offset, 0]),
            north_pole.get_corner(UP + RIGHT),
            north_pole.get_corner(DOWN + RIGHT),
            north_pole.get_corner(DOWN + RIGHT) + np.array([north_pole.height / offset * 2, 0, 0]),
            north_pole.get_corner(UP + RIGHT) + np.array([north_pole.height / offset * 2, 0, 0]),
            north_pole.get_corner(UP + RIGHT) + np.array([north_pole.height / offset, north_pole.height / offset, 0]),
            north_pole.get_corner(UP + RIGHT),
        ]


        shape = Polygon(*positions, fill_opacity=0.3, color=RED)
        N = Text("N", color=WHITE).scale(0.7).move_to(Polygon(*np.unique(shape.get_anchors(), axis=0)[:4]).get_center())  # create text
        north = VGroup(shape, N)
        return north
    
    def createSouthPole(self, south_pole: Mobject) -> Mobject:
        offset2 = 4
        positions2 = [
            south_pole.get_corner(UP + LEFT),
            south_pole.get_corner(UP + RIGHT),
            south_pole.get_corner(DOWN + RIGHT),
            south_pole.get_corner(DOWN + LEFT),
            south_pole.get_corner(UP + LEFT),
            south_pole.get_corner(UP + LEFT) + np.array([south_pole.height / offset2, south_pole.height / offset2, 0]),
            south_pole.get_corner(UP + RIGHT) + np.array([south_pole.height / offset2, south_pole.height / offset2, 0]),
            south_pole.get_corner(UP + RIGHT),
            south_pole.get_corner(DOWN + RIGHT),
            south_pole.get_corner(DOWN + RIGHT) + np.array([south_pole.height / offset2, south_pole.height / offset2, 0]),
            south_pole.get_corner(UP + RIGHT) + np.array([south_pole.height / offset2, south_pole.height / offset2, 0]),
            south_pole.get_corner(UP + RIGHT),
        ]

        shape2 = Polygon(*positions2, fill_opacity=0.3, color=BLUE)
        S = Text("S", color=WHITE).scale(0.7).move_to(Polygon(*np.unique(shape2.get_anchors(), axis=0)[:4]).get_center())  # create text
        south = VGroup(shape2, S)
        return south
    
    def create_textbox(self, color_, string, string_color, height=1.5, width=3.5):
        result = VGroup()  # create a VGroup
        box = Rectangle(  # create a box
            height=height, width=width, fill_color=color_,
            fill_opacity=0.2, stroke_color=color_
        )
        text = Text(string, color=string_color).scale(0.7).move_to(box.get_center())  # create text
        result.add(box, text)  # add both objects to the VGroup
        return result