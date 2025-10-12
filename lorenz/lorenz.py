from manim import *
import numpy as np
from scipy.integrate import solve_ivp

class Lorenz(ThreeDScene):
    def lorenz(self, t, state, sigma=10, rho=28, beta=8/3):
        x, y, z = state
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        return [dx, dy, dz]

    def construct(self):
        # --- Simulation parameters ---
        sigma, rho, beta = 10, 28, 8/3
        t_span = (0, 30)             # total time span, use 30 for final version
        t_eval = np.linspace(*t_span, 2000)  # time steps for smoothness, use 2000 for final version
        ball_runtime = 60

        # Two slightly different initial conditions
        init1 = [1.0, 1.0, 1.0]
        init2 = [1.1, 1.1, 0.9]

        # Solve Lorenz equations
        sol1 = solve_ivp(lambda t, y: self.lorenz(t, y, sigma, rho, beta),
                         t_span, init1, t_eval=t_eval)
        sol2 = solve_ivp(lambda t, y: self.lorenz(t, y, sigma, rho, beta),
                         t_span, init2, t_eval=t_eval)

        # --- 3D Axes ---
        axes = ThreeDAxes(
            x_range=[-50, 50, 10],
            y_range=[-50, 50, 10],
            z_range=[-10, 50, 10],
            x_length=10, y_length=10, z_length=6
        )
        axes.add(axes.get_axis_labels(x_label="x", y_label="y", z_label="z"))
        self.add(axes)
        self.set_camera_orientation(phi=60 * DEGREES, theta=15 * DEGREES, zoom=1, frame_center=[0, 0, -0.5])



        # --- Full attractor curves (faint for context) ---
        # connect points to axes coordinate system
        points1 = [axes.c2p(x, y, z) for x, y, z in zip(*sol1.y)]
        points2 = [axes.c2p(x, y, z) for x, y, z in zip(*sol2.y)]
        # draw curves
        full_curve1 = VMobject(color="#577F8D", stroke_width=1)
        full_curve1.set_points_as_corners(points1)
        full_curve2 = VMobject(color="#E79E16", stroke_width=1)
        full_curve2.set_points_as_corners(points2)
        # add curves
        self.add(full_curve1, full_curve2)

        # --- Moving dots ---
        dot1 = Dot3D(points1[0], color=BLUE)
        dot2 = Dot3D(points2[0], color=ORANGE)

        # --- Trails (actual paths traced) ---
        trail1 = VMobject(color="#577F8D")
        trail1.set_points_as_corners([points1[0]])
        trail2 = VMobject(color="#E79E16")
        trail2.set_points_as_corners([points2[0]])

        self.add(dot1, dot2, trail1, trail2)

        # --- HUD State box ---

        # Updater for the coordinate texts
        def update_ball1_dim_text(mob, dt, dim):
            value = dot1.get_center()[dim]
            new_text = f"{value:.1f}"
            if mob.text != new_text:
                mob.set_text = new_text
                mob.become(Text(new_text, font_size=25, color = "#577F8D").move_to(mob.get_center()))
        def update_ball2_dim_text(mob, dt, dim):
            value = dot2.get_center()[dim]
            new_text = f"{value:.1f}"
            if mob.text != new_text:
                mob.set_text = new_text
                mob.become(Text(new_text, font_size=25, color = "#E79E16").move_to(mob.get_center()))

        # Actual box
        box_height = 1.5
        box_width = 7
        box = Rectangle(height=box_height, width=box_width, stroke_color=WHITE, fill_opacity=0
            ).shift(4*DOWN)
        state_text = Text("State:", font_size=25)
        ball1_x_value = Text(f"{dot1.get_center()[0]:.3f}", font_size=25, color = "#577F8D")
        ball1_x_value.add_updater(lambda mob, dt: update_ball1_dim_text(mob, dt, 0))
        ball1_y_value = Text(f"{dot1.get_center()[1]:.3f}", font_size=25, color = "#577F8D")
        ball1_y_value.add_updater(lambda mob, dt: update_ball1_dim_text(mob, dt, 1))
        ball1_z_value = Text(f"{dot1.get_center()[2]:.3f}", font_size=25, color = "#577F8D")
        ball1_z_value.add_updater(lambda mob, dt: update_ball1_dim_text(mob, dt, 2))
        ball1_line = VGroup(Text("x1 = ", font_size=25), ball1_x_value, Text("y1 = ", font_size=25), ball1_y_value, Text("z1 = ", font_size=25), ball1_z_value).arrange(RIGHT)
        ball2_x_value = Text(f"{dot2.get_center()[0]:.3f}", font_size=25, color = "#E79E16")
        ball2_x_value.add_updater(lambda mob, dt: update_ball2_dim_text(mob, dt, 0))
        ball2_y_value = Text(f"{dot2.get_center()[1]:.3f}", font_size=25, color = "#E79E16")
        ball2_y_value.add_updater(lambda mob, dt: update_ball2_dim_text(mob, dt, 1))
        ball2_z_value = Text(f"{dot2.get_center()[2]:.3f}", font_size=25, color = "#E79E16")
        ball2_z_value.add_updater(lambda mob, dt: update_ball2_dim_text(mob, dt, 2))
        ball2_line = VGroup(Text("x2 = ", font_size=25), ball2_x_value, Text("y2 = ", font_size=25), ball2_y_value, Text("z2 = ", font_size=25), ball2_z_value).arrange(RIGHT)
        box_text = VGroup(state_text, ball1_line, ball2_line).arrange(DOWN, buff=0.2)
        box_text.move_to(box.get_center())

        self.add_fixed_in_frame_mobjects(box, box_text)

        # --- Animate the two trajectories ---
        self.begin_ambient_camera_rotation(rate=-(2*PI/(ball_runtime+4))) # rotate camera during the animation
        self.wait(2) # to trigger rotation start
        self.play(
            MoveAlongPath(dot1, full_curve1),
            MoveAlongPath(dot2, full_curve2),
            run_time=ball_runtime,
            rate_func=linear
        )

        self.wait(2)
