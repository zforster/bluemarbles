import math
import random
import noise


class WorldGen:
    def __init__(self, width: int, height: int):
        self.image_width = width
        self.image_height = height

        self.octaves = 6
        self.persistence = .5
        self.lacunarity = 2.0
        self.base = 0
        self.offset = random.randint(1, 100) * random.randint(1, 1000)

        self.planet_radius = random.randint(150, 450)

        self.planet_diameter = self.planet_radius * 2

        self.atmosphere_thickness = random.randint(0, 10)
        self.terrain_scale = random.randint(75, 250)
        self.cloud_scale = random.randint(150, 320)

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

        # self.noise_to_col_ice = {0.99: (254, 254, 254),
        #                          0.96: (248, 254, 255),
        #                          0.93: (245, 253, 254),
        #                          0.9: (240, 249, 254),
        #                          0.85: (237, 245, 254),
        #                          0.81: (233, 241, 249),
        #                          0.79: (228, 237, 243),
        #                          0.743: (222, 231, 233),
        #                          0.72: (199, 210, 217),
        #                          0.71: (189, 195, 202),
        #                          0.7: (150, 165, 174),
        #                          0.697: (95, 157, 152)}
        self.noise_to_col_ice = {0.697: (95, 157, 152),
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
                                  octaves=20,
                                  persistence=0.5,
                                  lacunarity=2,
                                  repeatx=self.image_width,
                                  repeaty=self.image_height,
                                  base=0)
        return noise_val

    def gen_terrain(self, x: int, y: int):
        noise_val = self.generate_perlin_noise(x=x, y=y, scale=self.terrain_scale)
        chosen_key = -99999
        for key in self.noise_to_col_map_terrain:
            if noise_val > chosen_key:
                chosen_key = key
        return self.noise_to_col_map_terrain[chosen_key]

    def gen_ice_caps(self, x: int, y: int):
        planet_start_x = (self.image_width // 2) - self.planet_radius // 2
        planet_start_y = (self.image_height // 2) - self.planet_radius // 2

        noise_val = self.generate_perlin_noise(x=x, y=y, scale=self.terrain_scale) + 0.7

        sin_x = math.sin((x / planet_start_x) * math.pi) * 0.7
        sin_y = math.sin((y / planet_start_y) * math.pi)

        sin_val = (1.3 - sin_y) * (sin_x + 0.3)
        noise_val = (sin_val * 1) * (noise_val * 1)

        chosen_key = 0.6969
        for key in self.noise_to_col_ice:
            if noise_val > chosen_key:
                chosen_key = key
        if chosen_key != 0.6969:
            return self.noise_to_col_ice[chosen_key]

    def render_ice_caps(self, x, y):
        sin_x = math.sin(x / self.planet_diameter)
        sin_y = math.sin(y / self.planet_diameter)
        sin_val = sin_x * sin_y
        return sin_x * 255, sin_x * 255, sin_x * 255
        # icewidth = self.planet_radius * 2
        # iceheight = self.planet_radius * 2
        # screenx = (self.image_width // 2) - icewidth // 2
        # screeny = (self.image_height // 2) - iceheight // 2
        # for x in range(0, icewidth):
        #     for y in range(0, iceheight):
        #         # good function
        #         distance_from_center = math.sqrt(math.pow((x - icewidth//2), 2) + math.pow((y - iceheight//2), 2))
        #         if distance_from_center < icewidth // 2:
        #             noise_val = self.generate_perlin_noise(x=x + icewidth, y=y + iceheight, scale=self.terrain_scale) + 0.7
        #             sin_x = math.sin(((x / icewidth)) * (math.pi)) * 0.7
        #             sin_y = math.sin((y / iceheight) * (math.pi))
        #
        #             sin_val = (1.3 - sin_y) * (sin_x + 0.3)
        #             # sin_val = 1 - (((sin_y) + (1-sin_x)) / 2)
        #             noise_val = (sin_val * 1) * (noise_val * 1)
        #
        #             if noise_val > 0.99:
        #                 return 254, 254, 254
        #             elif noise_val > 0.96:
        #                 return 248, 254, 255
        #             elif noise_val > 0.93:
        #                 return 245, 253, 254
        #             elif noise_val > 0.9:
        #                 return 240, 249, 254
        #             elif noise_val > 0.85:
        #                 return 237, 245, 254
        #             elif noise_val > 0.81:
        #                 return 233, 241, 249
        #             elif noise_val > 0.79:
        #                 return 228, 237, 243
        #             elif noise_val > 0.743:
        #                 return 222, 231, 233
        #             elif noise_val > 0.72:
        #                 return 199, 210, 202
        #             elif noise_val > 0.71:
        #                 return 189, 195, 202
        #             elif noise_val > 0.7:
        #                 return 150, 165, 174
        #             elif noise_val > 0.697:
        #                 return 95, 157, 152
