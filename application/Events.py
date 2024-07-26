from typing import Dict


class Events:
    def __init__(self):
        self.subscribers = None

    def subscribe(self, subscriber: str, keys_to_track_down: tuple, keys_to_track_pressed: tuple):
        self.subscribers[subscriber] = {
            'keys_to_track_pressed': {key: 0 for key in keys_to_track_pressed},
            'keys_to_track_down': {key: {'down': None, 'up': None} for key in keys_to_track_down}
        }


