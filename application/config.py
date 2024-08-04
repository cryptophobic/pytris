from application.game.Player import Player
from application.game.controls import wasd, uldr, tfgh

INITIAL_SPEED_OF_FALLING_DOWN = 1000
FPS = 60

players = [
    Player(name='player1', controls=wasd, speed=1.5, color=(100, 150, 0)),
    Player(name='player2', controls=uldr, speed=2.1, color=(150, 100, 0)),
    Player(name='player3', controls=tfgh, speed=1.8, color=(0, 100, 150))
]
