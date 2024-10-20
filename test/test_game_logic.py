import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pytest_mock import MockerFixture

import card_logic
import display_funct
import game_control
import Main_Decision_Tree
import pygame
from game_logic import *

class MockTree:
    def __init__(self):
        self.value = None

    def get_offshoots(self):
        return (MockTree(), MockTree())
    
class MockDecisionTree:
    def __init__(self):
        self.Dec_Tree = MockTree()

class MockPlayer:
    def __init__(self, name, hand=None, hatval=None, AI=False, skip=False):
        self.name = name
        self.hand = hand if hand else []
        self.hatval = hatval if hatval else {}
        self.AI = AI
        self.skip = skip
        self.Main_Decision_Tree = MockDecisionTree()
    def grab_card(self, deck):
        if deck:
            self.hand.append(deck.pop())

class MockImage:
    def get_rect(self):
        return pygame.Rect(0, 0, 100, 150) 

class MockCard:
    def __init__(self, old_val=0):
        self.old_val = old_val
        self.card_data = MockImage() 

class MockBoard:
    def __init__(self):
        self.turn_iterator = iter(range(100))
        self.card_stack = [] 
        

class MockDeck:
    def __init__(self):
        self.cards = ["Card1", "Card2", "Card3"]  # Simulamos un mazo con 3 cartas

    def pop(self):
        return self.cards.pop()  # El método pop para sacar una carta del mazo




class MockSurface:
    def get_rect(self):
        return pygame.Rect(0, 0, 100, 150)  # Simulamos un rectángulo cualquiera

    def get_size(self):
        return (100, 150)  # Simulamos el tamaño de la imagen

def mock_load_image(filename):
    return MockSurface()  # Retornamos un objeto que puede ser escalado por pygame





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
    mock_player = MockPlayer(name="Player 1")
    def mock_pygame_event():
        return ['mock_event']
    def mock_get_keypress(event):
        return (False, False, True)
    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)
    monkeypatch.setattr('pygame.event.get', mock_pygame_event)
    monkeypatch.setattr('game_control.get_keypress', mock_get_keypress)
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)
    players = [mock_player]
    result = check_game_done(players)
    assert result == True

class ForcedExit(Exception):
    pass
def test_check_game_done_all_but_select_up(monkeypatch):
    """Caso que entra a todas las condiciones menos al if select_UP"""
    mock_player = MockPlayer(name="Player 1")
    def mock_pygame_event():
        return ['mock_event'] 
    def mock_get_keypress(event):
        return (False, False, False) 
    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)
    event_count = 0
    def mock_pygame_event_exit():
        nonlocal event_count
        if event_count < 2:
            event_count += 1
            return ['mock_event']
        raise ForcedExit  
    monkeypatch.setattr('pygame.event.get', mock_pygame_event_exit)
    monkeypatch.setattr('game_control.get_keypress', mock_get_keypress)
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)
    winners = []
    players = [mock_player]
    winners.append(mock_player)
    try:
        result = check_game_done(players)
    except ForcedExit:
        result = False 
    assert result == False
    assert winners == [mock_player]

def test_check_game_done_no_select_up_or_for_event(monkeypatch):
    """Caso que no entra al select_UP ni al for event pero si al resto"""
    mock_player = MockPlayer(name="Player 1")
    def mock_pygame_event():
        return []
    def mock_get_keypress(event):
        return (False, False, False)  
    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)
    def mock_pygame_event_exit():
        raise ForcedExit 
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

def test_check_game_done_enters_for_but_not_while(monkeypatch):
    """Prueba que entra al if len(players) <= 1, ejecuta el for pero no el while."""
    mock_player_1 = MockPlayer(name="Player 1")
    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)
    def mock_pygame_event_get():
        raise ForcedExit  
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)
    monkeypatch.setattr('pygame.event.get', mock_pygame_event_get)
    winners = []
    winners.append(mock_player_1)
    players = [mock_player_1]
    try:
        result = check_game_done(players)
    except ForcedExit:
        result = False  
    assert result == False
    assert len(winners) == 1
    assert winners[0] == mock_player_1

