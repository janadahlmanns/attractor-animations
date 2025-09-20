from manim import *
import numpy as np

class Pendulum_damped(MovingCameraScene):
    def construct(self):
        # Parameters
        amplitude = PI / 2 * 0.8
        L = 6
        ball_radius = 1
        g = 9.81
        beta = 0.25 # damping coefficient

        # Derived parameters
        pendulum_max_width = L * np.sin(amplitude) + ball_radius
        omega_0 = np.sqrt(g/L) # frequency without damping
        omega_d = np.sqrt(max(0, omega_0 **2 - beta**2)) # frequency with damping

        # Tracker for time
        t_tracker = ValueTracker(0)

        def get_theta(t): # diff equation for damped pendulum
            return amplitude * np.exp(-beta * t) * np.cos(omega_d * t)

        def get_pendulum_pos(): # convert theta to x,y,z coordinates to draw
            t = t_tracker.get_value()
            theta = get_theta(t)
            x = L * np.sin(theta)
            y = -L * np.cos(theta)
            return np.array([x, y, 0])

        def get_theta_degrees(): # convert theta to degrees
            t = t_tracker.get_value()
            theta = get_theta(t)
            return np.degrees(theta)

        # Updater that only updates every n frames
        def update_theta_text(mob, dt):
            if not hasattr(update_theta_text, "frame_counter"):
                update_theta_text.frame_counter = 0
            update_theta_text.frame_counter += 1

            if update_theta_text.frame_counter % 2 == 0:
                mob.text = f"{get_theta_degrees():.1f}"
                mob.become(Text(mob.text, font_size=60).move_to(mob.get_center()))

        # Pendulum visuals
        pendulum_line = always_redraw(
            lambda: Line(ORIGIN, get_pendulum_pos(), color=WHITE, stroke_width=20)
        )
        pendulum_ball = always_redraw(
            lambda: Dot(get_pendulum_pos(), radius=ball_radius, color="#0e4058")
        )

        # Arc with θ label
        reference_line = DashedLine(ORIGIN, DOWN * config.frame_height, color="#666666")
        theta_arc = always_redraw(
            lambda: Arc(
                start_angle=3 * PI / 2,
                angle = get_theta(t_tracker.get_value()),
                radius=2.5,
                arc_center=ORIGIN,
                color="#666666",
                stroke_width=6,
            )
        )
        theta_label = always_redraw(
            lambda: Text("θ", font_size=64, color="#666666").move_to(
                Arc(
                    start_angle=3 * PI / 2,
                    angle = get_theta(t_tracker.get_value())/2,
                    radius=2.0,
                    arc_center=ORIGIN,
                ).point_from_proportion(0.5)
            )
        )
   
        # State box
        box_margin = 2
        box_height = 3.0
        box_width = 3.5
        box = Rectangle(
            height=box_height, width=box_width, stroke_color=WHITE, fill_opacity=0
        ).shift(RIGHT * (pendulum_max_width + box_margin), RIGHT)
        state_text = Text("State:")
        theta_value = Text(f"{get_theta_degrees():.1f}", font_size=60)
        theta_value.add_updater(update_theta_text)
        theta_line = VGroup(Text("θ = ", font_size=60), theta_value, Text("°", font_size=60)).arrange(RIGHT)
        box_text = VGroup(state_text, theta_line).arrange(DOWN, buff=0.4)
        box_text.move_to(box.get_center())


        #set camera field of view
        fov_margin = 0.25
        x_min = -L -ball_radius - fov_margin
        x_max = L +ball_radius + box_margin + box_width + fov_margin
        y_min = min(-L -ball_radius - fov_margin, -box_height - fov_margin)
        y_max = 2*fov_margin

        frame_width = x_max - x_min
        frame_center = [(x_min + x_max)/2, (y_min + y_max)/2, 0]

        self.camera.frame.set_width(frame_width)
        self.camera.frame.move_to(frame_center)


        # Add elements in order of layering
        self.add(reference_line)
        self.add(theta_arc, theta_label)
        self.add(pendulum_line, pendulum_ball, box, box_text)

        self.play(t_tracker.animate.set_value(30), run_time=20, rate_func=linear)

        self.wait(3)
