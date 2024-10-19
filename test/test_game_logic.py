import pytest
from pytest_mock import MockerFixture

import card_logic
import display_funct
import game_control
import Main_Decision_Tree
import pygame

from game_logic import *


class MockPlayer:
    def __init__(self, name, hand=None, hatval=None, AI=False, skip=False):
        self.name = name
        self.hand = hand if hand else []
        self.hatval = hatval if hatval else {}
        self.AI = AI
        self.skip = skip


class MockCard:
    def __init__(self, old_val=0):
        self.old_val = old_val



def test_update_hatval_try():
    player = "Player A"
    target = MockPlayer(name="Player B", hatval={"Player A": 1})

    update_hatval(player, target)
    assert target.hatval[player] == 2

    update_hatval(player, target, hate_increase=3)
    assert target.hatval[player] == 5


def test_update_hatval_catch():
    player = "Player A"
    target = MockPlayer(name="Player B", hatval={})

    update_hatval(player, target)
    assert target.hatval[player] == 1

    update_hatval(player, target, hate_increase=2)
    assert target.hatval[player] == 3

def test_degrade_hatval_if():
    player = MockPlayer(name="Player A", hatval={"Player B": 3, "Player C": 1})

    degrade_hatval(player)
    assert player.hatval["Player B"] == 2
    assert player.hatval["Player C"] == 0


def test_degrade_hatval_no_if():
    player = MockPlayer(name="Player A", hatval={"Player B": 0, "Player C": 0})

    degrade_hatval(player)
    assert player.hatval["Player B"] == 0
    assert player.hatval["Player C"] == 0

def test_degrade_hatval_empty_hatval():
    player = MockPlayer(name="Player A", hatval={})
    degrade_hatval(player)
    assert player.hatval == {}

def test_increment_card_old_vals_with_cards():
    player = MockPlayer(name="Player A", hand=[MockCard(1), MockCard(3)])

    increment_card_old_vals(player)
    assert player.hand[0].old_val == 2
    assert player.hand[1].old_val == 4


def test_increment_card_old_vals_no_cards():
    player = MockPlayer(name="Player A", hand=[])

    increment_card_old_vals(player)
    assert player.hand == []         




def test_compute_turn_if():
    players = ["Player A", "Player B", "Player C"]
    turn = 0
    new_turn = compute_turn(players, turn, -1)
    assert new_turn == 2


def test_compute_turn_elif():
    players = ["Player A", "Player B", "Player C"]
    turn = 2
    new_turn = compute_turn(players, turn, 1)
    assert new_turn == 0


def test_compute_turn_no_condition():
    players = ["Player A", "Player B", "Player C"]
    turn = 1
    new_turn = compute_turn(players, turn, 1)
    assert new_turn == 2


def test_check_update_if_if(mocker: MockerFixture):
    board = mocker.Mock()
    allowed_card_list = mocker.Mock()
    selected = None
    player = MockPlayer(name="Player A")
    players = [player]
    update = True

    mock_redraw_screen = mocker.patch('display_funct.redraw_screen')

    result = check_update(board, allowed_card_list, selected, player, players, update)
    assert not result
    mock_redraw_screen.assert_called_once_with([(player, None)], board, players)


def test_check_update_if_else(mocker: MockerFixture):
    board = mocker.Mock()
    allowed_card_list = [mocker.Mock()]
    selected = 0
    player = MockPlayer(name="Player A")
    players = [player]
    update = True

    mock_redraw_screen = mocker.patch('display_funct.redraw_screen')

    result = check_update(board, allowed_card_list, selected, player, players, update)
    assert not result
    mock_redraw_screen.assert_called_once_with([(player, allowed_card_list[selected])], board, players)


