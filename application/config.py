from application.game.Player import Player
from application.game.controls import wasd, uldr, tfgh

INITIAL_SPEED_OF_FALLING_DOWN = 1000
FPS = 60

SCREEN_SIZE = (400, 800)
DESK_HEIGHT = 30
DESK_WIDTH = 15
SQUARE_BLOCK = False
BLOCK_HEIGHT = SCREEN_SIZE[1] / DESK_HEIGHT
BLOCK_WIDTH = SCREEN_SIZE[0] / DESK_WIDTH
if SQUARE_BLOCK:
    BLOCK_WIDTH = BLOCK_WIDTH if BLOCK_WIDTH < BLOCK_HEIGHT else BLOCK_HEIGHT
    BLOCK_HEIGHT = BLOCK_WIDTH

BORDERS_WIDTH = BLOCK_WIDTH // 15
BORDERS_HEIGHT = BLOCK_HEIGHT // 15
print(BLOCK_WIDTH)


players = [
    Player(name='player1', controls=uldr, speed=1),
    Player(name='player2', controls=wasd, speed=1),
    Player(name='player3', controls=tfgh, speed=1)
]
