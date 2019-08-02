from threading import Thread
from time import sleep
from Music import *

import pygame
BROWN = (160, 95, 25)
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3




class ShotMusicThread(Thread):

    def run(self):
        tank_numsic = 'tank_music.mp3'
        pygame.mixer.init()
        pygame.mixer.music.load(tank_numsic)
        pygame.mixer.music.play(5, 5.35)
        sleep(0.05)
        pygame.mixer.quit()


class BoomMusicThread(Thread):

    def run(self):
        tank_numsic = 'tank_music.mp3'
        pygame.mixer.init()
        pygame.mixer.music.load(tank_numsic)
        pygame.mixer.music.play(5)
        sleep(0.05)
        pygame.mixer.quit()







class RefreshThread(Thread):

    def __init__(self, screen, is_refresh=True):
        super().__init__()
        self.screen = screen
        self.is_refresh = is_refresh
        self.game_begin = False

    def run(self):
        """ 独立线程刷新屏幕"""

        while self.is_refresh:
            if not self.game_begin:
                bg_picture = pygame.image.load('tank2.jpg')
                self.screen.blit(bg_picture, (150, 150))
                pygame.draw.rect(self.screen, BROWN, (150, 150, 500, 300), 5)
                pygame.draw.rect(self.screen, BROWN, (309, 307, 25, 30), 3)
                self.game_begin = True
                pygame.display.flip()
                sleep(1)

                pygame.display.flip()
            self.screen.fill((0, 0, 0))
            map_picture = pygame.image.load('tank3.jpg')
            self.screen.blit(map_picture, (200, 100))
            pygame.draw.rect(self.screen, BROWN, (150, 100, 500, 420), 5)

            pygame.display.flip()
            sleep(0.05)


class TankShot(object):

    def __init__(self, pos, ndir, speed=50):
        self.pos = pos
        self.speed = speed
        self.dir = ndir

    def draw(self, screen):
        while 100 <= self.pos[0] <= 650 and 80 <= self.pos[1] <= 600:
            if self.dir == RIGHT:
                print(self.pos[0], self.pos[1])
                self.pos = self.pos[0] + self.speed, self.pos[1]
                pygame.draw.circle(screen, (255, 255, 255), self.pos, 2)

            if self.dir == DOWN:
                self.pos = self.pos[0], self.pos[1] + self.speed
                pygame.draw.circle(screen, (255, 255, 255), self.pos, 2)

            if self.dir == LEFT:
                self.pos = self.pos[0] - self.speed, self.pos[1]
                pygame.draw.circle(screen, (255, 255, 255), self.pos, 2)

            if self.dir == UP:
                self.pos = self.pos[0], self.pos[1] - self.speed
                pygame.draw.circle(screen, (255, 255, 255), self.pos, 2)



class Tank(object):

    def __init__(self, image, rect, speed=1):
        self.image = image
        self.rect = rect
        self.speed = speed
        self.dir = UP
        self.speed = speed

    def change(self, new_dir):
        self.dir = new_dir

    def attack(self, screen):
        if self.dir == UP or DOWN:
            TankShot((self.rect[0] + 15, self.rect[1]), self.dir).draw(screen)
        else:
            TankShot((self.rect[0], self.rect[1] + 15), self.dir).draw(screen)
        print(self.rect[0], self.rect[1])

    def move(self, screen):
        if self.dir == UP:
            self.rect.top -= self.speed
            if self.rect.top <= 100:
                self.rect.top = 100
        elif self.dir == RIGHT:
            self.rect.left += self.speed
            if self.rect.left >= 620:
                self.rect.left = 620
        elif self.dir == DOWN:
            self.rect.top += self.speed
            if self.rect.top >= 500:
                self.rect.top = 500
        else:
            self.rect.left -= self.speed
            if self.rect.left <= 150:
                self.rect.left = 150
        screen.blit(self.image, self.rect)


def main():

    def key_event(ekey):
        if ekey == pygame.K_w:
            tank.change(UP)
        elif ekey == pygame.K_d:
            tank.change(RIGHT)
        elif ekey == pygame.K_s:
            tank.change(DOWN)
        elif event.key == pygame.K_a:
            tank.change(LEFT)
        elif ekey == pygame.K_SPACE:
            tank.attack(screen)



    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('坦克大战')


    RefreshThread(screen).start()
    #BooMusicThread(daemon=True).start()


    rect = pygame.Rect(350, 480, 30, 30)
    tank_image = pygame.image.load('one_tank.png')#.convert()
    tank = Tank(tank_image, rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                key_event(event.key)




        tank.move(screen)
        pygame.display.flip()





    pygame.quit()


if __name__ == '__main__':
    main()