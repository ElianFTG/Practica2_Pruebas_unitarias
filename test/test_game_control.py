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
    assert result == (0,"Card1",0)

def test_player_LR_selection_hand_card_allowed():
    player = Player(name="Test Player")
    selected = "Card1"
    allowed_card_list = ["Card1", "Card3"]
    result = player_LR_selection_hand(player, selected, allowed_card_list=allowed_card_list)
    assert result ==  (False, 'Card1', False) 


def test_player_LR_selection_hand_card_not_allowed():
    player = Player(name="Test Player")
    selected = "Card2"
    allowed_card_list = ["Card1"]
    result = player_LR_selection_hand(player, selected, allowed_card_list=allowed_card_list)
    assert result == (False, 'Card2', False)  


def test_player_LR_selection_hand_no_valid_cards():
    player = Player(name="Test Player")
    selected = None
    allowed_card_list = ["Card1"]
    result = player_LR_selection_hand(player, selected, allowed_card_list=allowed_card_list)
    assert result == (False, None, False)


def test_player_choice_target_multiple_players():
    players = [Player(name="Player 1"), Player(name="Player 2"), Player(name="Player 3")]
    result = player_choice_target(players)
    assert result in players


def test_player_choice_target_one_player():
    players = [Player(name="Player 1")]
    result = player_choice_target(players)
    assert result == players[0]

def test_player_choice_target_none():
    players = None
    with pytest.raises(TypeError):
        player_choice_target(players)


def test_player_choice_color():
    color = player_choice_color() 
    assert color in ["g","b","y","r"]