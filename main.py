from canvas import ImageCanvas
from world_gen import WorldGen
import math
import random


def render_stars():
    """
    Draw stars on the image, but avoid the planet + the atmosphere of the planet
    """
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            distance_from_center = math.sqrt(math.pow((x - WIDTH//2), 2) + math.pow((y - HEIGHT//2), 2))
            if distance_from_center > world.planet_radius + world.atmosphere_thickness:
                canvas.draw_star(x, y)


def render_shadow():
    """
    Render shadow over planet with probability of 0.66
    If random number < 0.33 draw shadow on left side, otherwise draw it on the right side
    """
    draw_shadow_decider = random.random()
    if draw_shadow_decider > 0.33:
        for x in range(0, world.atmosphere_diameter):
            for y in range(0, world.atmosphere_diameter):
                if canvas.distance_from_image_center(x=x+world.atmosphere_start_x,
                                                     y=y+world.atmosphere_start_y) < world.atmosphere_diameter:
                    alpha = world.gen_shadow(x, y, SHADOW_SPAN)
                    if draw_shadow_decider >= 0.66:
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
    """
    Draw the atmosphere over the planet
    """
    for x in range(0, world.atmosphere_diameter):
        for y in range(0, world.atmosphere_diameter):
            if canvas.distance_from_image_center(x=x+world.atmosphere_start_x, y=y+world.atmosphere_start_y) < world.planet_radius + world.atmosphere_thickness:
                sin_val = 1 - world.gen_atmosphere(x, y, ATMOSPHERE_STRENGTH)
                canvas.draw_pixel(x+world.atmosphere_start_x, y+world.atmosphere_start_y, 200, 200, 200, sin_val)


def main_render_loop():
    """
    Main loop draws three things (terrain, ice-caps, clouds) to reduce run-time
    If the user has chosen to generate an 'ice-age' earth, then skip drawing ice caps
    """
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
                    col = world.gen_ice_caps(x, y, ICE_CAP_STRENGTH)
                    if col:  # only draw if we are given a colour for the poles
                        canvas.draw_pixel(planet_offset_x, planet_offset_y, col[0], col[1], col[2], 1)

                if ICE_AGE:
                    col = world.gen_ice_age(x, y)
                    if col:  # only draw if we are given a colour for the poles
                        canvas.draw_pixel(planet_offset_x, planet_offset_y, col[0], col[1], col[2], 1)

                #  draw clouds
                col = world.gen_clouds(x, y, CLOUD_STRENGTH)
                canvas.draw_pixel(planet_offset_x, planet_offset_y, 255, 255, 255, col)


def render_and_save():
    """
    Would be more efficient to move render_atmosphere, render_shadow and render_stars into the main render loop
    but I can't figure out the maths as the atmosphere and shadow require larger radius for the sin waves

    stars must be drawn last, otherwise the shadow will draw over the stars
    """
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

    """ User Options """

    DRAW_BORDER = True  # set False if you don't want the white border around the image

    """ 
    set True to generate an 'ice-age' style earth
    If True, normal earth terrain ice caps are not generated
    'ICE_CAP_STRENGTH' does not refer to the this ice altering that will have no affect on the ice density here 
    """
    ICE_AGE = False

    CLOUD_STRENGTH = random.choice([1, 2, 3, 4])  # set lower to make clouds more transparent, set higher to make more opaque

    """ 
    setting higher generates longer ice caps, reducing generates smaller
    Only useful if ICE_AGE is False (if generating a normal non-ice-age earth)
    """
    ICE_CAP_STRENGTH = random.choice([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

    ATMOSPHERE_STRENGTH = random.choice([1, 1, 1, 1, 1.1, 1.2, 1.3, 1.4])  # higher to generate a thicker atmosphere covering the earth

    """ End User Options """

    SHADOW_SPAN = random.choice([0.4, 0.6])  # don't change these two values look realistic

    world = WorldGen(WIDTH, HEIGHT)

    canvas = ImageCanvas(WIDTH, HEIGHT)

    render_and_save()
