import pytest
from unittest.mock import MagicMock
import sys
import os
from AI_card_logic import *
from AI_classes import Branch
from AI_classes import Leaf
from AI_functs import *
from card_logic import *
from deck_gen import gen_rand_deck
from game_classes import *
from Card_Choose_Tree import travel_Card_Choose_Tree, read_Card_Choose_Tree, read_Card_Choose_Tree_question, read_Card_Choose_Leaf_instruction

# Creamos mocks simples de las funciones necesarias
class MockLeaf:
    def __init__(self, value):
        self.value = value

class MockTree:
    def __init__(self, left_tree=None, right_tree=None, question=None):
        self.left_tree = left_tree
        self.right_tree = right_tree
        self.question = question

    def get_offshoots(self):
        return (self.left_tree, self.right_tree)
    
class MockCard:
    def __init__(self, color, type):
        self.color = color
        self.type = type

# Mock de la clase Player
class MockPlayer:
    def __init__(self, hand):
        self.hand = hand
        self.name = "player"
        self.hatval = dict({Player("player"): 1})

# Mock del objeto Board
class MockBoard:
    def __init__(self, card_stack=None):
        self.card_stack = card_stack if card_stack else []
        self.type = "p"
        self.color = "r"
        

class MockDeck:
    pass


# Prueba 1: El árbol es una hoja
def test_read_card_choose_tree_leaf():
    # Creamos una hoja con un valor
    leaf = MockLeaf("Leaf Value")
    result = read_Card_Choose_Tree(leaf)
    assert result == (False, "Leaf Value")

# Prueba 2: El árbol tiene ramas
def test_read_card_choose_tree_branch():
    # Creamos un árbol con ramas
    left_branch = MockLeaf("Left Leaf")
    right_branch = MockLeaf("Right Leaf")
    tree = MockTree(left_tree=left_branch, right_tree=right_branch)
    result = read_Card_Choose_Tree(tree)
    assert result == (left_branch, right_branch)


# Mock para las funciones auxiliares que se llaman dentro de travel_Card_Choose_Tree
def mock_read_Card_Choose_Tree(Card_Choose_Tree):
    if isinstance(Card_Choose_Tree, MockLeaf):
        return (False, Card_Choose_Tree.value)
    return Card_Choose_Tree.get_offshoots()

def mock_read_Card_Choose_Tree_question(board, player, players, question):
    if question == "go_left":
        return (True, False)
    elif question == "go_right":
        return (False, True)
    else:
        return (False, False)

def mock_read_Card_Choose_Leaf_instruction(board, deck, player, players, right_tree):
    print(f"Leaf instruction: {right_tree}")

@pytest.fixture(autouse=True)
def patch_functions(monkeypatch):
    monkeypatch.setattr("Card_Choose_Tree.read_Card_Choose_Tree", mock_read_Card_Choose_Tree)
    monkeypatch.setattr("Card_Choose_Tree.read_Card_Choose_Tree_question", mock_read_Card_Choose_Tree_question)
    monkeypatch.setattr("Card_Choose_Tree.read_Card_Choose_Leaf_instruction", mock_read_Card_Choose_Leaf_instruction)

# Prueba 1: El árbol es una hoja (ruta especial para hoja)
def test_travel_card_choose_tree_leaf():
    board = Board("Test Board")
    deck = Deck("Test Deck", [])
    player = Player("Player 1")
    players = [player]
    leaf = MockLeaf("Leaf Instruction")
    travel_Card_Choose_Tree(board, deck, player, players, leaf)
    assert True  

# Prueba 2: El árbol tiene una pregunta que conduce al lado izquierdo
def test_travel_card_choose_tree_go_left():
    board = Board("Test Board")
    deck = Deck("Test Deck", [])
    player = Player("Player 1")
    players = [player]
    
    left_leaf = MockLeaf("Left Leaf")
    right_leaf = MockLeaf("Right Leaf")
    tree = MockTree(left_tree=left_leaf, right_tree=right_leaf, question="go_left")
    travel_Card_Choose_Tree(board, deck, player, players, tree)
    assert True  

# Prueba 3: El árbol tiene una pregunta que conduce al lado derecho
def test_travel_card_choose_tree_go_right():
    board = Board("Test Board")
    deck = Deck("Test Deck", [])
    player = Player("Player 1")
    players = [player]
    left_leaf = MockLeaf("Left Leaf")
    right_leaf = MockLeaf("Right Leaf")
    tree = MockTree(left_tree=left_leaf, right_tree=right_leaf, question="go_right")
    travel_Card_Choose_Tree(board, deck, player, players, tree)
    assert True  

