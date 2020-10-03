from typing import List, Tuple

from attr import attrs, attrib
import pygame

from tetris_human_ai.game.tetris import Piece


GameState = Tuple[[Piece, List[List[Tuple[int, int, int]]]]]


@attrs
class BigBrain:
    game_states: List[GameState] = attrib()

    def big_thonk(state: GameState) -> List[pygame.event]:
        smallest_hole = ((0, 0), 11)
        continuous_hole = ((0, 0), 0)
        for i, row in enumerate(state[1]):
            continuous_hole = ((0, i), 0)
            if (0, 0, 0) in row:
                for j, cell in enumerate(row):
                    if cell != (0, 0, 0):
                        continuous_hole[1] += 1
                    else:
                        if continuous_hole[1] > 0 and continuous_hole < smallest_hole[1]:
                            smallest_hole = continuous_hole
                        continuous_hole = ((j, i), 0)
            else:
                continue
            if state[0] fits in smalles_hole:
                return moves to get it into the hole
            else:
                continue



# def _available_positions(state: GameState):
#     for rotation in state[0].
