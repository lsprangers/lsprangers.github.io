from manim import (
    Scene,
    Axes,
    Text,
    FadeIn,
    Write,
    Arrow,
    MathTex,
    Dot,
    ORIGIN,
    RIGHT,
    UP,
    UR,
    YELLOW,
    GrowArrow,
    Transform,
    smooth,
)
import numpy as np

class VectorScalingDemo(Scene):
    """Animate a single yellow vector being scaled to three different endpoints.

    The vector always originates at the origin. you show axes, the vector, and
    animate it changing length (and potentially direction if points differ) to
    reach three specified target points sequentially.
    """

    def construct(self):
        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True, "font_size": 28},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        title = Text("Scaling a Single Vector", font_size=36).to_edge(UP + 0.2)

        self.play(FadeIn(axes), Write(axes_labels), FadeIn(title))
        self.wait(0.5)

        # Define the three target points (as examples)
        targets = [
            np.array([1.5, 1.0, 0.0]),  # First endpoint
            np.array([2.5, 0.5, 0.0]),  # Second endpoint
            np.array([-1.0, 2.0, 0.0]), # Third endpoint (change direction)
        ]

        # Initial vector (start tiny so you can grow it)
        origin = ORIGIN
        vector = Arrow(start=origin, end=origin + 0.01 * RIGHT, buff=0, color=YELLOW)
        vector_label = MathTex("\\vec{v}", color=YELLOW).next_to(vector.get_end() + 0.03 * RIGHT, UP)

        self.play(GrowArrow(vector), FadeIn(vector_label))
        self.wait(0.5)

        # Helper to animate to a new target
        def animate_to(target, label_text):
            new_vector = Arrow(start=origin, end=target, buff=0, color=YELLOW)
            new_label = MathTex(label_text, color=YELLOW).next_to(new_vector.get_end(), UP)
            # Transform vector shape and move label
            self.play(
                Transform(vector, new_vector),
                Transform(vector_label, new_label),
                run_time=1.5,
                rate_func=smooth,
            )
            dot = Dot(point=target, color=YELLOW)
            coord = MathTex(f"({target[0]:.1f}, {target[1]:.1f})", font_size=28).next_to(dot, UR, buff=0.35)
            self.play(FadeIn(dot), FadeIn(coord))
            self.wait(0.4)

        # Animate through targets with labels representing scale factors or steps
        animate_to(targets[0], "1.0 \\vec{v}")
        animate_to(targets[1], "1.7 \\vec{v}")
        animate_to(targets[2], "-0.8 \\vec{v}")

        self.wait(1.5)

if __name__ == "__main__":
    # To render: manim -pql manim/vector_scaling_demo.py VectorScalingDemo
    pass