def test_check_game_done_first_if_only(monkeypatch):
    """Prueba que solo entra al if len(players) <= 1 y no ejecuta el for ni el while."""
    mock_player = MockPlayer(name="Player 1")
    def mock_draw_winners(winners_list):
        print("Mock draw_winners called with:", winners_list)
    def mock_pygame_event_get():
        raise ForcedExit 
    monkeypatch.setattr('display_funct.draw_winners', mock_draw_winners)
    monkeypatch.setattr('pygame.event.get', mock_pygame_event_get)
    winners = []
    players = [mock_player]
    try:
        result = check_game_done(players)
    except ForcedExit:
        result = False  
    assert result == False
    assert len(winners) == 0

def test_check_game_done_no_conditions(monkeypatch):
    """Caso que no entra a ninguna condición, más de un jugador"""
    mock_player1 = MockPlayer(name="Player 1")
    mock_player2 = MockPlayer(name="Player 2")
    players = [mock_player1, mock_player2]
    result = check_game_done(players)
    assert result == False




def test_extern_AI_player_turn(monkeypatch):
    mock_board = {}
    mock_deck = [MockCard(old_val=1), MockCard(old_val=2)]
    mock_player = MockPlayer("AI_Player", hand=[], AI=True)
    mock_players = [mock_player]
    mock_turn = 0

    global increment_card_old_vals_called
    global travel_Main_Decision_Tree_called
    global degrade_hatval_called

    increment_card_old_vals_called = False
    travel_Main_Decision_Tree_called = False
    degrade_hatval_called = False

    def mock_increment_card_old_vals(player):
        global increment_card_old_vals_called
        increment_card_old_vals_called = True

    def mock_travel_Main_Decision_Tree(board, deck, player, players, tree):
        global travel_Main_Decision_Tree_called
        travel_Main_Decision_Tree_called = True

    def mock_degrade_hatval(player):
        global degrade_hatval_called
        degrade_hatval_called = True

    monkeypatch.setattr('game_logic.increment_card_old_vals', mock_increment_card_old_vals)
    monkeypatch.setattr('game_logic.Main_Decision_Tree.travel_Main_Decision_Tree', mock_travel_Main_Decision_Tree)
    monkeypatch.setattr('game_logic.degrade_hatval', mock_degrade_hatval)
    extern_AI_player_turn(mock_board, mock_deck, mock_player, mock_players, mock_turn)
    assert increment_card_old_vals_called, "increment_card_old_vals was not called"
    assert travel_Main_Decision_Tree_called, "travel_Main_Decision_Tree was not called"
    assert degrade_hatval_called, "degrade_hatval was not called"
    assert degrade_hatval_called, "degrade_hatval was not called"

def mock_intern_player_turn(board, deck, player, allowed_card_list, selected):
    return (True, allowed_card_list[0] if allowed_card_list else None, True)

def test_extern_player_turn_no_playable_cards(monkeypatch):
    mock_board = MockBoard()
    mock_deck = [1, 2, 3]
    mock_player = MockPlayer("Player1")
    mock_players = [mock_player]
    mock_turn = 0

    monkeypatch.setattr(card_logic, 'card_allowed', lambda board, player: [])
    monkeypatch.setattr(display_funct, 'redraw_screen', lambda *args: None)
    monkeypatch.setattr('game_logic.compute_turn', lambda players, turn, iterator: turn + 1)

    player, turn = extern_player_turn(mock_board, mock_deck, mock_player, mock_players, mock_turn)

    assert len(mock_player.hand) == 1
    assert turn == 1

def test_extern_player_turn_playable_card_no_drop_again(monkeypatch):
    mock_board = {}
    mock_deck = [1, 2, 3]
    mock_player = MockPlayer("Player1")
    mock_players = [mock_player]
    mock_turn = 0

    monkeypatch.setattr(card_logic, 'card_allowed', lambda board, player: [1])
    monkeypatch.setattr(display_funct, 'redraw_screen', lambda *args: None)
    monkeypatch.setattr('game_logic.intern_player_turn', mock_intern_player_turn)
    monkeypatch.setattr('game_logic.check_winners', lambda player: None)
    monkeypatch.setattr('game_logic.check_update', lambda *args: True)
    monkeypatch.setattr(card_logic, 'card_played_type', lambda *args: False)

    player, turn = extern_player_turn(mock_board, mock_deck, mock_player, mock_players, mock_turn)

    assert turn == 0

