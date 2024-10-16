import pytest
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game_control import *
from game_classes import Player


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


@pytest.mark.parametrize(
        "select_L, select_R, players, selected,result",
        [
            (1,0,[1,1,1,1],None,0),
            (0,1,[1,1],2,1),
            (0,1,[1,1,1,1],None,1)
        ]
)
def test_select_move_target(select_L, select_R, players, selected,result):
    assert select_move_target(select_L, select_R, players, selected) == result


@pytest.mark.parametrize(
        "select_L, select_R, allowed_card_list, selected, result",
        [
            (1,0,["y","b","r"],None,0),
            (0,1,["y","b"],2,1),
            (0,1,["y","b","r"],None,1)
        ]
)
def test_select_move_hand(select_L, select_R, allowed_card_list, selected, result):
    assert select_move_hand(select_L, select_R, allowed_card_list, selected) == result


def test_player_LR_selection_hand_no_board_no_allowed():
    player = Player(name="Test Player")
    selected = "Card1"
    result = player_LR_selection_hand(player, selected)
    assert result == (0,"Card1",0)  # Reemplaza con el resultado esperado

# Test when allowed_card_list contains the selected card
def test_player_LR_selection_hand_card_allowed():
    player = Player(name="Test Player")
    selected = "Card1"
    allowed_card_list = ["Card1", "Card3"]
    result = player_LR_selection_hand(player, selected, allowed_card_list=allowed_card_list)
    assert result ==  (False, 'Card1', False) # Reemplaza con el resultado esperado

# Test when selected card is not in allowed_card_list
def test_player_LR_selection_hand_card_not_allowed():
    player = Player(name="Test Player")
    selected = "Card2"
    allowed_card_list = ["Card1"]
    result = player_LR_selection_hand(player, selected, allowed_card_list=allowed_card_list)
    assert result == (False, 'Card2', False)  # Reemplaza con el resultado esperado

# Test when player has no valid cards in hand
def test_player_LR_selection_hand_no_valid_cards():
    player = Player(name="Test Player")
    selected = None
    allowed_card_list = ["Card1"]
    result = player_LR_selection_hand(player, selected, allowed_card_list=allowed_card_list)
    assert result == (False, None, False)