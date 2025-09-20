from manim import *

class Traffic(MovingCameraScene):
    def construct(self):
        # --- GLOBAL SETTINGS ---
        self.camera.background_color = "#c3c3c3"

        # Sample tile to measure size 
        sample_tile = SVGMobject("traffic/street_2.svg")
        ts = sample_tile.width  # tile size in manim units

        tile_map = {
            "traffic/street_2.svg": [[0, 0, 0], [3 , 0, 0], [1,1,90]],
            "traffic/house-blue.svg": [[2 , 0,0]],
            "traffic/street_4.svg": [[4, 0,0], [0,1,0]],
        }


        # Adjust camera to fit everything
        self.camera.frame.set_width(5*ts*2)

        # Place backgroung tiles
        for filename, positions in tile_map.items():
            for pos in positions:
                x, y, rot = pos
                tile = SVGMobject(filename)
                tile.move_to([x*ts,y*ts,0])
                tile.rotate(rot * DEGREES)
                self.add(tile)


