import pytest
from card_logic import *
from game_classes import *

CARD_IMAGE_PATH = "small_cards/"

### Funcion card_allowed

# Test 1: El mazo del tablero está vacio, cualquier carta es permitida
def test_card_allowed_board_empty():
    player = Player(name="Test Player")
    player.hand = [Card(name="r-1", filename=CARD_IMAGE_PATH + "red_1.png"), 
                   Card(name="g-2", filename=CARD_IMAGE_PATH + "green_2.png")]
    board = Board(name="Test Board")
    board.card_stack = []
    board.color = "r"
    board.type = "1"
    result = card_allowed(board, player)
    assert result == range(len(player.hand)) 

# Test 2: El color del tablero es "w" (comodín), cualquier carta es permitida
def test_card_allowed_board_color_wild():
    player = Player(name="Test Player")
    player.hand = [Card(name="r-1", filename=CARD_IMAGE_PATH + "red_1.png"), 
                   Card(name="g-2", filename=CARD_IMAGE_PATH + "green_2.png")]
    
    board = Board(name="Test Board")
    board.card_stack = [Card(name="b-3", filename=CARD_IMAGE_PATH + "blue_3.png")]
    board.color = "w"
    result = card_allowed(board, player)
    assert result == range(len(player.hand)) 

# Test 3: La mano contiene una carta comodín (color "w")
def test_card_allowed_player_wild_card():
    player = Player(name="Test Player")
    player.hand = [Card(name="w-wild", filename=CARD_IMAGE_PATH + "wild_pick_four.png"), 
                   Card(name="g-2", filename=CARD_IMAGE_PATH + "green_2.png")]
    board = Board(name="Test Board")
    board.card_stack = [Card(name="b-3", filename=CARD_IMAGE_PATH + "blue_3.png")]
    board.color = "b"
    board.type = "3"
    result = card_allowed(board, player)
    assert result == [0]  

# Test 4: La mano contiene una carta que coincide con el tipo de la carta del tablero
def test_card_allowed_matching_type():
    player = Player(name="Test Player")
    player.hand = [Card(name="r-1", filename=CARD_IMAGE_PATH + "red_1.png"), 
                   Card(name="g-2", filename=CARD_IMAGE_PATH + "green_2.png")]
    
    board = Board(name="Test Board")
    board.card_stack = [Card(name="b-2", filename=CARD_IMAGE_PATH + "blue_2.png")]
    board.color = "b"
    board.type = "2"
    result = card_allowed(board, player)
    assert result == [1] 

# Test 5: La mano contiene una carta que coincide con el color de la carta del tablero
def test_card_allowed_matching_color():
    player = Player(name="Test Player")
    player.hand = [Card(name="r-1", filename=CARD_IMAGE_PATH + "red_1.png"), 
                   Card(name="g-2", filename=CARD_IMAGE_PATH + "green_2.png")]
    board = Board(name="Test Board")
    board.card_stack = [Card(name="r-3", filename=CARD_IMAGE_PATH + "red_3.png")]
    board.color = "r"
    result = card_allowed(board, player)
    assert result == [0]  

# Test 6: No hay cartas permitidas en la mano del jugador
def test_card_allowed_no_valid_cards():
    player = Player(name="Test Player")
    player.hand = [Card(name="g-1", filename=CARD_IMAGE_PATH + "green_1.png"), 
                   Card(name="y-2", filename=CARD_IMAGE_PATH + "yellow_2.png")]
    board = Board(name="Test Board")
    board.card_stack = [Card(name="b-3", filename=CARD_IMAGE_PATH + "blue_3.png")]
    board.color = "b"
    board.type = "3"
    result = card_allowed(board, player)
    assert result == [] 

# Test 7: Varias cartas son permitidas (comodín y coincidencia de color)
def test_card_allowed_multiple_valid_cards():
    player = Player(name="Test Player")
    player.hand = [Card(name="w-wild", filename=CARD_IMAGE_PATH + "wild_pick_four.png"), 
                   Card(name="b-2", filename=CARD_IMAGE_PATH + "blue_2.png")]
    board = Board(name="Test Board")
    board.card_stack = [Card(name="b-3", filename=CARD_IMAGE_PATH + "blue_3.png")]
    board.color = "b"
    result = card_allowed(board, player)
    assert result == [0, 1]


