from application.game.Player import Player
from application.game.State.Desk import Desk
from application.game.objects import shapes
from application.game.vectors import Vec2


class Movement:
    def __init__(self, desk: Desk):
        self.desk = desk

    def rotate(self, player, with_mass) -> tuple[bool, int]:
        rotated_shape = shapes.rotate(player.body.shape.shape, player.body.rotate)
        player.body.rotate = 0
        objects_to_move = self.desk.get_obstacles_on_position(
            player.name, rotated_shape, player.body.coordinates)
        is_place_available = 0 <= objects_to_move.mass <= with_mass

        if not is_place_available:
            return False, -1

        # for moveable_object in objects_to_move.objects:
        #     moveable_object_velocity = moveable_object.body.velocity
        #     is_place_available, mass = self.move(moveable_object, with_mass - moveable_object.body.mass)
        #     moveable_object.body.velocity = moveable_object_velocity
        #     if not is_place_available:
        #         return False, mass

        self.desk.set_new_position(player, player.body.coordinates, rotated_shape)

        return True, objects_to_move.mass

    def move(self, player, with_mass: int = 0) -> tuple[bool, int]:
        player_body_velocity = player.body.velocity
        place = player.body.coordinates + player_body_velocity
        player.body.velocity = Vec2(0, 0)

        objects_to_move = self.desk.get_obstacles_on_position(player.name, player.body.shape.shape, place)
        is_place_available = 0 <= objects_to_move.mass <= with_mass

        if not is_place_available:
            return False, -1

        if is_place_available:
            for moveable_object in objects_to_move.objects:
                moveable_object_velocity = moveable_object.body.velocity
                moveable_object.body.velocity = player_body_velocity
                is_place_available, mass = self.move(moveable_object, with_mass - moveable_object.body.mass)
                moveable_object.body.velocity = moveable_object_velocity
                if not is_place_available:
                    return False, mass

        self.desk.set_new_position(player, place, player.body.shape.shape)

        return True, with_mass - objects_to_move.mass

    def apply(self, player: Player) -> tuple[bool, bool]:
        possibly_grounded = False
        applied = False

        if player.body.velocity.is_dirty():
            to = player.body.velocity
            push_mass = player.body.mass
            last_velocity = Vec2(0, 0)
            for possible_velocity in Vec2(0, 0).iterate_to(to):
                player_velocity = possible_velocity - last_velocity
                player.body.velocity = player_velocity
                last_velocity = possible_velocity
                [is_moved, push_mass] = self.move(player, with_mass=push_mass)
                applied |= is_moved

                if not is_moved:
                    possibly_grounded = player_velocity.y > 0
                    break

        if player.body.rotate != 0:
            rotate = player.body.rotate
            direction = 1 if rotate > 0 else -1
            push_mass = 0
            for _ in range(0, rotate, direction):
                player.body.rotate = direction
                [is_rotated, push_mass] = self.rotate(player, with_mass=push_mass)
                applied |= is_rotated
                if not is_rotated:
                    break

        return applied, possibly_grounded



