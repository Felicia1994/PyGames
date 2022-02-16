import pygame
print(pygame.ver)
from Elements import Button
from Renju import RenjuScreen
from SymbolColor import SymbolColorScreen

display_width = 1200
display_height = 640
framerate = 10

DARK = (25, 77, 25)
LIGHT = (216, 243, 216)
bg_location = 'bg.jpg'

def StartingScreen(screen, framerate):

    clock = pygame.time.Clock()

    exit_button = Button('Exit', DARK, screen, display_width*0.8, display_height*0.4, bg_color=LIGHT)
    renju_button = Button('Renju', DARK, screen, display_width*0.8, display_height*0.2, bg_color=LIGHT)
    symbolcolor_button = Button('SymbolColor', DARK, screen, display_width*0.8, display_height*0.4, bg_color=LIGHT)

    running = True
    while running:
        clock.tick(framerate)
        pygame.display.set_caption('Games')
        screen.blit(pygame.image.load(bg_location), (0,0))

        game_title = Button('Welcome!', LIGHT, screen, display_width*0.1, display_height*0.2)
        game_title.display(screen)
        if exit_button.is_clicked(pygame.mouse.get_pos()):
            exit_button = Button('Exit', LIGHT, screen, display_width*0.1, display_height*0.4)
        else:
            exit_button = Button('Exit', DARK, screen, display_width*0.1, display_height*0.4, bg_color=LIGHT)
        exit_button.display(screen)
        if renju_button.is_clicked(pygame.mouse.get_pos()):
            renju_button = Button('Renju', LIGHT, screen, display_width*0.8, display_height*0.2)
        else:
            renju_button = Button('Renju', DARK, screen, display_width*0.8, display_height*0.2, bg_color=LIGHT)
        renju_button.display(screen)
        if symbolcolor_button.is_clicked(pygame.mouse.get_pos()):
            symbolcolor_button = Button('SymbolColor', LIGHT, screen, display_width*0.8, display_height*0.4)
        else:
            symbolcolor_button = Button('SymbolColor', DARK, screen, display_width*0.8, display_height*0.4, bg_color=LIGHT)
        symbolcolor_button.display(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.is_clicked(pygame.mouse.get_pos()):
                    running = False
                    break
                if renju_button.is_clicked(pygame.mouse.get_pos()):
                    RenjuScreen(screen, framerate)
                if symbolcolor_button.is_clicked(pygame.mouse.get_pos()):
                    SymbolColorScreen(screen, framerate)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    StartingScreen(screen, framerate)
    pygame.quit()
