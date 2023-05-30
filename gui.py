import pygame as pg
from button import Button, CheckBox
from colours import BLACK, WHITE, RED, GREEN, BLUE
import particle

# ---------- Initialisation ---------- #
WIDTH, HEIGHT = 800, 600

box = [250, 750, 50, 550]
particle_list = []

pause_button = Button(50, 50, 120, 40, "Pause/Play", 3, 24, text_mult=0.15, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
ideal_check = CheckBox(140, 250, 25, "Ideal", 3, 24, text_mult=1.8, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
clear_button = Button(50, 120, 120, 40, "Clear", 3, 24, text_mult=0.3, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
create_button = Button(50, 500, 120, 40, "Create", 3, 24, text_mult=0.25, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))
#Number of Particles
#Temperature Options
highlight_button = CheckBox(140, 350, 25, "Highlight", 3, 24, text_mult=3, border_colour=WHITE, fill_colour=(30, 30, 40), hover_colour=(60, 60, 80))

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
        elif clear_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN:
            particle_list.clear()
        elif create_button.check_over(m_x, m_y) and event.type == pg.MOUSEBUTTONDOWN and len(particle_list) == 0:
            particle_count = 100
            ave_vel = 30
            mass = 1
            radius = 5
            hl = RED if highlight_button.checked else BLUE
            particle_list = particle.generate_gas(particle_count, [350, 650, 150, 450], ave_vel, ideal_check.checked, BLUE, hl)

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

    pg.display.flip()
    # -------------------------------- #

    # ---------- Updates ----------- #
    if not paused:
        particle.update_positions(particle_list, box, delta)
    # -------------------------------- #