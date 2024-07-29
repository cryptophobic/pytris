import pygame


class Timer:
    def __init__(self):
        self.__last_timestamp = pygame.time.get_ticks()
        self.__delta_time = 0

    def tick(self):
        current_timestamp = pygame.time.get_ticks()
        self.__delta_time = current_timestamp - self.__last_timestamp
        self.__last_timestamp = current_timestamp

    @property
    def delta_time(self):
        return self.__delta_time

    @property
    def last_timestamp(self):
        return self.__last_timestamp

    @staticmethod
    def current_timestamp():
        return pygame.time.get_ticks()
