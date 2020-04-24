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

    def save(self):
        self.image.write_to_png('Examples/test.png')




def main():

    scale = 500.0
    octaves = 6
    persistence = .5
    lacunarity = 2.0
    base = 0
    max_distance = 900.0
    planet_number_high = 1
    planet_number_wide = 1
    planet_size = 1500
    border_thickness = 50


    draw_border(canvas=canvas, thickness=border_thickness, width=image_width, height=image_height)

    image.write_to_png('Examples/test.png')


    offset = random.randint(1, 100) * random.randint(1, 1000)


    colors_list = [(127, 199, 175), (218, 216, 167), (167, 219, 216), (237, 118, 112)]

    # for col in range(pil_image.size[0]):
    #     for row in range(pil_image.size[1]):
    #         pixels[col, row] = (208, 200, 176)

    # for col in range(0, pil_image.size[0], planet_size):
    #     for row in range(0, pil_image.size[1], planet_size):
    #         color_water = random.choice(colors_list)
    #         color_ground = random.choice(colors_list)
    #         while color_ground is color_water:
    #             color_ground = random.choice(colors_list)
    #         other_color = random.choice(colors_list)
    #         while other_color is color_water or other_color is color_ground:
    #             other_color = random.choice(colors_list)
    #         for i in range(col, col+planet_size):
    #             for j in range(row, row+planet_size):
    #
    #                 # Generates a value from -1 to 1
    #                 pixel_value = noise.pnoise2((offset+i)/scale,
    #                                             (offset+j)/scale,
    #                                             octaves,
    #                                             persistence,
    #                                             lacunarity,
    #                                             width,
    #                                             height,
    #                                             base)
    #                 distance_from_center = math.sqrt(math.pow((i - (col+(col+planet_size))/2), 2) + math.pow((j - (row+(row+planet_size))/2), 2))
    #
    #                 if (distance_from_center < max_distance):
    #                     if (other_color == 1 and int(pixel_value * 100.0) > 25):
    #                         pixels[i, j] = other_color
    #                     elif (int(pixel_value * 100.0) > 5):
    #                         pixels[i, j] = color_ground
    #                     else:
    #                         pixels[i, j] = color_water
    #                 elif (distance_from_center < (max_distance + .03 * max_distance)):
    #                     pixels[i, j] = (15, 15, 15)



if __name__ == "__main__":
    c = Canvas(width=1100, height=1500, border_thickness=50)
    c.draw_background()
    c.draw_border()
    c.save()