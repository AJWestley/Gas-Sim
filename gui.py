import pygame as pg
from button import Button, CheckBox, TextInput, IntensityButton
from colours import BLACK, WHITE, RED, GREEN, BLUE
import particle
from collisions import SpatialHashMap

# ---------- Initialisation ---------- #
WIDTH, HEIGHT = 800, 600

pause_button = Button(50, 50, 120, 40, "Pause/Play", 3, 24, text_mult=0.15, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
clear_button = Button(50, 120, 120, 40, "Clear", 3, 24, text_mult=0.3, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
particle_num_input = TextInput(85, 250, 80, 35, "Number of particles:", 3, 24, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
ideal_check = CheckBox(140, 300, 25, "Ideal:", 3, 24, text_mult=2, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
highlight_button = CheckBox(140, 350, 25, "Highlight:", 3, 24, text_mult=3.3, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
particle_radius_button = IntensityButton(100, 400, 65, 25, "Size:", [4, 8], ["small", "large"], 3, 24, text_mult=0.8, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
particle_speed_button = IntensityButton(100, 450, 65, 25, "Temp:", [10, 30], ["cold", "warm"], 3, 24, text_mult=0.8, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
create_button = Button(50, 500, 120, 40, "Create", 3, 24, text_mult=0.25, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))

box = [250, 750, 50, 550]
particle_list = []
particle_map = SpatialHashMap(box, 9)

pg.init()
pg.display.set_caption('Gas Simulation')
screen = pg.display.set_mode((WIDTH, HEIGHT))

delta = 100
running = True
paused = True
clock = pg.time.Clock()
screen.fill((20, 20, 20))
# ------------------------------------ #

# ------------------------------------ #

while running:
    clock.tick(delta)

    # -------- Event Handling -------- #
    m_x, m_y = pg.mouse.get_pos()

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
        elif pause_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            paused = not paused
        elif ideal_check.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            ideal_check.checked = not ideal_check.checked
        elif highlight_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            highlight_button.checked = not highlight_button.checked
        elif particle_num_input.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            particle_num_input.active = True
        elif particle_radius_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            particle_radius_button.increment()
        elif particle_speed_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            particle_speed_button.increment()
        elif clear_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            particle_list.clear()
            for bucket in particle_map.map:
                bucket.clear()
        elif create_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN and len(particle_list) == 0:
            particle_count = int(particle_num_input.value)
            particle_radius = particle_radius_button.values[particle_radius_button.current_val]
            ave_vel = particle_speed_button.values[particle_speed_button.current_val]
            hl = RED if highlight_button.checked else BLUE
            particle_list = particle.generate_gas(particle_count, [300, 700, 100, 500], ave_vel, ideal_check.checked, BLUE, hl, radius=particle_radius)
            particle_map = SpatialHashMap(box, int(particle_radius + 1))
            for p in particle_list:
                particle_map.insert((p.x, p.y), p)
        elif event.type == pg.MOUSEBUTTONDOWN:
            particle_num_input.active = False
        elif event.type == pg.KEYDOWN and particle_num_input.active:
            if event.key == pg.K_BACKSPACE:
                particle_num_input.backspace()
            else:
                particle_num_input.add(event.unicode)

    # -------------------------------- #

    # ---------- Rendering ----------- #
    background = pg.Surface(screen.get_size())
    background.fill(BLACK)
    screen.blit(background, (0, 0))

    pg.draw.rect(screen, WHITE, (box[0]-5, box[2]-5, box[1]-box[0]+10, box[3]-box[2]+10), width=5)

    for p in particle_list:
        pg.draw.circle(screen, p.colour, (p.x, p.y), p.radius)
    
    pause_button.draw(pg, screen)
    clear_button.draw(pg, screen)
    create_button.draw(pg, screen)
    ideal_check.draw(pg, screen)
    highlight_button.draw(pg, screen)
    particle_num_input.draw(pg, screen)
    particle_radius_button.draw(pg, screen)
    particle_speed_button.draw(pg, screen)

    pg.display.flip()
    # -------------------------------- #

    # ---------- Updates ----------- #
    if not paused:
        particle_map.update_positions(box, delta)
    # -------------------------------- #