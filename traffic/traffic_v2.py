from manim import *

class Traffic(MovingCameraScene):
    def construct(self):
        # --- GLOBAL SETTINGS ---
        self.camera.background_color = "#8bc08c"


        # --- BACKGROUND MAP ---
        # Sample tile to measure size 
        sample_tile = SVGMobject("traffic/street_2.svg")
        ts = sample_tile.width  # tile size in manim units

        map_max_width = 8*ts
        tile_map = {
            "traffic/street_2.svg": [[0,0,0], [3,0,0], [6,0,0], [1,-1,90], [2,-1,90],[4,-1,90], [5,-1,90], [3,-2,0], [6,-2,0], [0,-3,0], [3,-3,0],[6,-3,0], [1,-4,90], [2,-4,90], [4,-4,90], [5,-4,90], [7,-4,90], [0,-5,0], [3,-5,0], [6,-5,0]],
            "traffic/street_3.svg": [[0,-1,0], [6,-1,180], [0,-2,180], [0,-4,0]],
            "traffic/street_4.svg": [[3,-1,0], [3,-4,0], [6,-4,0]],
            "traffic/house-blue.svg": [[2,-2,0]],
            "traffic/house-orange.svg": [[2,-3,0]],
            "traffic/house-green.svg": [[5,0,0]],
        }

        # --- STATE DEFINITION ---
        # Format: [x, y, v] (in tile coordinates)
        state_list = [
        [[6, 0, 1], [3, -3, 1], [3, -2, 1], [3, 20, 1]],
        [[6, -1, 1], [3, -4, 1], [3, -1, 1], [3, 20, 1]],
        [[6, -2, 1], [4, -4, 1], [2, -1, 1], [3, 0, 1]],
        [[6, -3, 1], [5, -4, 1], [1, -1, 1], [3, -1, 1]],
        [[6, -3, 0], [6, -4, 1], [0, -1, 1], [2, -1, 1]],
        [[6, -4, 1], [7, -4, 1], [0, 0, 1], [1, -1, 1]],
        [[6, -5, 1], [20, -4, 1], [0, 20, 1], [0, -1, 1]],
        [[6, -20, 1], [20, -4, 1], [0, 20, 1], [0, -2, 1]],
        [[6, -20, 1], [20, -4, 1], [0, 20, 1], [-5, -2, 1]],
        ]

        # --- CAMERA SETTINGS ---
        self.camera.frame.set_width(12*ts)
        self.camera.frame.move_to([10, -5, 0])

        # --- DRAW BACKGROUND ---
        for filename, positions in tile_map.items():
            for x, y, rot in positions:
                tile = SVGMobject(filename)
                tile.move_to([x * ts, y * ts, 0])
                tile.rotate(rot * DEGREES)
                self.add(tile)

        # --- CREATE CARS ---
        init_green_state, init_orange_state, init_blue_state, init_yellow_state = state_list[0]
        car_green = SVGMobject("traffic/car_3_green.svg")
        car_green.scale(0.6)
        car_green.move_to([init_green_state[0] * ts, init_green_state[1] * ts, 0])
        self.add(car_green)
        car_orange = SVGMobject("traffic/car_2_orange.svg")
        car_orange.scale(0.6)
        car_orange.move_to([init_orange_state[0] * ts, init_orange_state[1] * ts, 0])
        self.add(car_orange)
        car_blue = SVGMobject("traffic/car_1_blue.svg")
        car_blue.scale(0.6)
        car_blue.move_to([init_blue_state[0] * ts, init_blue_state[1] * ts, 0])
        self.add(car_blue)
        car_yellow = SVGMobject("traffic/car_4_yellow.svg")
        car_yellow.scale(0.6)
        car_yellow.move_to([init_yellow_state[0] * ts, init_yellow_state[1] * ts, 0])
        self.add(car_yellow)

        # --- CREATE STATE BOX ---
        box_margin = 0
        box_width = 5
        box_height = 12
        box = Rectangle(height=box_height, width=box_width, stroke_color=WHITE, fill_opacity=0)
        anchor_pos = RIGHT * (map_max_width + box_margin)
        top_left_shift = DOWN * ((box_height / 2)-(ts/2)) + RIGHT * (box_width / 2)
        box.move_to(anchor_pos + top_left_shift)


        state_text = Text("State", font_size=36)

        x_val_green = Text(f"{init_green_state[0]:.0f}", font_size=36)
        y_val_green = Text(f"{init_green_state[1]:.0f}", font_size=36)
        v_val_green = Text(f"{init_green_state[2]:.0f}", font_size=36)
        x_line_green = VGroup(Text("Green car X =", font_size=36), x_val_green).arrange(RIGHT, buff=0.2)
        y_line_green = VGroup(Text("Green car Y =", font_size=36), y_val_green).arrange(RIGHT, buff=0.2)
        v_line_green = VGroup(Text("Green car V =", font_size=36), v_val_green).arrange(RIGHT, buff=0.2)

        x_val_orange = Text(f"{init_orange_state[0]:.0f}", font_size=36)
        y_val_orange = Text(f"{init_orange_state[1]:.0f}", font_size=36)
        v_val_orange = Text(f"{init_orange_state[2]:.0f}", font_size=36)
        x_line_orange = VGroup(Text("Orange car X =", font_size=36), x_val_orange).arrange(RIGHT, buff=0.2)
        y_line_orange = VGroup(Text("Orange car Y =", font_size=36), y_val_orange).arrange(RIGHT, buff=0.2)
        v_line_orange = VGroup(Text("Orange car V =", font_size=36), v_val_orange).arrange(RIGHT, buff=0.2)

        x_val_blue = Text(f"{init_blue_state[0]:.0f}", font_size=36)
        y_val_blue = Text(f"{init_blue_state[1]:.0f}", font_size=36)
        v_val_blue = Text(f"{init_blue_state[2]:.0f}", font_size=36)
        x_line_blue = VGroup(Text("Blue car X =", font_size=36), x_val_blue).arrange(RIGHT, buff=0.2)
        y_line_blue = VGroup(Text("Blue car Y =", font_size=36), y_val_blue).arrange(RIGHT, buff=0.2)
        v_line_blue = VGroup(Text("Blue car V =", font_size=36), v_val_blue).arrange(RIGHT, buff=0.2)

        x_val_yellow = Text(f"{init_yellow_state[0]:.0f}", font_size=36)
        y_val_yellow = Text(f"{init_yellow_state[1]:.0f}", font_size=36)
        v_val_yellow = Text(f"{init_yellow_state[2]:.0f}", font_size=36)
        x_line_yellow = VGroup(Text("Yellow car X =", font_size=36), x_val_yellow).arrange(RIGHT, buff=0.2)
        y_line_yellow = VGroup(Text("Yellow car Y =", font_size=36), y_val_yellow).arrange(RIGHT, buff=0.2)
        v_line_yellow = VGroup(Text("Yellow car V =", font_size=36), v_val_yellow).arrange(RIGHT, buff=0.2)

        box_text = VGroup(state_text, x_line_green, y_line_green, v_line_green, x_line_orange, y_line_orange, v_line_orange, x_line_blue, y_line_blue, v_line_blue, x_line_yellow, y_line_yellow, v_line_yellow).arrange(DOWN, buff=0.3)
        box_text.scale_to_fit_width(box_width * 0.9)
        box_text.move_to(box.get_center())

        self.add(box, box_text)

        # --- STEP THROUGH STATE LIST ---
        for state in state_list:
            green_state, orange_state, blue_state, yellow_state = state
            
            x_green = green_state[0]
            y_green = green_state[1]
            v_green = green_state[2]
            x_orange = orange_state[0]
            y_orange = orange_state[1]
            v_orange = orange_state[2]
            x_blue = blue_state[0]
            y_blue = blue_state[1]
            v_blue = blue_state[2]
            x_yellow = yellow_state[0]
            y_yellow = yellow_state[1]
            v_yellow = yellow_state[2]

            # Animate car movement
            self.play(
                car_green.animate.move_to([x_green * ts, y_green * ts, 0]),
                car_orange.animate.move_to([x_orange * ts, y_orange * ts, 0]),
                car_blue.animate.move_to([x_blue * ts, y_blue * ts, 0]),
                car_yellow.animate.move_to([x_yellow * ts, y_yellow * ts, 0]),
                run_time=0.8
            )

            # Update text 
            x_val_green.become(Text(f"{x_green:.0f}", font_size=36).move_to(x_val_green.get_center()))
            y_val_green.become(Text(f"{y_green:.0f}", font_size=36).move_to(y_val_green.get_center()))
            v_val_green.become(Text(f"{v_green:.0f}", font_size=36).move_to(v_val_green.get_center()))
            x_val_orange.become(Text(f"{x_orange:.0f}", font_size=36).move_to(x_val_orange.get_center()))
            y_val_orange.become(Text(f"{y_orange:.0f}", font_size=36).move_to(y_val_orange.get_center()))
            v_val_orange.become(Text(f"{v_orange:.0f}", font_size=36).move_to(v_val_orange.get_center()))
            x_val_blue.become(Text(f"{x_blue:.0f}", font_size=36).move_to(x_val_blue.get_center()))
            y_val_blue.become(Text(f"{y_blue:.0f}", font_size=36).move_to(y_val_blue.get_center()))
            v_val_blue.become(Text(f"{v_blue:.0f}", font_size=36).move_to(v_val_blue.get_center()))
            x_val_yellow.become(Text(f"{x_yellow:.0f}", font_size=36).move_to(x_val_yellow.get_center()))
            y_val_yellow.become(Text(f"{y_yellow:.0f}", font_size=36).move_to(y_val_yellow.get_center()))
            v_val_yellow.become(Text(f"{v_yellow:.0f}", font_size=36).move_to(v_val_yellow.get_center()))

            self.wait(0.2)

        self.wait(2)
