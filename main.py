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
        self.offset = random.randint(1, 100) * random.randint(1, 1000)
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

        self.planet_size = 500

        self.scale = 175.0
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
                    star_size = random.choice([1, 1, 1, 1, 1, 1, 1, 2])
                    self.canvas.arc(width, height, star_size, 0, 2*math.pi)
                    self.canvas.set_source_rgba(star_col[0] / 255, star_col[1] / 255, star_col[2] / 255, random.random())
                    self.canvas.fill()

    def save(self):
        self.image.write_to_png('Examples/test.png')

    def noise_test(self):
        for width in range(0, self.image_width):
            for height in range(0, self.image_height):
                # octaves = sharpness
                noise_val = noise.pnoise2((width+self.offset)/self.scale,
                                          (height+self.offset)/self.scale,
                                          octaves=20,
                                          persistence=0.5,
                                          lacunarity=2,
                                          repeatx=self.image_width,
                                          repeaty=self.image_height,
                                          base=0)
                # print(noise_val)

                if noise_val < -0.263:
                    self.canvas.set_source_rgba(8/255, 30/255, 75/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.23:
                    self.canvas.set_source_rgba(8/255, 34/255, 80/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.197:
                    self.canvas.set_source_rgba(8/255, 34/255, 80/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.164:
                    self.canvas.set_source_rgba(9/255, 38/255, 84/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.131:
                    self.canvas.set_source_rgba(9/255, 38/255, 84/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.098:
                    self.canvas.set_source_rgba(11/255, 42/255, 90/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.065:
                    self.canvas.set_source_rgba(11/255, 46/255, 94/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < -0.032:
                    self.canvas.set_source_rgba(11/255, 48/255, 99/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.001:
                    self.canvas.set_source_rgba(11/255, 46/255, 97/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.034:
                    self.canvas.set_source_rgba(23/255, 68/255, 102/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.067:
                    self.canvas.set_source_rgba(44/255, 103/255, 128/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.1:
                    self.canvas.set_source_rgba(95/255, 157/255, 152/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                #
                elif noise_val < 0.123:
                    self.canvas.set_source_rgba(126/255, 123/255, 103/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.146:
                    self.canvas.set_source_rgba(109/255, 113/255, 86/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.169:
                    self.canvas.set_source_rgba(120/255, 123/255, 100/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.192:
                    self.canvas.set_source_rgba(117/255, 132/255, 94/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.215:
                    self.canvas.set_source_rgba(104/255, 115/255, 87/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.238:
                    self.canvas.set_source_rgba(75/255, 94/255, 63/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.261:
                    self.canvas.set_source_rgba(76/255, 97/255, 63/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.284:
                    self.canvas.set_source_rgba(73/255, 93/255, 64/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.307:
                    self.canvas.set_source_rgba(74/255, 94/255, 65/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.33:
                    self.canvas.set_source_rgba(129/255, 129/255, 122/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.353:
                    self.canvas.set_source_rgba(141/255, 137/255, 130/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.376:
                    self.canvas.set_source_rgba(154/255, 150/255, 143/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.38:
                    self.canvas.set_source_rgba(116/255, 112/255, 102/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.39:
                    self.canvas.set_source_rgba(112/255, 114/255, 109/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                elif noise_val < 0.4:
                    self.canvas.set_source_rgba(175/255, 176/255, 173/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()
                else:
                    self.canvas.set_source_rgba(255/255, 255/255, 255/255, 1)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()




if __name__ == "__main__":
    c = Canvas(width=1100, height=1500, border_thickness=50)
    c.draw_background()
    # c.draw_stars()
    c.noise_test()
    c.draw_border()
    c.save()
