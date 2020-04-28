import cairo
import math
import time
import random


class ImageCanvas:
    def __init__(self, width: int, height: int):
        self.image_width = width
        self.image_height = height
        self.image = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image_width, self.image_height)
        self.canvas = cairo.Context(self.image)
        if self.image_height > self.image_width:
            self.border_thickness = self.image_width // 20
        else:
            self.border_thickness = self.image_height // 20
        self.star_colours = [(204, 217, 252),
                             (206, 215, 252),
                             (249, 247, 252),
                             (255, 253, 219),
                             (253, 244, 173),
                             (247, 211, 173),
                             (238, 106, 93),
                             (206, 216, 252),
                             (239, 239, 239),
                             (255, 255, 255),
                             (255, 255, 255),
                             (255, 255, 255),
                             (255, 255, 255),
                             (255, 255, 255),
                             (255, 255, 255),
                             (255, 255, 255),
                             ]

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
        self.canvas.rectangle(0, 0, self.border_thickness, self.image_height)  # left
        self.canvas.rectangle(border_right_start_x, 0, self.border_thickness, self.image_height)  # right
        self.canvas.rectangle(0, border_bottom_start_x, self.image_width, self.border_thickness)  # bottom
        self.canvas.rectangle(0, 0, self.image_width, self.border_thickness)  # top
        self.canvas.fill()

    def draw_star(self, x, y):
        draw_star = random.random()
        if draw_star > 0.999:
            star_col = random.choice(self.star_colours)
            star_size = 1
            self.set_colour(star_col[0], star_col[1], star_col[2], random.random())
            self.canvas.arc(x, y, star_size, 0, 2*math.pi)
            self.canvas.fill()

    def save_image_png(self):
        self.image.write_to_png('{}.png'.format(time.strftime("%d%m%Y-%H%M%S")))

    def distance_from_image_center(self, x: int, y: int):
        return math.sqrt(math.pow((x - self.image_width//2), 2) + math.pow((y - self.image_height//2), 2))
