from dataclasses import dataclass
from typing import Dict

from application.Timer import Timer


@dataclass
class KeyEventsScheduler:
    up: int = 0
    down: int = 0
    pressed: int = 0
    interval: int = 0


class Scheduler:
    def __init__(self):
        self.schedule: Dict[int, KeyEventsScheduler] = {}
        pass

    def is_pressed(self, key: int) -> bool:
        event = self.schedule.get(key)
        res = False
        if event is None:
            return res

        current_timestamp = Timer.current_timestamp()
        if 0 < event.pressed < current_timestamp:
            event.pressed = 0 if event.interval == 0 else current_timestamp + event.interval
            res |= True

        if 0 < event.down < current_timestamp:
            res |= True if event.up == 0 or event.up > current_timestamp else False
            event.down = 0 if event.interval == 0 else current_timestamp + event.interval

        if 0 < event.up < current_timestamp:
            event.up = 0 if event.interval == 0 else current_timestamp + event.up

        if event.up == 0 and event.down == 0 and event.pressed == 0:
            self.remove_key(key)

        return res

    def schedule_key_pressed(self, ticks: int, key: int, interval: int = 0):
        self.schedule[key] = KeyEventsScheduler(pressed=ticks, interval=interval)

    def schedule_key_down(self, ticks: int, key: int, interval: int = 0):
        self.schedule[key] = KeyEventsScheduler(down=ticks, interval=interval)

    def schedule_key_up(self, ticks: int, key: int, interval: int = 0):
        self.schedule[key] = KeyEventsScheduler(up=ticks, interval=interval)

    def remove_key(self, key: int):
        self.schedule.pop(key)
