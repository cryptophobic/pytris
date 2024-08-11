from typing import List

import pygame
from pygame.joystick import JoystickType


class Gamepads:
    def __init__(self):
        self.__joysticks: List[JoystickType] = []
        pygame.joystick.init()
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.__joysticks.append(joy)

    def pressed(self, button):
        button -= 2000
        for joystick in self.__joysticks:
            if 0 <= button < joystick.get_numbuttons() and joystick.get_button(button):
                return True

        return False
