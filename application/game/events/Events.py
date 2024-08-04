import pygame
from application.Timer import Timer
from typing import Dict, Tuple, List
from dataclasses import dataclass
from application.game.controls import MoveControls
from application.game.events.Scheduler import Scheduler


@dataclass
class KeyPressLogRecord:
    dt: int
    down: bool


@dataclass
class KeyPressLog:
    down: bool
    log: List[KeyPressLogRecord]
    subscribers: int


class Events:

    flush = 10000

    def __init__(self):
        self.scheduler = Scheduler()
        self.subscribers: Dict[str, Tuple] = {}
        self.key_map: Dict[int, KeyPressLog] = {}
        self.keys_down: List[int] = []
        self.next_flush = Timer.current_timestamp() + Events.flush

    def subscribe(self, subscriber: str, keys: MoveControls):

        if subscriber in self.subscribers:
            return False

        for key in keys.keys():
            if self.key_map.get(key) is None:
                self.key_map[key] = KeyPressLog(down=False, subscribers=0, log=[])
            self.key_map[key].subscribers += 1

        self.subscribers[subscriber] = tuple(keys.keys())

        return True

    def unsubscribe(self, subscriber: str):
        if subscriber not in self.subscribers:
            return False

        for key in self.subscribers[subscriber]:
            if key not in self.key_map:
                continue

            if self.key_map[key].subscribers == 1:
                del self.key_map[key]
                continue

            self.key_map[key].subscribers -= 1

    def listen(self, ticks: int):
        pressed = pygame.key.get_pressed()

        for idx, key in enumerate(self.keys_down):

            if key not in self.key_map:
                self.keys_down.pop(idx)
                continue

            if not pressed[key] and not self.scheduler.is_pressed(key):
                self.key_map[key].down = False
                self.key_map[key].log.append(KeyPressLogRecord(dt=ticks, down=False))
                self.keys_down.pop(idx)

        for key, events_log in self.key_map.items():
            if (pressed[key] or self.scheduler.is_pressed(key)) and events_log.down is not True:
                self.key_map[key].down = True
                self.key_map[key].log.append(KeyPressLogRecord(dt=ticks, down=True))
                self.keys_down.append(key)

    def slice(self, start: int, end: int) -> Dict[int, List[KeyPressLog]]:

        local_keymap = self.key_map

        if Timer.current_timestamp() > self.next_flush:
            self.next_flush = Timer.current_timestamp() + Events.flush
            self.key_map = {
                key: KeyPressLog(
                    down=value.down,
                    log=list(filter(lambda timestamp: (end <= timestamp.dt), value.log)),
                    subscribers=value.subscribers
                )
                for key, value in local_keymap.items()
            }

        return {
            key:
                list(filter(lambda log_entry: (start <= log_entry.dt < end), value.log))
            for key, value in local_keymap.items()
        }
