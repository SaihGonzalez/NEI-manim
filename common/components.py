import numpy as np
from manim import * 
from common.colors import *


def fade_swap(scene: Scene, old_mobjects, new_mobjects, run_time: float = 1.0): 
    """
    Fades out old mobjects while fading in new mobjects simultaneously. 
    Accepts single Mobjects, lists, or VGroups. 
    """
    outs = [FadeOut(m) for m in (old_mobjects if isinstance(old_mobjects, (list, tuple, VGroup)) else [old_mobjects])]
    ins = [FadeIn(m) for m in (new_mobjects if isinstance(new_mobjects, (list, tuple, VGroup)) else [new_mobjects])]
    scene.play(*outs, *ins, run_time=run_time)


def pulse_highlight(scene: Scene, mobject: Mobject, color=HIGHLIGHT, scale_factor: float = 1.25, run_time: float = 0.8): 
    """
    Briefly scales up and highlights Mobject to draw viewer attention
    """
    scene.play(
        mobject.animate.scale(scale_factor).set_color(color), 
        rate_func=there_and_back,
        run_time=run_time
    )

def smart_wait(scene: Scene, duration: float = 1.0): 
    """
    Wait helper to make scene timing adjustments easily embedded. 
    """
    scene.wait(duration)

def create_labeled_vector(coords, label_text: str = "", color=PRIMARY, buff: float = 0) -> VGroup:
    """
    Creates 2D vector with option LaTex label positioned near the tip. 
    """
    x, y = coords[0], coords[1]
    vec = Vector([x, y, 0], color=color, buff=buff)

    if label_text: 
        label = MathTex(label_text, color=color, font_size=32)
        direction = np.array([x, y, 0], dtype=float)

        norm = np.linalg.norm(direction)
        if norm != 0: 
            direction /= norm

        label.move_to(vec.get_end() + direction * 0.35)
        return VGroup(vec, label)
    return VGroup(vec)

def create_vector_addition(v1_coords, v2_coords, color1=PRIMARY, color2=SECONDARY, sum_color=ACCENT) -> VGroup: 
    """
    Builds complete head-to-tail vector addition diagram for $\\vec{u} + \\vec{v} = \\vec{w}$.
    Returns a VGroup containing: [v1, v2, resultant_sum, dashed_projection1, dashed_projection2]
    """
    v1_end= np.array([v1_coords[0], v1_coords[1], 0], dtype=float)
    v2_vec= np.array([v2_coords[0], v2_coords[1], 0], dtype=float)
    sum_end = v1_end + v2_vec

    v1 = Vector(v1_end, color=color1, buff=0)
    v2 = Arrow(start=v1_end, end=sum_end, color=color2, buff=0)

    v_sum = Vector(sum_end, color=sum_color, buff=0)

    guide_v2 = Arrow(start=ORIGIN, end=v2_vec, color=color2, buff=0).set_opacity(0.3)
    dash_proj = DashedLine(start=v2_vec, end=sum_end, color=color1, stroke_opacity=0.5)

    return VGroup(v1, v2, v_sum, guide_v2, dash_proj)

def create_styled_matrix(matrix_data: Union[list, np.ndarray], color=TEXT_MAIN, bracket_color=BORDER, decimal_places: int | None = None) -> Matrix: 
    """
    Creates formated matrix using np array or 2d list"""

    if isinstance(matrix_data, np.ndarray):
        matrix_data = matrix_data.reshape(-1, 1)

    if decimal_places is not None: 
        matrix_data = np.round(matrix_data, decimal_places)

    matrix_data = matrix_data.tolist()

    matrix_mobj = Matrix(
        matrix_data, element_to_mobj_config={"color": color}
    )
    matrix_mobj.get_brackets().set_color(bracket_color)

    return matrix_mobj

# Add to common/components.py

def transition_to_grid(scene: Scene, old_mobjects, x_range=[-5, 5, 1], y_range=[-3, 3, 1]) -> NumberPlane:
    """
    Fades out old scene elements while animating in a coordinate grid (NumberPlane).
    Returns the created NumberPlane for further vector operations.
    """
    grid = NumberPlane(
        x_range=x_range,
        y_range=y_range,
        background_line_style={"stroke_color": BORDER, "stroke_opacity": 0.5},
        axis_config={"color": TEXT_MUTED}
    )
    
    outs = [FadeOut(m) for m in (old_mobjects if isinstance(old_mobjects, (list, tuple, VGroup)) else [old_mobjects])]
    scene.play(*outs, Create(grid), run_time=1.2)
    return grid


def animate_matrix_transform(scene: Scene, matrix_np: np.ndarray, grid: NumberPlane, vectors: VGroup = None, run_time: float = 2.0):
    """
    Applies a 2x2 matrix transformation to the grid and optional vectors simultaneously.
    
    matrix_np: A 2x2 NumPy array, e.g., np.array([[2, 1], [0, 1]])
    """
    # 2x2 matrix into a 3x3 transformation matrix for Manim's 3D coordinates
    transform_matrix = np.array([
        [matrix_np[0, 0], matrix_np[0, 1], 0],
        [matrix_np[1, 0], matrix_np[1, 1], 0],
        [0,               0,               1]
    ])

    animations = [ApplyMatrix(transform_matrix, grid)]
    
    if vectors is not None:
        animations.append(ApplyMatrix(transform_matrix, vectors))

    scene.play(*animations, run_time=run_time, rate_func=smooth)

    