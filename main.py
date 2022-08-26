import pygame
from game import Game
from menu import Menu
from sys import platform as _sys_platform
from os import environ

pygame.init()
window = pygame.display.set_mode((1280,720))


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('win32','win64','cygwin'):
        return "win"


def main():
    platform_used = platform()
    path = ""
    if platform_used == "android":
        path = "/data/data/org.test.pygame/files/app/"

    running = True
    in_game = False
    game = Game(window, path)
    menu = Menu(window, path)
    while running:
        pygame.display.flip()
        window.fill((0, 0, 0))
        if in_game:
            game.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.FINGERDOWN:
                    print(f"finger-down : {event.finger_id+1}")
                    finger_id = event.finger_id+1

                #elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.x*window.get_width(), event.y* window.get_height()
                    for button in game.buttons_interface:
                        if button.rect.collidepoint(x, y):
                            print(f"Clicking on button {button.name} with finger {event.finger_id}")
                            button.click(True)
                            game.buttons[button] = finger_id
                #elif event.type == pygame.MOUSEBUTTONUP:
                elif event.type == pygame.FINGERUP:
                    x, y = event.x * window.get_width(), event.y * window.get_height()
                    finger_id = event.finger_id+1
                    print(f"finger-up : {event.finger_id+1}")
                    for value in game.buttons.items():
                        if value[1] == finger_id:
                            print(f"Releasing touch on button {value[0].name}")
                            game.buttons[value[0]] = False
                            value[0].click(False)

                            if game.pause_button.rect.collidepoint(x, y):
                                in_game = False
                                menu.state = 4

        else:
            menu.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.state == 1:
                        if menu.play_button.rect.collidepoint(event.pos):
                            menu.play_button.click(True)
                        if menu.options_button.rect.collidepoint(event.pos):
                            menu.options_button.click(True)
                        if menu.quit_button.rect.collidepoint(event.pos):
                            menu.quit_button.click(True)
                    if menu.state == 2:
                        if menu.back_button.rect.collidepoint(event.pos):
                            menu.back_button.click(True)
                        else:
                            a = 1
                            for level in menu.levels_buttons:
                                if level.rect.collidepoint(event.pos):
                                    level.click(True)
                                a += 1

                    if menu.state == 3:
                        if menu.back_button.rect.collidepoint(event.pos):
                            menu.back_button.click(True)
                if event.type == pygame.MOUSEBUTTONUP:
                    if menu.state == 1:
                        if menu.play_button.clicking:
                            if menu.play_button.rect.collidepoint(event.pos):
                                menu.state = 2
                            menu.play_button.click(False)
                        if menu.options_button.clicking:
                            if menu.options_button.rect.collidepoint(event.pos):
                                menu.state = 3
                            menu.options_button.click(False)
                        if menu.quit_button.clicking:
                            if menu.quit_button.rect.collidepoint(event.pos):
                                running = False
                                pygame.quit()
                            menu.quit_button.click(False)
                    if menu.state == 2:
                        if menu.back_button.clicking:
                            if menu.back_button.rect.collidepoint(event.pos):
                                menu.state = 1
                            menu.back_button.click(False)
                        else:
                            a = 1
                            for level in menu.levels_buttons:
                                if level.clicking:
                                    if level.rect.collidepoint(event.pos):
                                        in_game = True
                                        game.level = a
                                        print(game.level)
                                    level.click(False)
                                a += 1

                    if menu.state == 3:
                        if menu.back_button.clicking:
                            if menu.back_button.rect.collidepoint(event.pos):
                                menu.state = 1
                            menu.back_button.click(False)


if __name__ == "__main__":
    main()
