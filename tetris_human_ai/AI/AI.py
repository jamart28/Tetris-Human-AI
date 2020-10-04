from typing import List, Tuple

from attr import attrs, attrib
import pygame
from immutablecollections import ImmutableSetMultiDict, immutablesetmultidict
from more_itertools import first

from tetris_human_ai.game.tetris import Piece


GameState = Tuple[Piece, Piece, List[List[Tuple[int, int, int]]]]

def _move_left():
    return pygame.event(type=pygame.KEYDOWN, key=pygame.K_LEFT)


def _move_right():
    return pygame.event(type=pygame.KEYDOWN, key=pygame.K_RIGHT)


def _move_down():
    return pygame.event(type=pygame.KEYDOWN, key=pygame.K_DOWN)


def _rotate():
    return pygame.event(type=pygame.KEYDOWN, key=pygame.K_UP)

@attrs
class BigBrain:
    game_states: List[GameState] = attrib()

    def big_thonk(self, state: GameState) -> List[pygame.event]:
        current_piece, next_piece, grid = state
        smallest_hole = ((0, 0), 11)
        continuous_hole = ((0, 0), 0)
        for i, row in enumerate(state[1]):
            continuous_hole = ((0, i), 0)
            if (0, 0, 0) in row:
                for j, cell in enumerate(row):
                    if cell == (0, 0, 0):
                        continuous_hole[1] += 1
                    else:
                        if continuous_hole[1] > 0 and continuous_hole < smallest_hole[1]:
                            smallest_hole = continuous_hole
                        continuous_hole = ((j, i), 0)
            else:
                continue

            size_to_rotation = self._orientation_to_size(current_piece)
            actions_to_take: List[pygame.event] = []
            if continuous_hole[1] in size_to_rotation:
                rotation_goal = first(size_to_rotation[continuous_hole[1]])
                while current_piece.rotation != rotation_goal:
                    current_piece.rotation = current_piece.rotation + 1 % 4
                    actions_to_take.append(_rotate())  # Add Rotation Action

                while current_piece.x != continuous_hole[0][0]:
                    if current_piece.x < continuous_hole[0][0]:
                        current_piece.x = current_piece.x + 1
                        actions_to_take.append(_move_right())  # Add Move Right Event
                    else:
                        current_piece.x = current_piece.x - 1
                        actions_to_take.append(_move_left())  # Add Move Left Event

                # We should maybe move down but that seems like bonus points when we could
                # Let the game do that for us :)

                return actions_to_take

            else:
                # We may need to find the next smallest hole and try again.
                raise RuntimeError("No Solution For Current State")

    def _orientation_to_size(self, piece: Piece) -> ImmutableSetMultiDict[int, int]:
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



# def _available_positions(state: GameState):
#     for rotation in state[0].
