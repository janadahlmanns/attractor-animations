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
class LVAnimation(MovingCameraScene):
    def construct(self):
        # setup camera
        self.camera.frame.scale(1.6)  # zoom out 

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
        
        # --- Forest Panel on the Left ---
        forest_radius = 2.2
        forest_panel_size = 5  # width and height of clearing
        forest_clearing = Square(side_length=forest_panel_size, fill_color="#b3e6b3", fill_opacity=1, stroke_color=BLACK)

        # Tree map
        tree_map = {
            "lotka_volterra/tree1_green.svg": [0, 90, 210],
            "lotka_volterra/tree2_lightgreen.svg": [30, 100, 220],
            "lotka_volterra/tree1_darkgreen.svg": [45, 135, 180],
            "lotka_volterra/tree2_green.svg": [74, 250, 320],
            "lotka_volterra/tree1_lightgreen.svg": [270, 315],
            "lotka_volterra/tree2_darkgreen.svg": [80, 200, 340],
            "lotka_volterra/tree1_green.svg": [135, 160, 260],
            "lotka_volterra/tree1_darkgreen.svg": [150, 10, 20],
        }

        trees = VGroup()
        for svg_path, angles in tree_map.items():
            for angle_deg in angles:
                angle_rad = angle_deg * DEGREES
                tree = SVGMobject(svg_path).scale(0.3)
                pos = forest_clearing.get_center() + forest_radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
                tree.move_to(pos)
                trees.add(tree)

        # Rabbits map
        rabbits_map = [[0,0],[0.8,0], [0.5,90], [0.7,40], [0.3,160], [0.6, 200],[0.8, 280],[0.3,320],[0.8,140],[0.5,240]]
        rabbit_svg = "lotka_volterra/rabbit.svg"

        rabbits = VGroup()
        for rabbit_pos in rabbits_map:
            rabbit = SVGMobject(rabbit_svg ).scale(0.3)
            pos = forest_clearing.get_center() + (rabbit_pos[0]*forest_radius) * np.array([np.cos(rabbit_pos[1]*DEGREES), np.sin(rabbit_pos[1]*DEGREES), 0])
            rabbit.move_to(pos)
            rabbits.add(rabbit)

        forest_panel = VGroup(forest_clearing, trees, rabbits)
        forest_panel.move_to(np.array([-8, 0, 0]))

        self.add(forest_panel)


        # animate drawing
        self.play(Create(rabbit_curve, run_time=10),
                  Create(fox_curve, run_time=10))
        self.wait(2)
