import pygame


class Events:
    def __init__(self):
        self.subscribers = None

    def subscribe(self, subscriber: str, keys_to_track_down: tuple, keys_to_track_pressed: tuple):
        self.subscribers[subscriber] = {
            'keys_to_track_pressed': {key: [] for key in keys_to_track_pressed},
            'keys_to_track_down': {key: [] for key in keys_to_track_down}
        }

    def unsubscribe(self, subscriber: str):
        if subscriber in self.subscribers:
            del self.subscribers[subscriber]

    def listen(self):
        pressed = pygame.key.get_pressed()
        for subscriber in self.subscribers:
            for event in pressed[subscriber]:

