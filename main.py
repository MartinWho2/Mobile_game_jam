import pygame
from game import Game
from menu import Menu
from sys import platform as _sys_platform
from os import environ
import time
from head import Head

pygame.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
fps = 60


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('win32', 'win64', 'cygwin'):
        return "win"

def display_fps(dt):
    fps_text = pygame.font.SysFont("arial",30).render(str(round(60 / dt, 3)), False, (0, 0, 0))
    window.blit(fps_text, (0, 0))


def main():
    platform_used = platform()
    path = ""
    if platform_used == "android":
        path = "/data/data/org.test.pygame/files/app/"

    running = True
    in_game = False
    game = Game(window, path)
    menu = Menu(window, path)
    before = time.time()
    time.sleep(0.1)

    while running:
        clock.tick(fps)
        dt = (time.time() - before) * fps
        before = time.time()
        if dt > 5:
            dt = 5.0
        display_fps(dt)
        pygame.display.flip()
        window.fill((255, 255, 255))
        if in_game:
            game.update(dt)
            timing = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

                elif event.type == pygame.FINGERDOWN:
                    print(f"finger-down : {event.finger_id + 1}")
                    finger_id = event.finger_id + 1
                    x, y = event.x * window.get_width(), event.y * window.get_height()
                    for button in game.buttons_interface:
                        if button.rect.collidepoint(x, y):
                            print(f"Clicking on button {button.name} with finger {event.finger_id}")
                            button.click(True)
                            game.buttons[button] = finger_id

                elif event.type == pygame.FINGERUP:
                    x, y = event.x * window.get_width(), event.y * window.get_height()
                    finger_id = event.finger_id + 1
                    print(f"finger-up : {event.finger_id + 1}")
                    for value in game.buttons.items():
                        if value[1] == finger_id:
                            print(f"Releasing touch on button {value[0].name}")
                            game.buttons[value[0]] = False
                            value[0].click(False)

                            if game.pause_button.rect.collidepoint(x, y):
                                in_game = False
                                menu.state = 4
                            if game.reset_button.rect.collidepoint(x, y):
                                game.restart()
                            if game.button_up.rect.collidepoint(x,y):
                                if game.player_or_head:  # If player is moving
                                    game.player.jump()
                                else:  # If head is moving
                                    game.head.jump()
                elif event.type == pygame.FINGERMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game.action_button.rect.collidepoint(event.pos):
                        game.action_button.click(True)
                    if game.action2_button.rect.collidepoint(event.pos):
                        game.action2_button.click(True)
                    if game.reset_button.rect.collidepoint(event.pos):
                        game.restart()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if game.action_button.clicking:
                        game.action_button.click(False)
                        if game.player_or_head:
                            if game.arms_available > 0:
                                if game.distance > game.action_button.rect.w/2:
                                    game.player.launch_arm(game.arms_direction)
                                    game.arms_available -= 1
                        else:
                            for vent in game.vent_sprites:
                                if game.head.rect.colliderect(vent.rect):
                                    game.head.pos = pygame.Vector2(vent.dest[0], vent.dest[1])
                    if game.action2_button.clicking:
                        game.action2_button.click(False)
                        if game.player_or_head:
                            game.head = Head(pygame.Vector2(game.player.pos.x,game.player.pos.y), game.map, game.tile_size, game.window, game.path,
                                             game.collidable_sprites, [game.head_sprite])
                            game.player.state = f"without_head_{game.arms_available}"
                            game.player_or_head = not game.player_or_head

                        else:
                            if pygame.sprite.collide_mask(game.player, game.head):
                                game.head.kill()  # Alternate between player and head
                                game.player_or_head = not game.player_or_head

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        game.button_left.click(True)
                        game.buttons[game.button_left] = True
                    elif event.key == pygame.K_d:
                        game.buttons[game.button_right] = True
                        game.button_right.click(True)
                    elif event.key == pygame.K_w:
                        game.buttons[game.button_up] = True
                        game.button_up.click(True)
                        if game.player_or_head:  # If player is moving
                            game.player.jump()
                        else:  # If head is moving
                            game.head.jump()
                    elif event.key == pygame.K_ESCAPE:
                        game.buttons[game.pause_button] = True
                        game.pause_button.click(True)
                    if event.key == pygame.K_r:
                        if game.player_or_head:
                            game.head = Head(pygame.Vector2(game.player.pos.x,game.player.pos.y), game.map, game.tile_size, game.window, game.path,
                                             game.collidable_sprites, [game.head_sprite])
                            game.player.state = f"without_head_{game.arms_available}"
                            game.player_or_head = not game.player_or_head

                        else:
                            if pygame.sprite.collide_mask(game.player, game.head):
                                game.head.kill()  # Alternate between player and head
                                game.player_or_head = not game.player_or_head

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        game.button_left.click(False)
                        game.buttons[game.button_left] = False
                    elif event.key == pygame.K_d:
                        game.buttons[game.button_right] = False
                        game.button_right.click(False)
                    elif event.key == pygame.K_w:
                        game.buttons[game.button_up] = False
                        game.button_up.click(False)

                    elif event.key == pygame.K_ESCAPE:
                        game.buttons[game.pause_button] = False
                        game.pause_button.click(False)
                        in_game = False
                        menu.state = 4
            #print(f"the events are handled in {pygame.time.get_ticks()-timing} ms")

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
                    if menu.state == 4:
                        if menu.resume_button.rect.collidepoint(event.pos):
                            menu.resume_button.click(True)
                        if menu.menu_button.rect.collidepoint(event.pos):
                            menu.menu_button.click(True)

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
                                        game.restart()
                                    level.click(False)
                                a += 1

                    if menu.state == 3:
                        if menu.back_button.clicking:
                            if menu.back_button.rect.collidepoint(event.pos):
                                menu.state = 1
                            menu.back_button.click(False)

                    if menu.state == 4:
                        if menu.resume_button.clicking:
                            if menu.resume_button.rect.collidepoint(event.pos):
                                in_game = True
                            menu.resume_button.click(False)
                        if menu.menu_button.clicking:
                            if menu.menu_button.rect.collidepoint(event.pos):
                                menu.state = 1
                            menu.menu_button.click(False)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE and menu.state == 4:
                        in_game = True


if __name__ == "__main__":
    main()
