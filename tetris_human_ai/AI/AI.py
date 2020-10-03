from typing import List, Tuple

from attr import attrs, attrib
import pygame

from tetris_human_ai.game.tetris import Piece


GameState = Tuple[[Piece, List[List[Tuple[int, int, int]]]]]


@attrs
class BigBrain:
    game_states: List[GameState] = attrib()

    def big_thonk(state: GameState) -> List[pygame.event]:
        pass


def _available_positions(state: GameState):
    pass
