from manim import *

class Traffic(MovingCameraScene):
    def construct(self):
        # --- GLOBAL SETTINGS ---
        self.camera.background_color = "#8bc08c"
        # Tracker for time
        t_tracker = ValueTracker(0)

        # Sample tile to measure size 
        sample_tile = SVGMobject("traffic/street_2.svg")
        ts = sample_tile.width  # tile size in manim units

        tile_map = {
            "traffic/street_2.svg": [[0,0,0], [3,0,0], [6,0,0], [1,-1,90], [2,-1,90],[4,-1,90], [5,-1,90], [3,-2,0], [6,-2,0], [0,-3,0], [3,-3,0],[6,-3,0], [1,-4,90], [2,-4,90], [4,-4,90], [5,-4,90], [7,-4,90], [0,-5,0], [3,-5,0], [6,-5,0]],
            "traffic/street_3.svg": [[0,-1,0], [6,-1,180], [0,-2,180], [0,-4,0]],
            "traffic/street_4.svg": [[3,-1,0], [3,-4,0], [6,-4,0]],
            "traffic/house-blue.svg": [[2,-2,0]],
            "traffic/house-orange.svg": [[2,-3,0]],
            "traffic/house-green.svg": [[5,0,0]],
        }
        map_max_width = 8

        # Adjust camera to fit everything
        self.camera.frame.set_width(12*ts)
        self.camera.frame.move_to([10, -5, 0])


        # Place backgroung tiles
        for filename, positions in tile_map.items():
            for pos in positions:
                x, y, rot = pos
                tile = SVGMobject(filename)
                tile.move_to([x*ts,y*ts,0])
                tile.rotate(rot * DEGREES)
                self.add(tile)

        # Place cars
        car_green = SVGMobject("traffic/car_3_green.svg")
        car_orange = SVGMobject("traffic/car_2_orange.svg")
        car_blue = SVGMobject("traffic/car_1_blue.svg")
        car_yellow = SVGMobject("traffic/car_4_yellow.svg")
        car_green.move_to([6*ts,0,0])
        car_orange.move_to([3*ts,-3*ts,0])
        car_blue.move_to([3*ts,-2*ts,0])
        car_yellow.move_to([20*ts,3*ts,0])
        car_green.scale(0.6)
        car_orange.scale(0.6)
        car_blue.scale(0.6)
        car_yellow.scale(0.6)
        self.add(car_green)
        self.add(car_orange)
        self.add(car_blue)
        self.add(car_yellow)

        car_green_route=[[6,0], [6,-1], [6,-2], [6,-3], [6,-3], [6,-4], [6,-5], [6,-20]]
        car_green_speed=[1,1,1,1,0,1,1,1]
        car_orange_route=[[3,-3],[3,-4], [4,-4], [5,-4], [6,-4], [7,-4], [20,-4], [20,-4]]
        car_orange_speed=[1,1,1,1,1,1,1]
        car_blue_route = [[3,-2], [3,-1], [2,-1],[1,-1], [0,-1], [0, 0],[0,20],[0,20],[0,20]]
        car_blue_speed=[1,1,1,1,1,1,1,1,1]
        car_yellow_route = [[3,10], [3,10], [3,0], [3,-1], [2,-1], [1,-1], [0,-1], [0,-2], [0,-3]]
        car_yellow_speed = [1,1,1,1,1,1,1,1]

        def get_car_state(car_color):
            t = int(t_tracker.get_value())
            match car_color:
                case 'green':
                    [x,y]=car_green_route[t]
                    v = car_green_speed[t]
                    return [x,y,v]
        

        # --- CLEAN STATE BOX FOR GREEN CAR ---
        box_margin = 2
        box_height = 2.5
        box_width = 3.5
        box = Rectangle(
            height=box_height, width=box_width, stroke_color=WHITE, fill_opacity=0
        ).shift(RIGHT * (map_max_width + box_margin), RIGHT)

        state_text = Text("Green Car State", font_size=36)

        # --- Live-updating Texts ---
        def make_updating_value(index):
            def updater(mob):
                val = get_car_state('green')[index]
                mob.text = f"{val:.0f}"
                mob.become(Text(mob.text, font_size=36).move_to(mob.get_center()))
            return updater

        green_x_val = Text(f"{get_car_state('green')[0]:.0f}", font_size=36)
        green_y_val = Text(f"{get_car_state('green')[1]:.0f}", font_size=36)
        green_v_val = Text(f"{get_car_state('green')[2]:.0f}", font_size=36)

        green_x_val.add_updater(make_updating_value(0))
        green_y_val.add_updater(make_updating_value(1))
        green_v_val.add_updater(make_updating_value(2))

        green_X = VGroup(Text("X =", font_size=36), green_x_val).arrange(RIGHT, buff=0.2)
        green_Y = VGroup(Text("Y =", font_size=36), green_y_val).arrange(RIGHT, buff=0.2)
        green_V = VGroup(Text("V =", font_size=36), green_v_val).arrange(RIGHT, buff=0.2)

        box_text = VGroup(state_text, green_X, green_Y, green_V).arrange(DOWN, buff=0.3)
        box_text.scale_to_fit_width(box_width * 0.9)
        box_text.move_to(box.get_center())

        self.add(box, box_text)


        # Total number of steps (based on route length)
        num_steps = len(car_green_route) - 1
        # Animate t_tracker across steps (so car state updates over time)
        self.play(t_tracker.animate.set_value(num_steps), run_time=num_steps, rate_func=linear)

        # Animate cars
        for (gx, gy), (ox, oy), (bx, by), (yx, yy) in zip(car_green_route[1:], car_orange_route[1:], car_blue_route[1:], car_yellow_route[1:]):
            self.play(
                car_green.animate.move_to([gx*ts, gy*ts, 0]),
                car_orange.animate.move_to([ox*ts, oy*ts, 0]),
                car_blue.animate.move_to([bx*ts, by*ts,0]),
                car_yellow.animate.move_to([yx*ts, yy*ts,0])
            )
        self.wait(1)

