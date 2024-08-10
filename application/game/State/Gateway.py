import sys
from collections import deque

from application.game.Player import Player
from application.game.State.Desk import Desk
from application.game.State.PlayersCollection import PlayersCollection
from application.game.objects.Shape import Shape
from application.game.vectors import Vec2


class Gateway:
    def __init__(self, desk: Desk, players: PlayersCollection):
        self.desk = desk
        self.players = players
        self.__gateway: deque[str] = deque()

    def enqueue(self, player: Player):
        if player.name not in self.__gateway:
            player.body.coordinates = Vec2(x=self.desk.width // 2, y=-1)
            player.idle = True
            player.body.shape = Shape()
            player.body.velocity = Vec2(0, 0)
            player.body.rotate = 0
            self.__gateway.append(player.name)

    def __len__(self):
        return len(self.__gateway)

    def let_player_go(self) -> bool:

        player: Player | None = None
        while player is None and len(self.__gateway) > 0:
            player_name = self.__gateway[0]
            player = self.players.get(player_name)

            if player is None:
                sys.stderr.write(f"Player {player_name} not found in collection.\n")
                self.__gateway.popleft()

        if player is None:
            return False

        if self.desk.add_player(player):
            player.idle = False
            self.__gateway.popleft()
            return True

        return False
