import pytest
import pygame
import sys
import os
from unittest.mock import MagicMock
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
def test_get_keypress(event, expected): # Branch Coverage
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
def test_select_move_color(select_L, select_R,selected,result): # Branch coverage
    assert select_move_color(select_L, select_R,selected) == result

def test_player_LR_selection_color(mocker): #Branch coverage
    mocker.patch("pygame.event.get").return_value = [1]
    mocker.patch("game_control.get_keypress").return_value = (0, 0, None)
    assert player_LR_selection_color() == (0,0,0) # Rojo
    mocker.patch("game_control.get_keypress").return_value = (0, 1, 1)
    assert player_LR_selection_color(1) == (1,2,1) # Naranja
    mocker.patch("game_control.get_keypress").return_value = (1, 0, 1)
    assert player_LR_selection_color(2) == (1,1,1) # Verde

def test_player_choice_color(mocker): #Branch coverage
    mocker.patch("game_control.player_LR_selection_color").return_value = (0, 0, 1)
    assert player_choice_color() == "g"
    mocker.patch("game_control.player_LR_selection_color").return_value = (0, 1, 1)
    assert player_choice_color() == "b"
    mocker.patch("game_control.player_LR_selection_color").return_value = (0, 2, 1)
    assert player_choice_color() == "y"
    mocker.patch("game_control.player_LR_selection_color").return_value = (0, 3, 1)
    assert player_choice_color() == "r"

@pytest.mark.parametrize(
        "select_L, select_R, players, selected,result",
        [
            (1,0,[1,1,1,1],None,0),
            (0,1,[1,1],2,1),
            (0,1,[1,1,1,1],None,1)
        ]
)
def test_select_move_target(select_L, select_R, players, selected,result): # Branch coverage
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


### test para player_LR_selection_hand Branch Coverage

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
###

### test para player_choice_target() Branch coverage
def test_player_choice_target_multiple_players():
    players = [Player(name="Player 1"), Player(name="Player 2"), Player(name="Player 3")]
    result = player_choice_target(players)
    assert result in players


def test_player_choice_target_one_player():
    players = [Player(name="Player 1")]
    result = player_choice_target(players)
    assert result == players[0]
###

### Test para la funcion 
# Mock de la función get_keypress
def mock_get_keypress(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            return (False, True, False)
        elif event.key == pygame.K_LEFT:
            return (True, False, False)
        elif event.key == pygame.K_UP:
            return (False, False, True)
    return (False, False, False)

# Mock de la función select_move_target
def mock_select_move_target(select_L, select_R, players, selected):
    if select_L:
        return selected - 1 if selected > 0 else len(players) - 1
    elif select_R:
        return (selected + 1) % len(players)
    return selected

# Prueba 1: Selección hacia la derecha
def test_selection_right():
    players = [0, 1, 2]
    selected = 0
    pygame.event.get = MagicMock(return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})])
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    select_move_target = MagicMock(side_effect=mock_select_move_target)
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is True
    assert selected_new == 1
    assert turn_done is False

# Prueba 2: Selección hacia la izquierda
def test_selection_left():
    players = [0, 1, 2]
    selected = 1
    pygame.event.get = MagicMock(return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})])
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    select_move_target = MagicMock(side_effect=mock_select_move_target)
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is True
    assert selected_new == 0
    assert turn_done is False

# Prueba 3: Selección ya es la correcta (sin cambio)
def test_selection_no_change():
    players = [0, 1, 2]
    selected = 1
    pygame.event.get = MagicMock(return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})])
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    select_move_target = MagicMock(return_value=1)  # Selección permanece igual
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is True
    assert selected_new == 0
    assert turn_done is False

# Prueba 4: Confirmar selección (tecla arriba)
def test_confirm_selection():
    players = [0, 1, 2]
    selected = 0
    pygame.event.get = MagicMock(return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})])
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is True
    assert selected_new == 0
    assert turn_done is True

# Prueba 5: No hay eventos (sin cambios)
def test_no_event():
    players = [0, 1, 2]
    selected = 0
    pygame.event.get = MagicMock(return_value=[])  # No eventos
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is False
    assert selected_new == 0
    assert turn_done is False

# Prueba 6: Selección hacia la derecha y confirmación simultáneos
def test_selection_right_and_confirm():
    players = [0, 1, 2]
    selected = 0
    events = [
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}),
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
    ]
    pygame.event.get = MagicMock(return_value=events)
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    select_move_target = MagicMock(side_effect=mock_select_move_target)
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is True
    assert selected_new == 0
    assert turn_done is True

# Prueba 7: Eventos sin cambios (sin seleccionar ni confirmar)
def test_no_selection_no_confirm():
    players = [0, 1, 2]
    selected = 0
    pygame.event.get = MagicMock(return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})])
    get_keypress = MagicMock(side_effect=mock_get_keypress)
    update, selected_new, turn_done = player_LR_selection_target(players, selected)
    assert update is False
    assert selected_new == 0
    assert turn_done is False

### test para player_choice_targe Statment coverage
def test_player_choice_target_none():
    players = None
    with pytest.raises(TypeError):
        player_choice_target(players)





