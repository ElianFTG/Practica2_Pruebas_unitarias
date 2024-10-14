import pytest
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game_control import *


@pytest.mark.parametrize(
        "event, expected",
        [
            (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),(True, False, False)),
            (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT),(False, True, False)),
            (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP),(False, False, True))
        ]
)

def test_get_keypress(event, expected):
    assert get_keypress(event) == expected


def test_select_move_color():
    pass