def test_extern_player_turn_playable_card_with_drop_again(monkeypatch):
    # Mock objects
    mock_board = MockBoard()
    mock_deck = [1, 2, 3]
    mock_player = MockPlayer("Player1")
    mock_players = [mock_player]
    mock_turn = 0

    monkeypatch.setattr(card_logic, 'card_allowed', lambda board, player: [1])
    monkeypatch.setattr(display_funct, 'redraw_screen', lambda *args: None)
    monkeypatch.setattr('game_logic.intern_player_turn', mock_intern_player_turn)
    monkeypatch.setattr('game_logic.check_winners', lambda player: None)
    monkeypatch.setattr('game_logic.check_update', lambda *args: True)
    monkeypatch.setattr(card_logic, 'card_played_type', lambda *args: False)

    player, turn = extern_player_turn(mock_board, mock_deck, mock_player, mock_players, mock_turn)
    assert turn == mock_turn


def test_extern_player_turn_multiple_playable_cards(monkeypatch):
    mock_board = {}
    mock_deck = [1, 2, 3]
    mock_player = MockPlayer("Player1")
    mock_players = [mock_player]
    mock_turn = 0

    monkeypatch.setattr(card_logic, 'card_allowed', lambda board, player: [1, 2])
    monkeypatch.setattr(display_funct, 'redraw_screen', lambda *args: None)
    monkeypatch.setattr('game_logic.intern_player_turn', mock_intern_player_turn)
    monkeypatch.setattr('game_logic.check_winners', lambda player: None)
    monkeypatch.setattr('game_logic.check_update', lambda *args: True)
    monkeypatch.setattr(card_logic, 'card_played_type', lambda *args: False)

    player, turn = extern_player_turn(mock_board, mock_deck, mock_player, mock_players, mock_turn)

    assert turn == 0
    
def mock_player_LR_selection_hand(player, selected, board, allowed_card_list):
    return (True, allowed_card_list[0] if allowed_card_list else None, True)

def test_intern_player_turn_empty_allowed_card_list(monkeypatch):
    # Mock objects
    mock_board = MockBoard()
    mock_deck = [1, 2, 3]
    mock_player = MockPlayer("Player1")
    allowed_card_list = []
    selected = None

    monkeypatch.setattr(game_control, 'player_LR_selection_hand', mock_player_LR_selection_hand)

    update, selected, turn_done = intern_player_turn(mock_board, mock_deck, mock_player, allowed_card_list, selected)

    assert update == True
    assert selected == None
    assert turn_done == True
    assert len(mock_player.hand) == 1

def test_intern_player_turn_non_empty_allowed_card_list(monkeypatch):
    # Mock objects
    mock_board = MockBoard()
    mock_deck = [1, 2, 3]
    mock_player = MockPlayer("Player1")
    allowed_card_list = [1]
    selected = None

    monkeypatch.setattr(game_control, 'player_LR_selection_hand', mock_player_LR_selection_hand)

    update, selected, turn_done = intern_player_turn(mock_board, mock_deck, mock_player, allowed_card_list, selected)

    assert update == True
    assert selected == 1
    assert turn_done == True
    assert len(mock_player.hand) == 0 


def test_game_loop():
    class SimpleBoard:
        def __init__(self):
            self.turn_iterator = 1

    class SimpleDeck:
        def __init__(self):
            self.cards = ["Card_one", "Card_two", "Card_three"]

    class SimplePlayer:
        def __init__(self, name, AI=False, skip=False):
            self.name = name
            self.hand = []
            self.AI = AI
            self.skip = skip

        def grab_card(self, deck):
            if deck.cards:
                self.hand.append(deck.cards.pop())

    def game_loop(board, deck, players):
        for player in players:
            if not player.skip:
                player.grab_card(deck)
                board.turn_iterator += 1

    board = SimpleBoard()
    deck = SimpleDeck()
    players = [SimplePlayer("Player_one"), SimplePlayer("Player_two", AI=True), SimplePlayer("Player_three", skip=True)]

    game_loop(board, deck, players)

    assert len(players[0].hand) == 1
    assert len(players[1].hand) == 1
    assert len(players[2].hand) == 0
    assert board.turn_iterator == 3