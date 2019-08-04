from time import sleep
import random
import pygame
from concurrent.futures import ThreadPoolExecutor
from config.base_config import SCREEN_SIZE, UP, DOWN, LEFT, RIGHT, SCREEN_REFRESH as sleep_time
from base.tank import Tank

screen = None

def keydown_event(tank, key):
    """
    键盘事件，按下某个键, 改变tank状态
    :param tank: 坦克
    :param key: 按键
    :return: None
    """
    global screen
    move_key = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]
    if key in move_key:
        tank.set_is_move(True)
    if key == pygame.K_w:
        tank.set_dir(UP)
    elif key == pygame.K_d:
        tank.set_dir(RIGHT)
    elif key == pygame.K_s:
        tank.set_dir(DOWN)
    elif key == pygame.K_a:
        tank.set_dir(LEFT)
    elif key == pygame.K_j:
        tank.fire(screen)
        print("fire")
    elif key == pygame.K_SPACE:
        tank.change_is_move()

def keyup_event(tank, key):
    """
    键盘事件，按下某个键, 改变tank状态
    :param tank: 坦克
    :param key: 按键
    :return: None
    """
    move_key = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]
    if key in move_key:
        tank.set_is_move(False)


def refresh_screen(tank):
    global screen
    count = 1
    while True:
        count += 1
        if count % 5000 == 0:
            print(count)
        screen.fill((0,0,1))
        tank.draw(screen)
        pygame.display.flip()
        sleep(sleep_time)

def main():
    global screen
    thread_pool = ThreadPoolExecutor(8)
    pool = []
    pygame.init()

    # 设置屏幕尺寸大小
    screen = pygame.display.set_mode(SCREEN_SIZE)
    # 设置左上角标题d
    pygame.display.set_caption('坦克大战')

    tank = Tank()
    future = thread_pool.submit(refresh_screen, tank)
    pool.append(future)

    is_running = True
    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                keydown_event(tank, event.key)
            elif event.type == pygame.KEYUP:
                keyup_event(tank, event.key)

        tank.moving()

        sleep(sleep_time)
    pygame.quit()


if __name__ == '__main__':
    main()