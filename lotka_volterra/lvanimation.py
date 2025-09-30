from manim import *
import numpy as np

# --- Lotka–Volterra simulation function ---
def lotka_volterra(t_max=60, dt=0.1,
                   alpha=0.3, beta=0.15,
                   delta=0.05, gamma=0.3,
                   R0=5, F0=3): # parameter that keep the population SVG-animate-able
    steps = int(t_max / dt)
    t = np.linspace(0, t_max, steps)
    R = np.zeros(steps)
    F = np.zeros(steps)
    R[0], F[0] = R0, F0

    for i in range(steps - 1):
        dR = (alpha * R[i] - beta * R[i] * F[i]) * dt # actual non-linear equations
        dF = (delta * R[i] * F[i] - gamma * F[i]) * dt # actual non-linear equations
        R[i+1] = max(R[i] + dR, 0) # apply to initial population. use max to prevent nonsense ;-)
        F[i+1] = max(F[i] + dF, 0)

    return t, R, F


# --- Manim Scene ---
class PredatorPreyGraph(MovingCameraScene):
    def construct(self):
        # setup camera
        self.camera.frame.scale(1.3)  # zoom out 

        # simulate data
        t, R, F = lotka_volterra()

        # set up axes
        axes = Axes(
            x_range=[0, 60, 5],
            y_range=[0, 12, 2],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
            x_axis_config={"include_numbers": False}
        )
        labels = VGroup(
            MarkupText("Time").next_to(axes.x_axis, DOWN),
            MarkupText("Population").rotate(90*DEGREES).next_to(axes.y_axis, LEFT)
        )
        self.add(axes, labels)

        # rabbit curve
        rabbit_curve = axes.plot_line_graph(
            x_values=t, y_values=R,
            line_color="#0072B2",
            add_vertex_dots=False
        ).set_z_index(2)

        # fox curve
        fox_curve = axes.plot_line_graph(
            x_values=t, y_values=F,
            line_color="#E69F00",
            add_vertex_dots=False
        ).set_z_index(2)

        # animate drawing
        self.play(Create(rabbit_curve, run_time=10),
                  Create(fox_curve, run_time=10))
        self.wait(2)
