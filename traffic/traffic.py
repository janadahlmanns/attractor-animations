from manim import *

class Traffic(MovingCameraScene):
    def construct(self):
        # --- GLOBAL SETTINGS ---
        self.camera.background_color = "#8bc08c"

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

        # Adjust camera to fit everything
        self.camera.frame.set_height(7*ts)
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
        car_orange_route=[[3,-3],[3,-4], [4,-4], [5,-4], [6,-4], [7,-4], [20,-4], [20,-4]]
        car_blue_route = [[3,-2], [3,-1], [2,-1],[1,-1], [0,-1], [0, 0],[0,20],[0,20],[0,20]]
        car_yellow_route = [[3,10], [3,10], [3,0], [3,-1], [2,-1], [1,-1], [0,-1], [0,-2], [0,-3]]


        # Animate cars
        for (gx, gy), (ox, oy), (bx, by), (yx, yy) in zip(car_green_route[1:], car_orange_route[1:], car_blue_route[1:], car_yellow_route[1:]):
            self.play(
                car_green.animate.move_to([gx*ts, gy*ts, 0]),
                car_orange.animate.move_to([ox*ts, oy*ts, 0]),
                car_blue.animate.move_to([bx*ts, by*ts,0]),
                car_yellow.animate.move_to([yx*ts, yy*ts,0])
            )

