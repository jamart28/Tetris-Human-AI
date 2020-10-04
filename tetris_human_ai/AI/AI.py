from typing import List, Tuple

from attr import attrs, attrib
import pygame
from immutablecollections import ImmutableSetMultiDict, immutablesetmultidict
from more_itertools import first

from tetris_human_ai import convert_shape_format

GameState = "Tuple[Piece, Piece, List[List[Tuple[int, int, int]]]]"


def _move_left():
    return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)


def _move_right():
    return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)


def _move_down():
    return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)


def _rotate():
    return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)


@attrs
class BigBrain:
    def big_thonk(self, state: GameState) -> List[pygame.event.Event]:
        current_piece, next_piece, grid = state
        smallest_hole = ((0, 0), 11)
        continuous_hole = ((0, 0), 0)
        for i, row in enumerate(reversed(grid)):
            print(row)
            continuous_hole = ((0, i), 0)
            if (0, 0, 0) in row:
                for j, cell in enumerate(row):
                    if cell == (0, 0, 0):
                        continuous_hole = (continuous_hole[0], continuous_hole[1] + 1)
                    else:
                        if continuous_hole[1] > 0 and continuous_hole[1] < smallest_hole[1]:
                            smallest_hole = continuous_hole
                        continuous_hole = ((j, i), 0)
                break
            else:
                continue

        size_to_rotation = self._orientation_to_size(current_piece)
        actions_to_take: List[pygame.event] = []
        simulated_rotation = current_piece.rotation
        simulated_x = current_piece.x - 2
        if continuous_hole[1] in size_to_rotation:
            rotation_goal, shape_goal = first(size_to_rotation[continuous_hole[1]])
            simulated_x = min([pos_x for pos_x, _ in convert_shape_format(shape_goal)])
            while simulated_rotation != rotation_goal:
                simulated_rotation = simulated_rotation + 1 % 4
                actions_to_take.append(_rotate())  # Add Rotation Action

            while simulated_x != continuous_hole[0][0]:
                if simulated_x < continuous_hole[0][0]:
                    simulated_x = simulated_x + 1
                    actions_to_take.append(_move_right())  # Add Move Right Event
                else:
                    simulated_x = simulated_x - 1
                    actions_to_take.append(_move_left())  # Add Move Left Event

            # We should maybe move down but that seems like bonus points when we could
            # Let the game do that for us :)

            return actions_to_take

        else:
            largest_size = max(size_to_rotation.keys())
            rotation_goal = first(size_to_rotation[largest_size])
            while simulated_rotation != rotation_goal:
                simulated_rotation = simulated_rotation + 1 % 4
                actions_to_take.append(_rotate())  # Add Rotation Action

            while simulated_x != continuous_hole[0][0] + 2:
                if simulated_x < continuous_hole[0][0] + 2:
                    simulated_x = simulated_x + 1
                    actions_to_take.append(_move_right())  # Add Move Right Event
                else:
                    simulated_x = simulated_x - 1
                    actions_to_take.append(_move_left())  # Add Move Left Event

            # We should maybe move down but that seems like bonus points when we could
            # Let the game do that for us :)

            return actions_to_take

    def _orientation_to_size(self, piece: "Piece") -> ImmutableSetMultiDict[int, Tuple[int, List[str]]]:
        rotation_to_size: List[Tuple[int, Tuple[int, List[str]]]] = []
        for num, lines in enumerate(piece.shape):
            last_line = None
            for line in lines:
                if "0" in line:
                    last_line = line
            if last_line:
                count = 0
                for char in line:
                    if char == "0":
                        count = count + 1
                rotation_to_size.append((count, (num, lines)))
            else:
                raise RuntimeError("Failed to find last line of shape.")

        return immutablesetmultidict(rotation_to_size)



# def _available_positions(state: GameState):
#     for rotation in state[0].
