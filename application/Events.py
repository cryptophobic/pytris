import pygame
import json
from application.Timer import Timer


class Events:

    flush = 10000

    def __init__(self):
        self.subscribers = {}
        self.key_map = {}
        self.keys_down = []
        self.next_flush = Timer.current_timestamp() + Events.flush

    def subscribe(self, subscriber: str, keys: tuple):

        if subscriber in self.subscribers:
            return False

        for key in keys:
            if self.key_map.get(key) is None:
                self.key_map[key] = {
                    'down': False,
                    'subscribers': 0,
                    'log': [],
                }
            self.key_map[key]['subscribers'] += 1

        self.subscribers[subscriber] = keys

        return True

    def unsubscribe(self, subscriber: str):
        if subscriber not in self.subscribers:
            return False

        for key in self.subscribers[subscriber]:
            if key not in self.key_map:
                continue

            if self.key_map[key]['subscribers'] == 1:
                del self.key_map[key]
                continue

            self.key_map[key]['subscribers'] -= 1

    def listen(self, ticks: int):
        pressed = pygame.key.get_pressed()

        for idx, key in enumerate(self.keys_down):

            if key not in self.key_map:
                self.keys_down.pop(idx)
                continue

            if not pressed[key]:
                self.key_map[key]['down'] = False
                self.key_map[key]['log'].append([ticks, 0])
                self.keys_down.pop(idx)

        for key, events_log in self.key_map.items():
            if pressed[key] and events_log['down'] is not True:
                self.key_map[key]['down'] = True
                self.key_map[key]['log'].append([ticks, 1])
                self.keys_down.append(key)

    def slice(self, start: int, end: int):

        local_keymap = self.key_map

        if Timer.current_timestamp() > self.next_flush:
            self.next_flush = Timer.current_timestamp() + Events.flush
            self.key_map = {
                key: {
                    'down': value['down'],
                    'log': list(filter(lambda timestamp: (end <= timestamp[0]), value['log'])),
                    'subscribers': value['subscribers']}
                for key, value in local_keymap.items()}

        return {
            key:
                [list(filter(lambda timestamp: (start <= timestamp[0] < end), value['log']))]
            for key, value in local_keymap.items()
        }

