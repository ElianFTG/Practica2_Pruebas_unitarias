import pytest
from AI_functs import *
from game_classes import *
from unittest.mock import patch, MagicMock


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

# Tests para play_win

@pytest.fixture
def setup_play_win():
    player = Player("TestPlayer")
    players = [Player("Player1"), Player("Player2")]
    board = Board("TestBoard")
    input_deck = [Card("r_1", "small_cards/red_1.png"), 
        Card("b_1", "small_cards/blue_1.png"), Card("g_1", "small_cards/green_1.png"), Card("y_1", "small_cards/yellow_1.png")]
    deck = Deck("TestDeck", input_deck)
    return player, players, board, deck

@pytest.fixture
def mock_ai_card_logic(monkeypatch):
    def mock_func(*args, **kwargs):
        pass
    monkeypatch.setattr(AI_card_logic, "AI_card_played_type", mock_func)

def test_play_win(setup_play_win, mock_ai_card_logic):
    player, players, board, deck = setup_play_win
    player.hand = [Card("r_5", "small_cards/red_5.png")]
    player.hatval = {players[0]: 5}
    
    play_win(board, deck, player, players)
    
    assert len(player.hand) == 0
    assert board.color == "r"

def test_play_win_comodin(setup_play_win, mock_ai_card_logic):
    player, players, board, deck = setup_play_win
    player.hand = [Card("w_1", "small_cards/wild_color_changer.png"), Card("r_5", "small_cards/red_5.png")]
    player.hatval = {players[0]: 5}
    
    play_win(board, deck, player, players)
    
    assert len(player.hand) == 0
    assert board.color in ["r", "g", "b", "y"]

def test_play_win_vacio(setup_play_win, mock_ai_card_logic):
    player, players, board, deck = setup_play_win
    player.hand = []
    player.hatval = {players[0]: 5}
    
    play_win(board, deck, player, players)
    
    assert len(player.hand) == 0
    assert board.color in ["r", "g", "b", "y"]

# AI_functs.py                      133      9    93%   41-44, 57, 100-101, 147-148, 195, 256

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
    return Player("TestPlayer", hand=[
        Card("w_0", "small_cards/wild_color_changer.png"), 
        Card("g_3", "small_cards/green_3.png"),  
    ])

@pytest.fixture
def mock_wild_player_2():
    return Player("TestBadPlayer",hand=[
        Card("w_0", "small_cards/wild_color_changer.png"),
        Card("w_1", "small_cards/wild_color_changer.png"),
    ])

# Tests para fetch_most_common_color

def test_fetch_most_common_color(mock_player):
    assert fetch_most_common_color(mock_player) == "r"

def test_fmcc_con_comodin(mock_wild_player):
    assert fetch_most_common_color(mock_wild_player) == "g"

def test_fmcc_todos_comodines(mock_wild_player_2):
    random_color = fetch_most_common_color(mock_wild_player_2)
    assert random_color in ["b", "r", "g", "y"]

# Tests para fetch_most_common_color_playable

@pytest.fixture
def mock_board():
    return Board("TestBoard")

def test_fetch_most_common_color_playable(mock_board, mock_player):
    result = fetch_most_common_color_playable(mock_board, mock_player)
    assert result == "r"

def test_fmccp_con_comodin(mock_wild_player):
    board = Board("TestBoard")
    result = fetch_most_common_color_playable(board, mock_wild_player)
    assert result == "g"

def test_fmccp_todos_comodines(mock_wild_player_2, mocker):
    board = Board("TestBoard")
    mocker.patch('card_logic.card_allowed', return_value=[])
    result = fetch_most_common_color_playable(board, mock_wild_player_2)
    assert result in ["b", "r", "g", "y"]

# Tests para fetch_most_common_type

@pytest.fixture
def mock_tied_type_player():
    return Player("TestPlayer",hand=[
        Card("r_2", "small_cards/red_1.png", None),
        Card("g_2", "small_cards/green_1.png", None),
        Card("r_3", "small_cards/red_1.png", None),
        Card("g_3", "small_cards/green_1.png", None)
    ])

def test_fetch_most_common_type(mock_player):
    result = fetch_most_common_type(mock_player)
    assert result == "2"

def test_fmct_empate(mock_tied_type_player):
    result = fetch_most_common_type(mock_tied_type_player)
    assert result == ["2", "3"]

# Tests para fetch_most_common_type_playable

@pytest.fixture
def mock_player_reds():
    return Player("TestPlayer",hand=[
        Card("r_2", "small_cards/red_2.png"),  # Carta roja
        Card("r_3", "small_cards/red_3.png"),  # Carta roja
    ])

def test_fetch_most_common_type_playable(mock_player_reds):
    board = Board("TestBoard")
    result = fetch_most_common_type_playable(board, mock_player_reds)
    assert result == "2" 
    
# Tests para fetch_oldest_card

@pytest.fixture
def mock_player_with_old_card():
    return Player("TestPlayer",hand=[
        Card("r_1", "small_cards/red_1.png", old_val=3),
        Card("g_1", "small_cards/green_1.png", old_val=5), 
    ])

def test_fetch_oldest_card(mock_player_with_old_card):
    board = Board("TestBoard")
    result = fetch_oldest_card(board, mock_player_with_old_card)
    assert result == (5, 1) 

