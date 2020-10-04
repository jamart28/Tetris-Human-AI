from copy import copy
from typing import List, Tuple

from attr import attrib, attrs

from immutablecollections import (
    ImmutableSet,
    ImmutableSetMultiDict,
    immutableset,
    immutablesetmultidict,
)

from tetris_human_ai import convert_shape_format

import pygame
from more_itertools import first

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
        continuous_hole = (0, 0)
        for i, row in enumerate(reversed(grid)):
            continuous_hole = (0, 0)
            if (0, 0, 0) in row:
                for j, cell in enumerate(row):
                    if cell == (0, 0, 0):
                        continuous_hole = (continuous_hole[0], continuous_hole[1] + 1)
                    else:
                        if (
                            continuous_hole[1] > 0
                            and continuous_hole[1] < smallest_hole[1]
                        ):
                            smallest_hole = continuous_hole
                        continuous_hole = (j + 1, 0)

                size_to_rotation = self._orientation_to_size(current_piece)
                actions_to_take: List[pygame.event] = []
                simulated_shape = copy(current_piece)
                if continuous_hole[1] in size_to_rotation:
                    rotation_goal = first(size_to_rotation[continuous_hole[1]])
                    while simulated_shape.rotation != rotation_goal:
                        simulated_shape.rotation = simulated_shape.rotation + 1 % 4
                        actions_to_take.append(_rotate())  # Add Rotation Action

                    simulated_x = min(
                        [pos_x for pos_x, _ in convert_shape_format(simulated_shape)]
                    )

                    while simulated_x != continuous_hole[0]:
                        if simulated_x < continuous_hole[0]:
                            simulated_x = simulated_x + 1
                            actions_to_take.append(_move_right())  # Add Move Right Event
                        else:
                            simulated_x = simulated_x - 1
                            actions_to_take.append(_move_left())  # Add Move Left Event

                            # We should maybe move down but that seems like bonus points when we could
                            # Let the game do that for us :)

                            return actions_to_take

                else:
                    for size in size_to_rotation:
                        if continuous_hole[1] > size:
                            can_fit = True
                            break
                        else:
                            can_fit = False
                    if can_fit:
                        largest_size = max(size_to_rotation.keys())
                        rotation_goal = first(size_to_rotation[largest_size])
                        while simulated_shape.rotation != rotation_goal:
                            simulated_shape.rotation = simulated_shape.rotation + 1 % 4
                            actions_to_take.append(_rotate())  # Add Rotation Action

                        simulated_x = min(
                            [pos_x for pos_x, _ in convert_shape_format(simulated_shape)]
                        )

                        while simulated_x != continuous_hole[0]:
                            if simulated_x < continuous_hole[0]:
                                simulated_x = simulated_x + 1
                                actions_to_take.append(
                                    _move_right()
                                )  # Add Move Right Event
                            else:
                                simulated_x = simulated_x - 1
                                actions_to_take.append(
                                    _move_left()
                                )  # Add Move Left Event

                        # We should maybe move down but that seems like bonus points when we could
                        # Let the game do that for us :)

                        return actions_to_take
                    else:
                        raise RuntimeError(
                            "No Solution For Current State (Fix it so it finds a solution dumbass)"
                        )

    def _orientation_to_size(self, piece: "Piece") -> ImmutableSetMultiDict[int, int]:
        rotation_to_size: List[Tuple[int, int]] = []
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
                rotation_to_size.append((count, num))
            else:
                raise RuntimeError("Failed to find last line of shape.")

        return immutablesetmultidict(rotation_to_size)