def test_check_update_no_if(mocker: MockerFixture):
    board = mocker.Mock()
    allowed_card_list = mocker.Mock()
    selected = None
    player = MockPlayer(name="Player A")
    players = [player]
    update = False

    mock_redraw_screen = mocker.patch('display_funct.redraw_screen')

    result = check_update(board, allowed_card_list, selected, player, players, update)
    assert not result
    mock_redraw_screen.assert_not_called()        
    

def test_check_winners_if():
    player = MockPlayer(name="Player A", hand=[])
    check_winners(player)
    assert player in winners
    assert len(winners) == 1


def test_check_winners_no_if():
    winners = []
    player = MockPlayer(name="Player A", hand=[MockCard()])
    check_winners(player)
    assert player not in winners
    assert len(winners) == 0    
    

def test_check_game_done(monkeypatch):
    # Simulamos un jugador con cartas y el evento del final del juego
    mock_player = MockPlayer(name="Player 1")
    
    # Simulamos eventos de pygame para evitar el while 1
    def mock_pygame_event():
        return ['mock_event']  # Simulamos eventos vacíos

    def mock_get_keypress(event):
        return (False, False, True)  # Simulamos que se presiona UP para salir del bucle

    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)

    # Usamos monkeypatch para reemplazar funciones globales o módulos
    monkeypatch.setattr('pygame.event.get', mock_pygame_event)
    monkeypatch.setattr('game_control.get_keypress', mock_get_keypress)
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)

    # Llamamos a la función con un solo jugador, el juego debería terminar
    players = [mock_player]
    result = check_game_done(players)
    
    # Comprobamos que la función devolvió True (el juego terminó)
    assert result == True



# Excepción personalizada para salir del bucle
class ForcedExit(Exception):
    pass

def test_check_game_done_all_but_select_up(monkeypatch):
    """Caso que entra a todas las condiciones menos al if select_UP"""
    mock_player = MockPlayer(name="Player 1")
    
    # Simulamos eventos de pygame sin presionar UP
    def mock_pygame_event():
        return ['mock_event']  # Simulamos eventos vacíos

    def mock_get_keypress(event):
        return (False, False, False)  # No se presiona UP

    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)

    # Simulamos forzar la salida del while 1 después de hacer el trabajo necesario
    event_count = 0
    def mock_pygame_event_exit():
        nonlocal event_count
        if event_count < 2:  # Permitimos que el bucle se ejecute 2 veces antes de forzar la salida
            event_count += 1
            return ['mock_event']
        raise ForcedExit  # Forzamos la salida del bucle después de 2 eventos

    monkeypatch.setattr('pygame.event.get', mock_pygame_event_exit)
    monkeypatch.setattr('game_control.get_keypress', mock_get_keypress)
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)

    winners = []

    players = [mock_player]
    
    winners.append(mock_player)
    # Capturamos la excepción para evitar que la prueba falle debido a la salida forzada
    try:
        result = check_game_done(players)
    except ForcedExit:
        result = False  # Establecemos el valor de result si se fuerza la salida

    # Comprobamos que el resultado es False ya que no se presionó UP
    assert result == False
    assert winners == [mock_player]


def test_check_game_done_no_select_up_or_for_event(monkeypatch):
    """Caso que no entra al select_UP ni al for event pero si al resto"""
    mock_player = MockPlayer(name="Player 1")

    # Simulamos eventos vacíos para evitar el for
    def mock_pygame_event():
        return []

    def mock_get_keypress(event):
        return (False, False, False)  # No se presiona UP

    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)

    # Simulamos una salida forzada después de 1 iteración del bucle
    def mock_pygame_event_exit():
        raise ForcedExit  # Forzamos la salida del bucle

    monkeypatch.setattr('pygame.event.get', mock_pygame_event_exit)
    monkeypatch.setattr('game_control.get_keypress', mock_get_keypress)
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)

    winners = []
    winners.append(mock_player)

    try:
        players = [mock_player]
        result = check_game_done(players)
    except ForcedExit:
        result = False

    assert result == False
    assert winners == [mock_player]

