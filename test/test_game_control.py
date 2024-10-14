import pytest
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game_control import *
from AI_classes import *

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


@pytest.mark.parametrize(
        "select_L,select_R,selected,result",
        [
            (0,1,None,1),
            (0,1,3,3),
            (1,0,0,0),
            (0,1,1,2),
            (1,0,3,2)
        ]
)
def test_select_move_color(select_L, select_R,selected,result):
    assert select_move_color(select_L, select_R,selected) == result

@pytest.mark.parametrize(
    "selected,result",
    [
        (None,(0,0,0)),
        (1,(0,1,0)),
        # (None,()),
        # (None,()),
        # (None,()),
    ]
)
def test_player_LR_selection_color(selected,result):
    assert player_LR_selection_color(selected) == result


def test_leaf_initialization():
    leaf = Leaf(10)
    assert leaf.value == 10

def test_branch_initialization():
    leaf1 = Leaf(1)
    leaf2 = Leaf(2)
    branch = Branch(Branch_q="Is it a leaf?", child_1=leaf1, child_2=leaf2)
    
    assert branch.question == "Is it a leaf?"
    assert branch.child_1 == leaf1
    assert branch.child_2 == leaf2

def test_get_offshoots():
    leaf1 = Leaf(1)
    leaf2 = Leaf(2)
    branch = Branch(child_1=leaf1, child_2=leaf2)
    
    assert branch.get_offshoots() == (leaf1, leaf2)