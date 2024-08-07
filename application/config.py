from application.game.Player import Player
from application.game.controls import wasd, uldr, tfgh

INITIAL_SPEED_OF_FALLING_DOWN = 1000
FPS = 60

SCREEN_SIZE = (600, 800)
DESK_HEIGHT = 40
DESK_WIDTH = 30
SQUARE_BLOCK = False
BLOCK_HEIGHT = SCREEN_SIZE[1] / DESK_HEIGHT
BLOCK_WIDTH = SCREEN_SIZE[0] / DESK_WIDTH
if SQUARE_BLOCK:
    BLOCK_WIDTH = BLOCK_WIDTH if BLOCK_WIDTH < BLOCK_HEIGHT else BLOCK_HEIGHT
    BLOCK_HEIGHT = BLOCK_WIDTH


players = [
    Player(name='player1', controls=uldr, speed=2.5, color=(100, 150, 0)),
    Player(name='player2', controls=wasd, speed=1.8, color=(150, 100, 0)),
    Player(name='player3', controls=tfgh, speed=1, color=(0, 100, 150))
]
