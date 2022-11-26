import pygame
from game import Game
from interface_button import Interface_button
from menu import Menu
from sys import platform as _sys_platform
from os import environ
import time
from head import Head

pygame.init()
window = pygame.display.set_mode((1280, 720))
fps_font = pygame.font.SysFont("arial",30)
clock = pygame.time.Clock()
fps = 60


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('win32', 'win64', 'cygwin'):
        return "win"

def display_fps(dt):
    fps_text = fps_font.render(str(dt), False, (0, 0, 0))
    pygame.draw.rect(window,"white",fps_text.get_rect())
    window.blit(fps_text, (0, 0))


def main():
    platform_used = platform()
    path = ""
    if platform_used == "android":
        path = "/data/data/org.test.pygame/files/app/"

    running = True
    in_game = False
    gradient = pygame.surface.Surface((5, 5))
    gradient.fill((100, 100, 100))
    for row in range(1, 4):
        for col in range(1, 4):
            if row != 2 or col != 2:
                gradient.set_at((col, row), (150, 150, 150))
    gradient.set_at((2, 2), (200, 200, 200))
    gradient = pygame.transform.smoothscale(gradient, window.get_size())
    gradient.blit(pygame.transform.scale(pygame.image.load(path+"media/cave.jpg").convert(),gradient.get_size()),(0,0))
    game = Game(window, path, gradient)
    menu = Menu(window, path, gradient)
    before = time.time()
    icon = pygame.image.load(path+"media/icon.png")
    pygame.display.set_icon(icon)

    window.blit(gradient,(0,0))
    while running:
        clock.tick(fps)
        dt = (time.time() - before) * fps
        before = time.time()
        if dt > 5:
            dt = 5.0
        display_fps(clock.get_fps())
        pygame.display.flip()
        #window.blit(gradient,(0,0))
        if in_game:
            msg = game.update(dt)
            if msg == 'end':
                in_game = False
                menu.state = 6
                game.music.stop()
                game.music.play(game.menu_music, -1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.FINGERMOTION and event.finger_id == game.buttons[game.action_button]:
                        print(f"moving finger of x: {event.dx * window.get_width()}, y: {event.dy * window.get_height()}")
                        game.finger_on_aim[1] = game.finger_on_aim[1] + event.dx * window.get_width()
                        game.finger_on_aim[2] = game.finger_on_aim[2] + event.dy * window.get_height()

                elif event.type == pygame.FINGERDOWN:
                    print(f"finger-down : {event.finger_id}")
                    x, y = event.x * window.get_width(), event.y * window.get_height()
                    for button in game.buttons_interface:
                        if button.rect.collidepoint(x, y):
                            print(f"Clicking on button {button.name} with finger {event.finger_id}")
                            button.click(True,window,game.offset)
                            game.buttons[button] = event.finger_id
                            if button == game.button_up:
                                if game.player_or_head:  # If player is moving
                                    game.player.jump()
                                else:  # If head is moving
                                    game.head.jump()
                            elif button == game.action_button:
                                game.finger_on_aim = [True,x,y]

                elif event.type == pygame.FINGERUP:
                    x, y = event.x * window.get_width(), event.y * window.get_height()
                    finger_id = event.finger_id
                    print(f"finger-up : {event.finger_id}")
                    for value in game.buttons.items():
                        if value[1] is not False and value[1] == finger_id:
                            print(f"Releasing touch on button {value[0].name}")
                            if value[0] == game.action_button and game.player_or_head:
                                game.finger_on_aim[0] = False
                                if game.distance > game.action_button.rect.w/2 and game.arms_available > 0:
                                    game.player.launch_arm(game.arms_direction)
                                    game.arms_available -= 1
                            game.buttons[value[0]] = False
                            value[0].click(False,window,game.offset)
                    if game.pause_button.rect.collidepoint(x, y):
                        in_game = False
                        menu.state = 4
                        window.blit(gradient,(0,0))
                        game.music.stop()
                        game.music.play(game.menu_music,-1)
                    elif game.reset_button.rect.collidepoint(x, y):
                        game.restart()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #if game.action_button.rect.collidepoint(event.pos):
                    #    game.action_button.click(True)
                    #if game.action2_button.rect.collidepoint(event.pos):
                    #    game.action2_button.click(True)
                    pass

                elif event.type == pygame.MOUSEBUTTONUP:
                    if game.action_button.clicking:
                        game.action_button.click(False,window,game.offset)
                        if game.player_or_head:
                            if game.arms_available > 0 and game.finger_on_aim[0] is False:
                                if game.distance > game.action_button.rect.w/2 and not game.buttons[game.action_button]:
                                    game.player.launch_arm(game.arms_direction)
                                    game.arms_available -= 1
                        else:
                            for button in game.buttons_in_game:
                                if game.head.hitbox.colliderect(button):
                                    button.on = not button.on
                                    button.image = button.images[button.on]
                                    for num in button.num:
                                        for door in game.door_sprites:
                                            if num == door.num:
                                                door.opened = not door.opened
                                                game.opened_door_sprites.add(door)
                                                game.door_sprites.remove(door)
                                                game.rects_to_update.append(door.rect)
                                                break
                                        else:
                                            for door in game.opened_door_sprites:
                                                if num == door.num:
                                                    door.opened = not door.opened
                                                    game.door_sprites.add(door)
                                                    game.opened_door_sprites.remove(door)
                                                    game.sprites_to_update.append(door)
                                                    break
                                            for laser in game.laser_sprites:
                                                if num == laser.num:
                                                    laser.opened = not laser.opened
                                                    game.opened_laser_sprites.add(laser)
                                                    game.laser_sprites.remove(laser)
                                                    game.rects_to_update.append(laser.rect)
                                                    break
                                            else:
                                                for laser in game.opened_laser_sprites:
                                                    if num == laser.num:
                                                        laser.opened = not laser.opened
                                                        game.laser_sprites.add(laser)
                                                        game.opened_laser_sprites.remove(laser)
                                                        game.sprites_to_update.append(laser)
                                                        break
                            for vent in game.vent_sprites:
                                if game.head.hitbox.colliderect(vent.rect):
                                    game.head.pos = pygame.Vector2(vent.dest[0]-10, vent.dest[1]-12)
                                    game.head.rect.x,game.head.rect.y = round(game.head.pos.x),round(game.head.pos.y)
                                    game.head.fall(dt,game)
                                    break
                    if game.action2_button.clicking:
                        game.action2_button.click(False,window,game.offset)
                        if game.player_or_head:
                            game.head = Head(pygame.Vector2(game.player.pos.x,game.player.pos.y), game.map, game.tile_size, game.window, game.path,
                                             game.collidable_sprites, [game.head_sprite],game.player.speed,game)
                            game.player.state = f"without_head_{game.arms_available}"
                            game.player_or_head = not game.player_or_head
                            game.action_button.image = game.action_button.images_with_head["head"]
                            game.action_button.button_state = True
                            window.blit(game.action_button.image, game.action_button.rect)
                        else:
                            if pygame.sprite.collide_mask(game.player, game.head):
                                game.head.kill()  # Alternate between player and head
                                game.player_or_head = not game.player_or_head
                                game.action_button.image = game.action_button.images_with_head["body"]
                                game.action_button.button_state = False
                                window.blit(game.action_button.image, game.action_button.rect)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        game.button_left.click(True,window,game.offset)
                        game.buttons[game.button_left] = True
                    elif event.key == pygame.K_d:
                        game.buttons[game.button_right] = True
                        game.button_right.click(True,window,game.offset)
                    elif event.key == pygame.K_w:
                        game.buttons[game.button_up] = True
                        game.button_up.click(True,window,game.offset)
                        if game.player_or_head:  # If player is moving
                            game.player.jump()
                        else:  # If head is moving
                            game.head.jump()
                    elif event.key == pygame.K_ESCAPE:
                        game.buttons[game.pause_button] = True
                        game.pause_button.click(True,window,game.offset)
                    if event.key == pygame.K_r:
                        if game.player_or_head:
                            game.head = Head(pygame.Vector2(game.player.pos.x,game.player.pos.y), game.map, game.tile_size, game.window, game.path,
                                             game.collidable_sprites, [game.head_sprite],game.player.speed,game)
                            game.player.state = f"without_head_{game.arms_available}"
                            game.player_or_head = not game.player_or_head
                            game.action_button.image = game.action_button.images_with_head["head"]
                            game.action_button.button_state = True
                            window.blit(game.action_button.image, game.action_button.rect)

                        else:
                            if pygame.sprite.collide_mask(game.player, game.head):
                                game.head.kill()  # Alternate between player and head
                                game.player_or_head = not game.player_or_head
                                game.action_button.image = game.action_button.images_with_head["body"]
                                game.action_button.button_state = False
                                window.blit(game.action_button.image, game.action_button.rect)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        game.button_left.click(False,window,game.offset)
                        game.buttons[game.button_left] = False
                    elif event.key == pygame.K_d:
                        game.buttons[game.button_right] = False
                        game.button_right.click(False,window,game.offset)
                    elif event.key == pygame.K_w:
                        game.buttons[game.button_up] = False
                        game.button_up.click(False,window,game.offset)

                    elif event.key == pygame.K_ESCAPE:
                        game.buttons[game.pause_button] = False
                        game.pause_button.click(False,window,game.offset)
                        in_game = False
                        menu.state = 4
                        game.music.stop()
                        game.music.play(game.menu_music,-1)
            #print(f"the events are handled in {pygame.time.get_ticks()-timing} ms")

        else:
            #game.player.running_player(game, dt)
            #game.blit_player(game.player_spritesheet, dt)
            menu.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.state == 1:
                        if menu.play_button.rect.collidepoint(event.pos):
                            menu.play_button.click(True,window,[0,0])
                        if menu.options_button.rect.collidepoint(event.pos):
                            menu.options_button.click(True,window,[0,0])
                        if menu.quit_button.rect.collidepoint(event.pos):
                            menu.quit_button.click(True,window,[0,0])
                    if menu.state == 2:
                        if menu.back_button.rect.collidepoint(event.pos):
                            menu.back_button.click(True,window,[0,0])
                        else:
                            a = 1
                            for level in menu.levels_buttons:
                                if level.rect.collidepoint(event.pos):
                                    level.click(True,window,[0,0])
                                a += 1

                    if menu.state == 3:
                        if menu.back_button.rect.collidepoint(event.pos):
                            menu.back_button.click(True,window,[0,0])
                        if menu.sound_icon_rect.collidepoint(event.pos):
                            menu.sound_clicked = True
                    if menu.state == 4:
                        if menu.resume_button.rect.collidepoint(event.pos):
                            menu.resume_button.click(True,window,[0,0])
                        if menu.menu_button.rect.collidepoint(event.pos):
                            menu.menu_button.click(True,window,[0,0])
                    if menu.state == 6:
                        menu.state = 1

                if event.type == pygame.MOUSEBUTTONUP:
                    if menu.state == 1:
                        if menu.play_button.clicking:
                            menu.play_button.click(False,window,[0,0])
                            if menu.play_button.rect.collidepoint(event.pos):
                                menu.state = 2
                                window.blit(gradient, (0, 0))
                        if menu.options_button.clicking:
                            menu.options_button.click(False, window, [0, 0])
                            if menu.options_button.rect.collidepoint(event.pos):
                                menu.state = 3
                                window.blit(gradient,(0,0))
                        if menu.quit_button.clicking:
                            menu.quit_button.click(False, window, [0, 0])
                            if menu.quit_button.rect.collidepoint(event.pos):
                                running = False
                                pygame.quit()

                    if menu.state == 2:
                        if menu.back_button.clicking:
                            menu.back_button.click(False,window,[0,0])
                            if menu.back_button.rect.collidepoint(event.pos):
                                menu.state = 1
                        else:
                            a = 1
                            level_deselected = None
                            for level in menu.levels_buttons:
                                level: Interface_button
                                if level.clicking:
                                    level_deselected = level
                                    if level.rect.collidepoint(event.pos):
                                        in_game = True
                                        level.click(False, window, [0, 0])
                                        game.music.stop()
                                        game.music.play(game.level_music,-1)
                                        game.level = a
                                        game.restart()
                                a += 1
                            if not in_game and level_deselected is not None:
                                level_deselected.click(False,window,[0,0])

                    if menu.state == 3:
                        if menu.back_button.clicking:
                            menu.back_button.click(False,window,[0,0])
                            if menu.back_button.rect.collidepoint(event.pos):
                                menu.state = 1
                        if menu.sound_clicked:
                            if menu.sound_icon_rect.collidepoint(event.pos):
                                menu.sound_clicked = False
                                menu.sound_state = not menu.sound_state
                                if menu.sound_state:
                                    game.music.set_volume(0.5)
                                else:
                                    game.music.set_volume(0)
                                window.blit(gradient, (0, 0))
                                window.blit(menu.back_button.image, menu.back_button.rect)
                    if menu.state == 4:
                        if menu.resume_button.clicking:
                            if menu.resume_button.rect.collidepoint(event.pos):
                                in_game = True
                                menu.resume_button.click(False, window, [0, 0])
                                game.blit_whole_level()
                                game.music.stop()
                                game.music.play(game.level_music, -1)
                            else:
                                menu.resume_button.click(False, window, [0, 0])
                        if menu.menu_button.clicking:
                            menu.menu_button.click(False, window, [0, 0])
                            if menu.menu_button.rect.collidepoint(event.pos):
                                menu.state = 1
                    if menu.state == 5:
                        menu.state = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE and menu.state == 4:
                        in_game = True
                        game.music.stop()
                        game.music.play(game.level_music, -1)


if __name__ == "__main__":
    main()
