from threading import Thread
from multiprocessing import Process
from time import sleep
import pygame


class BGMusicThread(Thread):

    def run(self):
        while True:
            mu = 'music/gamestart.wav'
            pygame.mixer.init()
            pygame.mixer.music.load(mu)
            pygame.mixer.music.play(5)
            sleep(50)
        pygame.mixer.quit()


class ShotMusicThread(Thread):

    def run(self):
        mu = 'music/fire.wav'
        pygame.mixer.init()
        pygame.mixer.music.load(mu)
        pygame.mixer.music.play(1)
        sleep(0.2)
        pygame.mixer.quit()


class BooMusicThread(Thread):

    def run(self):
        for _ in range(2):
            mu = 'tank_music.mp3'
            pygame.mixer.init()
            pygame.mixer.music.load(mu)
            pygame.mixer.music.play(5, 6.28)
            sleep(0.25)
        pygame.mixer.quit()


