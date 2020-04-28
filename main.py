from canvas import ImageCanvas
from world_gen import WorldGen
import math
import random


def render_stars():
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            distance_from_center = math.sqrt(math.pow((x - WIDTH//2), 2) + math.pow((y - HEIGHT//2), 2))
            if distance_from_center > world.planet_radius + world.atmosphere_thickness:
                canvas.draw_star(x, y)


def render_shadow():
    # draw shadow, again cant move this inside the above loop as for some reason the atomosphere draws over the shadow
    draw_shadow_decider = random.random()
    for x in range(0, world.atmosphere_diameter):
        for y in range(0, world.atmosphere_diameter):
            if canvas.distance_from_image_center(x=x+world.atmosphere_start_x,
                                                 y=y+world.atmosphere_start_y) < world.atmosphere_diameter:
                alpha = world.gen_shadow(x, y)
                if draw_shadow_decider >= 0.5:
                    # draw on right side
                    canvas.draw_pixel((x+world.atmosphere_start_x)-(world.atmosphere_diameter / 5),
                                      y+world.atmosphere_start_y,
                                      0, 0, 0,
                                      alpha)
                else:
                    # draw on left side
                    canvas.draw_pixel((x+world.atmosphere_start_x)+(world.atmosphere_diameter / 5),
                                      y+world.atmosphere_start_y,
                                      0, 0, 0,
                                      alpha)


def render_atmosphere():
    # draw atmosphere (cant figure out how to put it in the single loop as sin waves need larger diameter)
    for x in range(0, world.atmosphere_diameter):
        for y in range(0, world.atmosphere_diameter):
            if canvas.distance_from_image_center(x=x+world.atmosphere_start_x, y=y+world.atmosphere_start_y) < world.planet_radius + world.atmosphere_thickness:
                sin_val = 1 - world.gen_atmosphere(x, y)
                canvas.draw_pixel(x+world.atmosphere_start_x, y+world.atmosphere_start_y, 200, 200, 200, sin_val)


def main_render_loop():
    for x in range(0, world.planet_diameter):
        for y in range(0, world.planet_diameter):
            planet_offset_x = x + world.planet_start_x
            planet_offset_y = y + world.planet_start_y

            if canvas.distance_from_image_center(x=planet_offset_x, y=planet_offset_y) < world.planet_radius:
                #  draw terrain surface

                if not ICE_AGE:
                    col = world.gen_terrain(x=x, y=y)
                    canvas.draw_pixel(planet_offset_x, planet_offset_y, col[0], col[1], col[2], 1)

                    # draw ice caps
                    col = world.gen_ice_caps(x, y)
                    if col:  # only draw if we are given a colour for the poles
                        canvas.draw_pixel(planet_offset_x, planet_offset_y, col[0], col[1], col[2], 1)

                if ICE_AGE:
                    col = world.gen_ice_age(x, y)
                    if col:  # only draw if we are given a colour for the poles
                        canvas.draw_pixel(planet_offset_x, planet_offset_y, col[0], col[1], col[2], 1)

                #  draw clouds
                col = world.gen_clouds(x, y)
                canvas.draw_pixel(planet_offset_x, planet_offset_y, 255, 255, 255, col)


def render_and_save():
    canvas.fill_background()
    main_render_loop()
    render_atmosphere()
    render_shadow()
    render_stars()
    if DRAW_BORDER:
        canvas.draw_border()
    canvas.save_image_png()


if __name__ == '__main__':
    WIDTH = 640
    HEIGHT = 1136

    DRAW_BORDER = True
    ICE_AGE = True

    world = WorldGen(WIDTH, HEIGHT)

    canvas = ImageCanvas(WIDTH, HEIGHT)
    render_and_save()