###

### card_played_type

# Test 1: Tablero vacio
def test_card_played_type_empty_board():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Player")
    players = [player]
    
    result = card_played_type(board, deck, player, players)
    assert result == board.turn_iterator

# Test 2: Carta comodín (wild) de tipo "d" (robar 4 cartas y cambiar color)
def test_card_played_type_wild_draw_4():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Pl4yer")
    player_2 = Player(name="Test Pl4yer 2")
    player_2.hand = [Card(name="g-1", filename=CARD_IMAGE_PATH + "green_1.png"), 
                   Card(name="y-2", filename=CARD_IMAGE_PATH + "yellow_2.png")] 
    players = [player,player_2]
    
    card = Card(name="w-d", filename=CARD_IMAGE_PATH + "wild_pick_four.png")
    board.update_Board(card)
    
    result = card_played_type(board, deck, player, players)
    assert result == True

# Test 3: Carta comodín (wild) de tipo "c" (cambiar de color sin robar)
def test_card_played_type_wild_choose_color():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Player")
    player.hand = [Card(name="g-1", filename=CARD_IMAGE_PATH + "green_1.png"), 
                   Card(name="y-2", filename=CARD_IMAGE_PATH + "yellow_2.png")]
    player_2 = Player(name="Test Player 2")
    player_2.hand = [Card(name="g-1", filename=CARD_IMAGE_PATH + "green_1.png"), 
                   Card(name="y-2", filename=CARD_IMAGE_PATH + "yellow_2.png")] 
    players = [player,player_2]
    
    card = Card(name="w-c", filename=CARD_IMAGE_PATH + "wild_color_changer.png")
    board.update_Board(card)
    
    result = card_played_type(board, deck, player, players)
    assert result == True

# Test 4: Carta de tipo "p" (robar 2 cartas)
def test_card_played_type_draw_2():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Pl1yer")
    player_2 = Player(name="Test Pl4yer 2")
    players = [player, player_2]
    
    card = Card(name="r-p", filename=CARD_IMAGE_PATH + "red_picker.png")
    board.update_Board(card)
    
    result = card_played_type(board, deck, player, players)
    assert result == False  # La funcion no debe devolver drop_again

# Test 5: Carta de tipo "s" (saltar turno)
def test_card_played_type_skip_turn():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Player")
    player_2 = Player(name="Test Pl4yer 2")
    players = [player, player_2]
    
    card = Card(name="r-s", filename=CARD_IMAGE_PATH + "red_skip.png")
    board.update_Board(card)
    
    result = card_played_type(board, deck, player, players)
    assert result == False

# Test 6: Carta de tipo "r" (invertir orden de turnos)
def test_card_played_type_reverse_turns():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Player")
    players = [player]
    
    card = Card(name="r-r", filename=CARD_IMAGE_PATH + "red_reverse.png")
    board.update_Board(card)
    
    result = card_played_type(board, deck, player, players)
    assert result == False 

# Test 7: Carta numérica sin efectos adicionales
def test_card_played_type_number_card():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Player")
    players = [player]
    
    card = Card(name="r-5", filename=CARD_IMAGE_PATH + "red_5.png")
    board.update_Board(card)
    
    result = card_played_type(board, deck, player, players)
    assert result == False 

# Test 8: Carta numérica pero tablero vacio (caso especial)
def test_card_played_type_number_card_empty_board():
    board = Board(name="Test Board")
    deck = Deck(name="Test Deck", input_deck=[])
    player = Player(name="Test Player")
    players = [player]
    
    card = Card(name="r-5", filename=CARD_IMAGE_PATH + "red_5.png")
    board.card_stack = []  # Tablero vacio
    
    result = card_played_type(board, deck, player, players)
    assert result == board.turn_iterator 
###