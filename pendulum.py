from manim import *
import numpy as np

class Pendulum(MovingCameraScene):
    def construct(self):
        self.camera.frame.shift(DOWN * 3)

        # Parameters
        amplitude = PI / 2
        speed = PI / 2
        L = 6

        # Tracker for time
        t_tracker = ValueTracker(0)

        def get_pendulum_pos():
            t = t_tracker.get_value()
            theta = amplitude * np.cos(speed * t)
            x = L * np.sin(theta)
            y = -L * np.cos(theta)
            return np.array([x, y, 0])

        def get_theta_degrees():
            t = t_tracker.get_value()
            theta = amplitude * np.cos(speed * t)
            return np.degrees(theta)

        # Updater that only updates every 4 frames
        def update_theta_text(mob, dt):
            if not hasattr(update_theta_text, "frame_counter"):
                update_theta_text.frame_counter = 0
            update_theta_text.frame_counter += 1

            if update_theta_text.frame_counter % 4 == 0:
                theta = get_theta_degrees()
                mob.become(Text(f"θ = {theta:.1f}°", font_size=60).to_corner(UR))

        # Pendulum visuals
        pendulum_line = always_redraw(
            lambda: Line(ORIGIN, get_pendulum_pos(), color=WHITE, stroke_width=20)
        )
        pendulum_ball = always_redraw(
            lambda: Dot(get_pendulum_pos(), radius=1, color="#0e4058")
        )
        theta_text = Text(f"θ = {get_theta_degrees():.1f}°", font_size=60).to_corner(UR)
        theta_text.add_updater(update_theta_text)

        # Arc showing angle θ
        theta_arc = always_redraw(
            lambda: Arc(
                start_angle=3 * PI / 2,
                angle=amplitude * np.cos(speed * t_tracker.get_value()),
                radius=2.5,
                arc_center=ORIGIN,
                color="#666666",
                stroke_width=6,
            )
        )

        # θ label
        theta_label = always_redraw(
            lambda: Text("θ", font_size=64, color="#666666").move_to(
                Arc(
                    start_angle=3 * PI / 2,
                    angle=amplitude * np.cos(speed * t_tracker.get_value()) / 2,
                    radius=2.0,
                    arc_center=ORIGIN,
                ).point_from_proportion(0.5)
            )
        )

        # Static elements
        reference_line = DashedLine(ORIGIN, DOWN * config.frame_height, color="#666666")

        # Add elements in order of layering
        self.add(reference_line)
        self.add(theta_arc, theta_label)
        self.add(pendulum_line, pendulum_ball, theta_text)

        self.play(t_tracker.animate.set_value(4), run_time=4, rate_func=linear)
