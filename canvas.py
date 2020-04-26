import cairo
import math
import time
from world_gen import WorldGen


class ImageCanvas:
    def __init__(self, width: int, height: int, world: WorldGen):
        self.image_width = width
        self.image_height = height
        self.image = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image_width, self.image_height)
        self.canvas = cairo.Context(self.image)
        self.border_thickness = 50
        self.world = world

    def set_colour(self, r: int, g: int, b: int, a: float=1):
        self.canvas.set_source_rgba(r/255, g/255, b/255, a)

    def draw_pixel(self, x: int, y: int, r: int, g: int, b: int, a: float):
        self.set_colour(r, g, b, a)
        self.canvas.rectangle(x, y, 1, 1)
        self.canvas.fill()

    def fill_background(self, r: int=0, g: int=0, b: int=0):
        self.canvas.set_source_rgb(r/255, g/255, b/255)
        self.canvas.paint()

    def draw_border(self, r: int=255, g: int=255, b: int=255):
        border_right_start_x = self.image_width-self.border_thickness
        border_bottom_start_x = self.image_height-self.border_thickness
        self.set_colour(r=r, g=g, b=b)
        self.canvas.rectangle(0, 0, self.border_thickness, self.image_width)  # left
        self.canvas.rectangle(border_right_start_x, 0, self.border_thickness, self.image_height)  # right
        self.canvas.rectangle(0, border_bottom_start_x, self.image_width, self.border_thickness)  # bottom
        self.canvas.rectangle(0, 0, self.image_width, self.border_thickness)  # top
        self.canvas.fill()

    def save_image_png(self):
        self.image.write_to_png('{}.png'.format(time.strftime("%d%m%Y-%H%M%S")))

    def render_loop(self):
        for x in range(0, self.image_width):
            for y in range(0, self.image_height):
                if self.distance_from_image_center(x=x, y=y) < self.world.planet_radius:
                    # col = self.world.gen_terrain(x=x, y=y)
                    # self.draw_pixel(x, y, col[0], col[1], col[2], 1)

                    ice = self.world.render_ice_caps(x=x, y=y)
                    if ice:
                        self.draw_pixel(x, y, ice[0], ice[1], ice[2], 1)

    def distance_from_image_center(self, x: int, y: int):
        return math.sqrt(math.pow((x - self.image_width//2), 2) + math.pow((y - self.image_height//2), 2))


if __name__ == '__main__':
    WIDTH = 1920
    HEIGHT = 1080

    world = WorldGen(WIDTH, HEIGHT)
    canvas = ImageCanvas(WIDTH, HEIGHT, world=world)
    canvas.fill_background()
    canvas.render_loop()
    canvas.save_image_png()
