import random
import math
import noise
import cairo


class Canvas:
    def __init__(self, width: int, height: int, border_thickness: int, generate_planet: bool=True):
        self.image_width = width
        self.image_height = height
        self.border_thickness = border_thickness
        self.generate_planet = generate_planet

        self.image = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image_width, self.image_height)
        self.canvas = cairo.Context(self.image)
        self.offset = random.randint(1, 100) * random.randint(1, 1000)
        self.cloud_offset = random.randint(1, 100) * random.randint(1, 1000)
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

        self.planet_radius_pix = random.randint(250, 450)
        # 250
        print(self.planet_radius_pix)

        self.terrain_scale = random.randint(75, 1000)

        # 250
        print(self.terrain_scale)

        self.cloud_scale = random.randint(175, 320)

        # 175
        print(self.cloud_scale)

        self.octaves = 6
        self.persistence = .5
        self.lacunarity = 2.0
        self.base = 0
        self.max_distance = 900.0
        self.planet_number_high = 1
        self.planet_number_wide = 1
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

    def generate_perlin_noise(self, x: int, y: int, scale: float, offset: int):
        noise_val = noise.pnoise2((x+offset)/scale,
                                  (y+offset)/scale,
                                  octaves=20,
                                  persistence=0.5,
                                  lacunarity=2,
                                  repeatx=self.image_width,
                                  repeaty=self.image_height,
                                  base=0)
        return noise_val


    def generate_terrain(self):
        for width in range(0, self.image_width):
            for height in range(0, self.image_height):
                # good function
                distance_from_center = math.sqrt(math.pow((width - self.image_width//2), 2) + math.pow((height - self.image_height//2), 2))
                if distance_from_center < self.planet_radius_pix:
                # if 1:
                    noise_val = self.generate_perlin_noise(x=width, y=height, scale=self.terrain_scale, offset=self.offset)
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
                    elif noise_val < 0.105:
                        self.canvas.set_source_rgba(236/255, 230/255, 200/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.123:
                        self.canvas.set_source_rgba(126/255, 123/255, 103/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.135:
                        self.canvas.set_source_rgba(109/255, 113/255, 86/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.145:
                        self.canvas.set_source_rgba(120/255, 123/255, 100/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.15:
                        self.canvas.set_source_rgba(117/255, 132/255, 94/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.17:
                        self.canvas.set_source_rgba(104/255, 115/255, 87/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.2:
                        self.canvas.set_source_rgba(75/255, 94/255, 63/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.231:
                        self.canvas.set_source_rgba(76/255, 97/255, 63/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.26:
                        self.canvas.set_source_rgba(73/255, 93/255, 64/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.28:
                        self.canvas.set_source_rgba(74/255, 94/255, 65/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.3:
                        self.canvas.set_source_rgba(129/255, 129/255, 122/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.32:
                        self.canvas.set_source_rgba(141/255, 137/255, 130/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.34:
                        self.canvas.set_source_rgba(154/255, 150/255, 143/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.35:
                        self.canvas.set_source_rgba(116/255, 112/255, 102/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.37:
                        self.canvas.set_source_rgba(112/255, 114/255, 109/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    elif noise_val < 0.38:
                        self.canvas.set_source_rgba(175/255, 176/255, 173/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()
                    else:
                        self.canvas.set_source_rgba(255/255, 255/255, 255/255, 1)
                        self.canvas.rectangle(width, height, 1, 1)
                        self.canvas.fill()

    def render_ice_caps(self, screenx: int, screeny: int, icewidth: int, iceheight: int):
        icewidth = self.planet_radius_pix * 2
        iceheight = self.planet_radius_pix * 2
        screenx = (self.image_width // 2) - icewidth // 2
        screeny = (self.image_height // 2) - iceheight // 2
        for x in range(0, icewidth):
            for y in range(0, iceheight):
                # good function
                distance_from_center = math.sqrt(math.pow((x - icewidth//2), 2) + math.pow((y - iceheight//2), 2))
                # if distance_from_center < icewidth // 2:
                if 1:
                    noise_val = self.generate_perlin_noise(x=x + icewidth, y=y + iceheight, scale=self.terrain_scale, offset=self.offset) + 0.5
                    sin_x = math.sin(((x / icewidth)) * (math.pi))
                    sin_y = math.sin((y / iceheight) * (math.pi))

                    sin_val = (1 - sin_y) * sin_x
                    noise_val = (sin_val * 1) * (noise_val * 2)

                    self.canvas.set_source_rgba(noise_val, noise_val, noise_val, noise_val)
                    self.canvas.rectangle(x+screenx, y+screeny, 1, 1)
                    self.canvas.fill()


    def generate_clouds(self):
        for width in range(0, self.image_width):
            for height in range(0, self.image_height):
                distance_from_center = math.sqrt(math.pow((width - self.image_width//2), 2) + math.pow((height - self.image_height//2), 2))
                if distance_from_center < self.planet_radius_pix:
                    noise_val = self.generate_perlin_noise(x=width, y=height, scale=self.cloud_scale, offset=self.cloud_offset)
                    self.canvas.set_source_rgba(255/255, 255/255, 255/255, noise_val*1.65)
                    self.canvas.rectangle(width, height, 1, 1)
                    self.canvas.fill()


    # def draw_ice_cap(self, width: int, height: int):
    #     noise_val = self.generate_perlin_noise(x=width, y=height, scale=self.terrain_scale, offset=self.offset)
    #     if noise_val < 0:
    #         self.canvas.set_source_rgba(255/255, 255/255, 255/255, 1)
    #         self.canvas.rectangle(width, height, 1, 1)
    #         self.canvas.fill()
    #     elif noise_val < 0.1:
    #         self.canvas.set_source_rgba(234/255, 238/255, 243/255, 1)
    #         self.canvas.rectangle(width, height, 1, 1)
    #         self.canvas.fill()
    #     elif noise_val < 0.2:
    #         self.canvas.set_source_rgba(195/255, 201/255, 208/255, 1)
    #         self.canvas.rectangle(width, height, 1, 1)
    #         self.canvas.fill()
    #     else:
    #         self.canvas.set_source_rgba(194/255, 198/255, 201/255, 1)
    #         self.canvas.rectangle(width, height, 1, 1)
    #         self.canvas.fill()


if __name__ == "__main__":
    c = Canvas(width=1500, height=1100, border_thickness=50)
    c.draw_background()
    # c.draw_stars()
    c.generate_terrain()
    c.render_ice_caps(10, 10, 200, 200)
    # c.generate_clouds()
    # c.draw_border()
    c.save()
