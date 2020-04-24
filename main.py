import random
import math
import noise
import cairo
from PIL import Image


class Canvas:
    def __init__(self, width: int, height: int, border_thickness: int):
        self.image_width = width
        self.image_height = height

        self.border_thickness = border_thickness

        self.image = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image_width, self.image_height)
        self.canvas = cairo.Context(self.image)

        # colours based on temp of real stars - https://qph.fs.quoracdn.net/main-qimg-f7d440db775a84d85a3f76b5822e9151
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

        self.scale = 500.0
        self.octaves = 6
        self.persistence = .5
        self.lacunarity = 2.0
        self.base = 0
        self.max_distance = 900.0
        self.planet_number_high = 1
        self.planet_number_wide = 1
        self.planet_size = 1500
        self.border_thickness = 50
        self.first = True

        self.offset = random.randint(1, 100) * random.randint(1, 1000)
        self.colors_list = [(127, 199, 175), (218, 216, 167), (167, 219, 216), (237, 118, 112)]

    def draw_border(self, r: int=255, g: int=255, b: int=255):
        self.canvas.set_source_rgb(r, g, b)
        # x y width height
        self.canvas.rectangle(0, 0, self.border_thickness, self.image_height)  # left
        self.canvas.rectangle(self.image_width-self.border_thickness, 0, self.border_thickness, self.image_height)  # right
        self.canvas.rectangle(0, self.image_height-self.border_thickness, self.image_width, self.border_thickness)  # bottom
        self.canvas.rectangle(0, 0, self.image_width, self.border_thickness)  # top
        self.canvas.fill()

    def draw_background(self, r: int=0, g: int=0, b: int=0):
        self.canvas.set_source_rgb(r, g, b)
        self.canvas.paint()

    def draw_stars(self):
        self.canvas.set_source_rgb(0, 0, 0)
        for width in range(0, self.image_width):
            for height in range(0, self.image_height):
                draw_star = random.random()
                if draw_star > 0.999:
                    star_col = random.choice(self.star_colours)
                    # self.canvas.rectangle(width, height, 1, 1)
                    star_size = random.choice([1, 1, 1, 1, 1, 2])
                    self.canvas.arc(width, height, star_size, 0, 2*math.pi)
                    self.canvas.set_source_rgba(star_col[0] / 255, star_col[1] / 255, star_col[2] / 255, random.random())
                    self.canvas.fill()
                    # exit(1)

    def save(self):
        self.image.write_to_png('Examples/test.png')






if __name__ == "__main__":
    c = Canvas(width=1100, height=1500, border_thickness=50)
    c.draw_background()
    c.draw_stars()
    c.draw_border()
    c.save()