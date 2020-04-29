import math
import random
import noise


class WorldGen:
    def __init__(self, width: int, height: int):
        """
        :param width: of the image in pixels
        :param height: of the image in pixels
        """
        self.image_width = width
        self.image_height = height

        #  Ensure planet can't be larger than the image
        if self.image_height > self.image_width:
            half_width = self.image_width // 2
            self.planet_radius = random.randint(150, half_width - (half_width // 3))
        else:
            half_height = self.image_height // 2
            self.planet_radius = random.randint(150, half_height - (half_height // 3))

        self.planet_diameter = self.planet_radius * 2
        self.planet_start_x = (self.image_width // 2) - self.planet_radius  # offset to start of planet on x axis
        self.planet_start_y = (self.image_height // 2) - self.planet_radius  # offest to start of planet on y axis

        self.atmosphere_diameter = int(self.planet_diameter * 1.8)  # must be bigger to give visible atmosphere
        self.atmosphere_start_x = (self.image_width // 2) - (self.atmosphere_diameter // 2)
        self.atmosphere_start_y = (self.image_height // 2) - (self.atmosphere_diameter // 2)
        self.atmosphere_thickness = random.randint(0, 3)  # how much atmosphere is visible outside the earth

        self.octaves = 60  # level of detail in perlin noise
        self.persistence = .5  # keep below 1 or generate random noise
        self.lacunarity = random.choice([2.0, 2.2, 2.4, 2.6, 2.8,
                                         3.0, 3.2, 3.4, 3.6, 3.8])  # higher = more granular terrain (above 5 code breaks)
        self.offset = random.randint(1, 100) * random.randint(1, 1000)
        self.terrain_scale = random.randint(75, 250)  # generate random scale (higher = more zoomed out)
        self.cloud_scale = random.randint(150, 320)

        #  given a noise value, extract the relevant colour to generate realistic looking terrain
        self.noise_to_col_map_terrain = {-0.263: (8, 30, 75),
                                         -0.197: (8, 34, 80),
                                         -0.164: (9, 38, 84),
                                         -0.098: (11, 42, 90),
                                         -0.065: (11, 46, 92),
                                         -0.032: (11, 48, 99),
                                         0.001: (11, 46, 97),
                                         0.034: (23, 68, 102),
                                         0.067: (44, 103, 128),
                                         0.1: (95, 157, 152),
                                         0.105: (236, 230, 200),
                                         0.123: (126, 123, 103),
                                         0.135: (109, 113, 86),
                                         0.145: (120, 123, 100),
                                         0.15: (117, 132, 94),
                                         0.17: (104, 114, 87),
                                         0.2: (75, 94, 63),
                                         0.231: (76, 97, 63),
                                         0.26: (73, 93, 64),
                                         0.28: (74, 94, 65),
                                         0.3: (129, 129, 122),
                                         0.32: (141, 137, 130),
                                         0.34: (154, 150, 143),
                                         0.35: (116, 112, 102),
                                         0.37: (112, 114, 109),
                                         0.38: (175, 176, 173),
                                         0.38000001: (255, 255, 255)}

        self.noise_to_ice_age = {-0.3463: (8, 30, 75),
                                 -0.34: (8, 34, 80),
                                 -0.32: (9, 38, 84),
                                 -0.3: (11, 42, 90),
                                 -0.2: (11, 46, 92),
                                 -0.1:  (11, 56, 99),
                                 -0.07:  (11, 73, 99),
                                 -0.05: (150, 165, 174),
                                 0.00: (189, 195, 202),
                                 0.01: (199, 210, 217),
                                 0.05: (222, 231, 233),
                                 0.07: (228, 237, 243),
                                 0.09: (233, 241, 249),
                                 0.11: (237, 245, 254),
                                 0.13: (240, 249, 254),
                                 0.14: (228, 237, 243),
                                 0.19: (245, 253, 254),
                                 0.21: (248, 254, 255),
                                 0.23: (254, 254, 254)}

        self.noise_to_col_ice = {0.69: (95, 157, 152),
                                 0.7: (150, 165, 174),
                                 0.71: (189, 195, 202),
                                 0.72: (199, 210, 217),
                                 0.743: (222, 231, 233),
                                 0.79: (228, 237, 243),
                                 0.81: (233, 241, 249),
                                 0.85: (237, 245, 254),
                                 0.9: (240, 249, 254),
                                 0.93: (245, 253, 254),
                                 0.96: (248, 254, 255),
                                 0.99: (254, 254, 254)}

    def generate_perlin_noise(self, x: int, y: int, scale: float):
        noise_val = noise.pnoise2((x+self.offset)/scale,
                                  (y+self.offset)/scale,
                                  octaves=self.octaves,
                                  persistence=self.persistence,
                                  lacunarity=self.lacunarity,
                                  repeatx=self.image_width,
                                  repeaty=self.image_height,
                                  base=0)
        return noise_val

    def gen_terrain(self, x: int, y: int):
        """
        Generate noise for the terrain and return relevant colour
        """
        noise_val = self.generate_perlin_noise(x=x, y=y, scale=self.terrain_scale)
        chosen_key = -99999
        for key in self.noise_to_col_map_terrain:
            if noise_val > chosen_key:
                chosen_key = key
        return self.noise_to_col_map_terrain[chosen_key]

    def gen_ice_age(self, x: int, y: int):
        """
        Generate noise for the ice age and return relevant colour
        """
        noise_val = self.generate_perlin_noise(x=x, y=y, scale=self.terrain_scale)
        chosen_key = -99999
        for key in self.noise_to_ice_age:
            if noise_val > chosen_key:
                chosen_key = key
        return self.noise_to_ice_age[chosen_key]

    def gen_ice_caps(self, x, y, strength):
        """
        Generate noise for the ice caps and return relevant colour
        """
        #  generate sin waves that pos peak in the middle of the planet
        sin_x = math.sin((x / self.planet_diameter) * math.pi)  # vertical gradient
        sin_y = math.sin((y / self.planet_diameter) * math.pi)  # horizontal gradient

        sin_x = sin_x + 0.3  # make the white gradient span a larger range
        sin_y = 1.3 - sin_y  # inverse (but make a little stronger, so the white appears at the top of the planet)

        sin_val = sin_y * sin_x  # generate a gradient that resembles polar ice caps

        ice_cap_power = strength  # increase to make lengthier caps, decrease to reduce
        noise_val = self.generate_perlin_noise(x=x, y=y, scale=self.terrain_scale)
        noise_val = noise_val + ice_cap_power

        # multiply together to get noise that matches our pole gradients
        noise_val = sin_val * noise_val

        chosen_key = 0.689
        for key in self.noise_to_col_ice:
            if noise_val > chosen_key:
                chosen_key = key
        if chosen_key != 0.689:
            return self.noise_to_col_ice[chosen_key]

    def gen_clouds(self, x, y, cloud_strength: int):
        """
        Generate noise for the clouds, return noise value
        """
        noise_val = self.generate_perlin_noise(x=x, y=y, scale=self.cloud_scale)
        cloud_power = noise_val * cloud_strength
        return cloud_power

    def gen_atmosphere(self, x, y, strength):
        """
        Generate sin waves to generate a circle gradient over the atmosphere diameter
        """
        #  generate sin waves that pos peak in the middle of the atmosphere
        sin_x = math.sin((x / self.atmosphere_diameter) * math.pi)
        sin_y = math.sin((y / self.atmosphere_diameter) * math.pi)
        sin_val = sin_y * sin_x
        sin_val = sin_val / strength
        return sin_val

    def gen_shadow(self, x, y, strength):
        """
        Generate sin waves to generate a circle gradient over the atmosphere diameter
        Minus 1 to invert the strength (set white to black for the shadow)
        """
        sin_x = math.sin((x / self.atmosphere_diameter) * math.pi) / strength
        sin_y = math.sin((y / self.atmosphere_diameter) * math.pi)
        sin_val = 1 - (sin_y * sin_x)
        return sin_val * 7
