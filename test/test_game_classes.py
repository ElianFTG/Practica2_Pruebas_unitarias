import pytest
from game_classes import *
from AI_card_logic import *


# Tests para la clase Card

def test_card_init():
    card = Card("b_1", "small_cards/blue_1.png", "TestOwner")
    assert card.name == "b_1"
    assert card.Owner == "TestOwner"
    assert card.color == "b"
    assert card.type == "1"

def test_set_owner():
    card = Card("b_1", "small_cards/blue_1.png", "TestOwner")
    card.set_Owner("NewOwner")
    assert card.Owner == "NewOwner"

def test_play_card():
    card = Card("b_1", "small_cards/blue_1.png", "TestOwner")
    board = Board("TestBoard")
    card.play_card(board)
    assert card.Owner == "TestBoard" 

# Tests para la clase Player

@pytest.fixture
def setup_game():
    mock_cards = [
        Card("b_5", "small_cards/blue_5.png", None),
        Card("r_6", "small_cards/red_6.png", None),
        Card("g_7", "small_cards/green_7.png", None)
    ]
    deck = Deck("TestDeck", mock_cards)
    player = Player("TestPlayer")
    return player, deck

def test_player_init():
    player = Player("TestPlayer")
    assert player.name == "TestPlayer"
    assert player.hand == []
    assert player.skip is False

def test_player_grab_card(setup_game):
    player, deck = setup_game
    player.grab_card(deck)

    assert len(player.hand) == 1
    assert player.hand[0].Owner == "TestPlayer"

@pytest.mark.usefixtures("mocker")
def test_player_grab_card_empty_deck(setup_game,mocker):
    player, deck = setup_game
    
    # Mockea el metodo grab_card devolviendo None
    mocker.patch.object(deck, 'grab_card', return_value=None)
    result = player.grab_card(deck)
    assert result is None

def test_grab_cards(setup_game):
    player, deck = setup_game
    player.grab_cards(deck, 2)

    assert len(player.hand) == 2
    for card in player.hand:
        assert card.Owner == "TestPlayer"

def test_player_play_card(setup_game):
    player, deck = setup_game
    player.grab_card(deck)  

    assert len(player.hand) == 1  

    board = Board("TestBoard")
    card_to_play = player.hand[0] 
    player.play_card(board, 0)  

    assert len(player.hand) == 0  
    assert board.card_stack[0].Owner == "TestBoard" 
    assert board.card_stack[0] == card_to_play 


# Tests para la clase deck

@pytest.fixture
def mock_cards():
    return [
        Card("b_1", "small_cards/blue_1.png", None),
        Card("r_2", "small_cards/red_2.png", None),
        Card("g_3", "small_cards/green_3.png", None)
    ]

def test_deck_init(mock_cards):
    deck = Deck("TestDeck", mock_cards)
    assert deck.name == "TestDeck"
    assert len(deck.deck) == len(mock_cards)
    for card in deck.deck:
        assert card.Owner == "TestDeck"

def test_grab_card(mock_cards):
    deck = Deck("TestDeck", mock_cards)
    grabbed_card = deck.grab_card()
    assert grabbed_card is not None
    assert grabbed_card.Owner is None
    assert len(deck.deck) == 2

def test_grab_card_empty_deck(monkeypatch, mock_cards): 
    deck = Deck("TestDeck", [])
    def mock_gen_rand_deck(name, arg): # Simulamos el comportamiento de deck_gen.gen_rand_deck
        return Deck(name, mock_cards)
    #Reemplaza la función original por la simulada
    monkeypatch.setattr("deck_gen.gen_rand_deck", mock_gen_rand_deck)
    grabbed_card = deck.grab_card()
    assert grabbed_card is not None
    assert grabbed_card.Owner is None
    assert len(deck.deck) == 2

# Tests para la clase board

def test_board_init():
    board = Board("TestBoard")
    assert board.name == "TestBoard"
    assert board.card_stack == []
    assert board.type is None
    assert board.color is None
    assert board.turn_iterator == 1

def test_update_board(mock_cards):
    board = Board("TestBoard")
    card = mock_cards[0]
    board.update_Board(card)
    assert board.type == card.type
    assert board.color == card.color
    assert len(board.card_stack) == 1
    assert board.card_stack[0].Owner == "TestBoard"

def test_check_board(mock_cards):
    board = Board("TestBoard")
    card = mock_cards[0]
    board.update_Board(card)
    last_card = board.check_Board()
    assert last_card == card

def test_check_empty_board():
    board = Board("TestBoard")
    assert board.check_Board() is None