from lib import *
from read import *
from pygame_tool import *
from settings import *
import sys
import pygame
import os
import pyperclip as clp

print('Init...')
__version__ = '1.0.1'
method = 'p'
tc = ()
file = open('val.vl', mode='w')
file.write('')
file.close()

print('Using settings "settings.Settings"')
settings = Settings()
total_pixels = settings.board_width * settings.board_height

print('Init pygame...')
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '123'
pygame.init()

print('Getting screen ready...')
icon = pygame.image.load('resources\\icon.png')
screen = pygame.display.set_mode(settings.screen_size)
ver = ''
if settings.show_version:
    ver = 'v%s' % __version__
pygame.display.set_caption('荣耀画板 %s' % ver)
pygame.display.set_icon(icon)
screen_rect = screen.get_rect()

color = [(255, 255, 255) for x in range(total_pixels)]

print('Creating elements...')
board = Board(screen, width=settings.board_width, height=settings.board_height, pixel=settings.pixel_size)

color_console = ColorConsole()
color_console.rect.bottomleft = screen_rect.bottomleft

panel = SealPanel()
seal = Seal(panel.panel)

read = TriggerButton('Read', size=settings.small_button)
read.rect.right = color_console.rect.right - 10
read.rect.top = color_console.rect.top + 10

cdm = TriggerButton('Cdm', size=settings.small_button)
cdm.rect.right = color_console.rect.right - 10
cdm.rect.top = read.rect.bottom + 10

name = 'Untitled'
name_t = ActiveText(font='STKaiti', size=16)
ch_name = TriggerButton('Change', size=settings.small_button)
name_t.set_text(name)
name_t.rect.top = color_console.rect.top + 20
name_t.rect.right = color_console.rect.right - 50
ch_name.rect.top = name_t.rect.bottom
ch_name.rect.centerx = name_t.rect.centerx
clear_all = TriggerButton('Clear', size=settings.small_button)
print('Run mainloop')

while True:
    tc = hls2rgb(color_console.hue_ctrl.value, color_console.value_ctrl.value, 1.0)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if method == 's':
            panel.update(event)
            seal.seal = panel.seal
            seal.update(event)
        cdm.update(event)
        ch_name.update(event)
        read.update(event)
        board.update(event, color, method, tc)
        color_console.update(event)
        if event.type == pygame.QUIT:
            sys.exit()

    board.blit(screen, color)
    color_console.compose()
    color_console.blit(screen, tc)
    cdm.compose()
    read.compose()
    read.blit(screen)
    name_t.set_text(name)
    name_t.rect.top = color_console.rect.top + 20
    name_t.rect.right = color_console.rect.right - 50
    name_t.blit(screen)
    ch_name.compose()
    ch_name.blit(screen)
    cdm.blit(screen)
    seal.blit(screen)
    if method == 's':
        panel.blit(screen, color_console.seal_sw.rect.right + 10, color_console.rect.top + 10)
    if ch_name.status:
        name = ask_and_get_val()
        ch_name.status = False
    if read.status:
        code = ask_and_get_val()
        if len(code) >= 2:
            result = decode(code, total_pixels)
            if result:
                color_code, seal_code, name = result
                color = ColorCode(color_code).to_rgb()
                seal.seals.clear()
                for num, pos in seal_code:
                    seal.create_seal(num, pos[0], pos[1])
        read.status = False
    if cdm.status:
        save_code = encode(color, seal.seals, name)
        clp.copy(save_code)
        cdm.status = False
    pygame.display.flip()

    if color_console.eraser_sw.button.status:
        method = 'e'
    elif color_console.seal_sw.button.status:
        method = 's'
    else:
        method = 'p'
