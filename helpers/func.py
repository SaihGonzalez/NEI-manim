"""This contains functions that will make lecture making easier. """
from manim import *

class LinearTransformationExample(Scene): 
    def construct(self): 

        plane = NumberPlane(
            x_range=[-5, 5, 1], 
            y_range=[-5, 5, 1], 
            background_line_style={
                "stroke_color": BLUE_D, 
                "stroke_width": 2, 
                "stroke_opacity": 0.6
            }
        )

        vector = Vector([1, 2], color=YELLOW)
        vector_label = MathTex(r"\begin{bmatrix} 1 \\ 2 \end{bmatrix}", color=YELLOW)
        vector_label.next_to(vector.get_end(), UR, buff=0.1)

        matrix = [[1, 1], 
                  [0, 1]]
        
        matrix_text = MathTex(r"A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}"
                              ).to_edge(UL).add_background_rectangle()
        
        self.play(Create(plane))
        self.play(GrowArrow(vector), Write(vector_label))
        self.wait(1)
        self.play(Write(matrix_text))
        self.wait(1)

    