# Tests para fetch_possible_winner

@pytest.fixture
def mock_winners():
    return [
        Player("Player1", hand=[Card("r_1", "small_cards/red_1.png")]),  # Tiene 1 carta
        Player("Player2", hand=[Card("g_1", "small_cards/green_1.png")]),  # Tiene 1 carta
        Player("AI_Player", hand=[Card("b_1", "small_cards/blue_1.png"), Card("b_2", "small_cards/blue_2.png")]),  # Tiene 2 cartas
    ]

def test_fetch_possible_winner(mock_winners):
    board = Board("TestBoard")
    result = fetch_possible_winner(board, mock_winners[2], mock_winners)
    assert result == (True, [mock_winners[0], mock_winners[1]])

def test_fpw_sin_ganadores():
    players_no_winners = [
        Player("Player1", hand=[Card("r_1", "small_cards/red_1.png"), Card("r_2", "small_cards/red_2.png")]),  
        Player("Player2", hand=[Card("g_1", "small_cards/green_1.png"), Card("g_2", "small_cards/green_2.png")]),  
        Player("AI_Player", hand=[Card("b_1", "small_cards/blue_1.png"), Card("b_2", "small_cards/blue_2.png")]),  # 
    ]
    board = Board("TestBoard")
    result = fetch_possible_winner(board, players_no_winners[2], players_no_winners)
    assert result == (False, None)

#Test para def fetch_hate_cards(board, player):

class MockCard:
    def __init__(self, card_type):
        self.type = card_type

def test_fetch_hate_cards():
    # Preparamos el entorno de prueba
    board = Board("TestBoard")
    player = Player("Player1", [MockCard("d"), MockCard("a"), MockCard("s"), MockCard("b"), MockCard("p")])
    
    # Llamamos a la función que estamos probando
    result = fetch_hate_cards(board, player)

    # Verificamos el resultado
    assert len(result) == 3  # Debe haber 3 cartas "hateables" jugables
    assert result[0][0].type == "d"  
    assert result[0][1] == 0 
    assert result[1][0].type == "s" 
    assert result[1][1] == 2  
    assert result[2][0].type == "p"  

#Tests para stop_winners

def mock_fetch_hate_cards(board, player):
    return [('hate_card_type', 0)]

# Mock de la lógica de IA
class MockAI:
    called = False  

    @staticmethod
    def AI_card_played_type(board, deck, player, players, possible_winner):
        MockAI.called = True 

class MockPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.play_card_called_with = None

    def play_card(self, board, card_ID):
        self.play_card_called_with = (board, card_ID)

@pytest.fixture
def setup_stop(monkeypatch):
    board = Board("Test Board")
    deck = Deck("Test Deck", [])
    player = MockPlayer("Player 1") 
    players = [Player(f"Player {i}") for i in range(2, 5)]  
    possible_winner = Player("Possible Winner")
    monkeypatch.setattr('AI_functs.fetch_hate_cards', mock_fetch_hate_cards) 
    monkeypatch.setattr('AI_functs.AI_card_logic.AI_card_played_type', MockAI.AI_card_played_type)

    return board, deck, player, players, possible_winner

def test_stop_winners(setup_stop):
    board, deck, player, players, possible_winner = setup_stop

    # Llama a la función que estamos probando
    stop_winners(board, deck, player, players, possible_winner)

    # Verifica que se haya llamado a play_card con el argumento correcto
    assert player.play_card_called_with is not None  # Verifica que se haya llamado
    assert player.play_card_called_with[0] == board  # Verifica que el primer argumento sea el tablero
    assert player.play_card_called_with[1] == 0  # Verifica que el segundo argumento sea el índice de la carta de odio

    # Verifica que se haya llamado a AI_card_logic.AI_card_played_type
    assert MockAI.called  # Verifica que la función fue llamada
    MockAI.called = False 

#Tests para fetch_hate_priority

@pytest.fixture
def player():
    return Player("TestPlayer")

@pytest.fixture
def players():
    return [Player("Player1"), Player("Player2"), Player("Player3")]

def test_fetch_hate_priority(player, players):
    player.hatval = {players[0]: 5, players[1]: 10, players[2]: 3}
    max_hate, hate_player = fetch_hate_priority(player, players)
    assert max_hate == 10
    assert hate_player == players[1]

def test_fhp_sin_odio(player, players):

    player.hatval = {}
    max_hate, hate_player = fetch_hate_priority(player, players)
    # Verificamos que se haya manejado correctamente el caso de hate_player None
    assert max_hate == 0
    assert hate_player in players
    assert len(player.hatval) == 3
    assert all(player.hatval[p] == 0 for p in players)


#Tests para do_nothing

@pytest.fixture
def mock_deck():
    class MockDeck:
        def grab_card(self):
            return Card("g_1", "small_cards/green_1.png") 
    return MockDeck()

def test_do_nothing(mock_deck, capsys):
    player = Player("Player 1")
    do_nothing(mock_deck, player) 
    captured = capsys.readouterr()
    assert captured.out.strip() == "NOTHING TO PLAY SKIPPING"
    assert len(player.hand) == 1  
    assert player.hand[0].name == "g_1"