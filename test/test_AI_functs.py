import pytest
from AI_functs import *
from game_classes import *


def test_get_rand_type():
    valid_types = ["p", "s", "r", "c", "d", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for _ in range(100):  
        card_type = get_rand_type()
        assert card_type in valid_types, f"Tipo de carta invalida: {card_type}"

def test_get_rand_color():
    valid_colors = ["b", "r", "g", "y"]
    for _ in range(100):
        card_color = get_rand_color()
        assert card_color in valid_colors, f"Color de carta invalida: {card_color}"

# FALTA play_win(): -> SUS METODOS UTILIZADOS son de otros archivos sin probar o de funciones aun sin su test




#-----------------------------FALTA

@pytest.fixture
def mock_player():
    return Player("TestPlayer",hand=[
        Card("r_2", "small_cards/red_1.png", None),
        Card("r_3", "small_cards/red_1.png", None),
        Card("g_2", "small_cards/green_1.png", None),
        Card("r_4", "small_cards/red_1.png", None)
    ])

@pytest.fixture
def mock_wild_player():
    return Player("TestPlayer",hand=[
        Card("w_2", "small_cards/red_1.png", None),
        Card("w_2", "small_cards/red_1.png", None),
        Card("g_4", "small_cards/green_1.png", None),
        Card("w_4", "small_cards/red_1.png", None)
    ])

@pytest.fixture
def mock_wild_player_2():
    return Player("TestBadPlayer",hand=[
        Card("w_2", "small_cards/red_1.png", None),
        Card("w_3", "small_cards/red_1.png", None),
    ])

# Tests para fetch_most_common_color

def test_fetch_most_common_color(mock_player):
    assert fetch_most_common_color(mock_player) == "r"

def test_fetch_most_common_color_con_comodin(mock_wild_player):
    assert fetch_most_common_color(mock_wild_player) == "g"

def test_fetch_most_common_todos_comodines(mock_wild_player_2):
    random_color = fetch_most_common_color(mock_wild_player_2)
    assert random_color in ["b", "r", "g", "y"]

# Tests para fetch_most_common_color_playable

@pytest.fixture
def mock_board():
    return Board("TestBoard")

def test_fetch_most_common_color_playable(mock_board, mock_player):
    result = fetch_most_common_color_playable(mock_board, mock_player)
    assert result == "r"

#-----------------------------FALTA




# Tests para fetch_most_common_type

@pytest.fixture
def mock_tied_type_player():
    return Player(hand=[
        Card("r_2", "small_cards/red_1.png", None),
        Card("g_2", "small_cards/green_1.png", None),
        Card("r_3", "small_cards/red_1.png", None),
        Card("g_3", "small_cards/green_1.png", None)
    ])

def test_fetch_most_common_type(mock_player):
    result = fetch_most_common_type(mock_player)
    assert result == "2"

def test_fetch_most_common_type_empate(mock_tied_type_player):
    result = fetch_most_common_type(mock_tied_type_player)
    assert result in ["2", "3"]


#Antes de pruebas
#AI_functs.py 132    116    12%   12-14, 23-24, 31-57, 66-80, 89-110, 119-128, 138-153, 163-173, 187-204, 214-218, 229-240, 250-267, 276-278 
# Prueba tipo y color
# AI_functs.py                  132    112    15%   31-57, 66-80, 89-110, 119-128, 138-153, 163-173, 187-204, 214-218, 229-240, 250-267, 276-278
# Despues de ejecutar funcion mas comun test 1 AI_functs.py                  
# AI_functs.py                 132    103    22%   31-57, 70, 78, 89-110, 119-128, 138-153, 163-173, 187-204, 214-218, 229-240, 250-267, 276-278
# Test 2
# AI_functs.py                  132    102    23%   31-57, 78, 89-110, 119-128, 138-153, 163-173, 187-204, 214-218, 229-240, 250-267, 276-278
# Test 3
# AI_functs.py                  132    101    23%   31-57, 89-110, 119-128, 138-153, 163-173, 187-204, 214-218, 229-240, 250-267, 276-278