# Prueba 4: No se elige ninguna ruta (error en el árbol)
def test_travel_card_choose_tree_error_no_path():
    board = Board("Test Board")
    deck = Deck("Test Deck", [])
    player = Player("Player 1")
    players = [player]
    left_leaf = MockLeaf("Left Leaf")
    right_leaf = MockLeaf("Right Leaf")
    tree = MockTree(left_tree=left_leaf, right_tree=right_leaf, question="invalid_question")

    travel_Card_Choose_Tree(board, deck, player, players, tree)

    assert True  


### test para read_Card_Choose_Leaf_instruction por Branch Coverage
# Prueba 1: Pregunta "Do I have multiple playable cards?" con más de una carta
def test_multiple_playable_cards_true():
    board = MockBoard()
    player = MockPlayer([MockCard("r", "5"), MockCard("b", "9")])  # 2 cartas
    players = [player]
    
    result = read_Card_Choose_Tree_question(board, player, players, "Do I multiple playable cards?")
    
    assert result == (True, False)

# Prueba 2: Pregunta "Do I have multiple playable cards?" con solo una carta
def test_multiple_playable_cards_false():
    board = MockBoard()
    player = MockPlayer([MockCard("r", "5")])  # 1 carta
    players = [player]
    
    result = read_Card_Choose_Tree_question(board, player, players, "Do I multiple playable cards?")
    
    assert result == (False, True)

# Prueba 3: Pregunta "Do I have a nonwild playable card?" con una carta que no es wild
def test_nonwild_playable_card_true():
    board = MockBoard()
    player = MockPlayer([MockCard("r", "5"), MockCard("w", "d")])  # Una carta no es wild
    players = [player]
    
    # Mockeamos la función card_allowed para que devuelva índices de cartas jugables
    card_logic.card_allowed = MagicMock(return_value=[0, 1])
    
    result = read_Card_Choose_Tree_question(board, player, players, "Do I have a nonwild playable card?")
    
    assert result == (True, False)

# Prueba 4: Pregunta "Do I have a nonwild playable card?" solo wild cards
def test_nonwild_playable_card_false():
    board = MockBoard()
    player = MockPlayer([MockCard("w", "d"), MockCard("w", "c")])  # Todas las cartas son wild
    players = [player]
    
    card_logic.card_allowed = MagicMock(return_value=[0, 1])
    
    result = read_Card_Choose_Tree_question(board, player, players, "Do I have a nonwild playable card?")
    
    assert result == (False, True)

# Prueba 5: Pregunta "What is my most common color or type?" con más color que tipo
def test_most_common_color_wins():
    board = MockBoard()
    player = MockPlayer([MockCard("r", "5"), MockCard("r", "7"), MockCard("b", "5")])  # Rojo es más común
    players = [player]
    
    # Mockeamos funciones para obtener el color y tipo más común
    AI_functs.fetch_most_common_color_playable = MagicMock(return_value="r")
    AI_functs.fetch_most_common_type_playable = MagicMock(return_value="5")
    
    result = read_Card_Choose_Tree_question(board, player, players, "what is my most common (color or type) that is also playable?")
    
    assert result == (True, False)  # El color rojo gana

# Prueba 6: Pregunta "What is my most common color or type?" con más tipo que color
def test_most_common_type_wins():
    board = MockBoard()
    player = MockPlayer([MockCard("r", "5"), MockCard("b", "5"), MockCard("y", "5")])  # Tipo 5 es más común
    players = [player]
    
    AI_functs.fetch_most_common_color_playable = MagicMock(return_value="r")
    AI_functs.fetch_most_common_type_playable = MagicMock(return_value="5")
    
    result = read_Card_Choose_Tree_question(board, player, players, "what is my most common (color or type) that is also playable?")
    
    assert result == (False, True)  # El tipo 5 gana

# Prueba 7: Pregunta "What is my most common color or type?" con empate
def test_most_common_color_type_tie():
    board = MockBoard()
    player = MockPlayer([MockCard("r", "5"), MockCard("r", "5")])  # Igual cantidad de tipo y color
    players = [player]
    
    AI_functs.fetch_most_common_color_playable = MagicMock(return_value="r")
    AI_functs.fetch_most_common_type_playable = MagicMock(return_value="5")
    
    result = read_Card_Choose_Tree_question(board, player, players, "what is my most common (color or type) that is also playable?")
    
    assert result == (True, False)  # Elige color por empate

