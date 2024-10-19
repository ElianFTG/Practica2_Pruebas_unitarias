import pytest
import sys
import os
from AI_classes import *
from game_classes import *
from Card_Guess_Tree import *

# Mocks para read_Card_Tree_basic y read_Card_Tree_values
def mock_read_Card_Tree_basic(Card_Tree):
    """ Retorna un subárbol izquierdo y derecho falso. """
    if Card_Tree == "None":
        return (None, None)
    if Card_Tree == "only_left":
        return (1, None)
    if Card_Tree == "only_right":
        return (None, 1)
    return (1, 1)

def mock_read_Card_Tree_values(right_tree, depth):
    """ Retorna valores falsos para una carta. """
    return ("red", "5", "Player1")

# Test 1: Card_Tree es None
def test_travel_recus_none_tree():
    Card_Guess_list = []
    travel_recus(None, 0, Card_Guess_list)
    assert Card_Guess_list == []

# Test 2: Ambos subárboles son None

def test_travel_recus_empty_subtrees(mocker):
    mocker.patch("Card_Guess_Tree.read_Card_Tree_basic").return_value = mock_read_Card_Tree_basic("None")
    Card_Guess_list = []
    travel_recus("None", 0, Card_Guess_list)
    assert Card_Guess_list == []  

# Test 3: Subárbol derecho contiene información
def test_travel_recus_right_tree(monkeypatch):
    monkeypatch.setattr('Card_Guess_Tree.read_Card_Tree_basic', mock_read_Card_Tree_basic)
    monkeypatch.setattr('Card_Guess_Tree.read_Card_Tree_values', mock_read_Card_Tree_values)
    Card_Guess_list = []
    travel_recus("only_right", 0, Card_Guess_list)
    assert Card_Guess_list == ["red", "5", "Player1"]  # Se deben agregar los valores de la carta


### travel_Card_Guess_Tree Branch coverage
def test_Card_Guess_Tree():
    card_tree = Card_Guess_Tree("Test_Tree", max_depth=3)

    card1 = Card("r-5", "small_cards/red_5.png", "Player1")
    card2 = Card("b-3", "small_cards/blue_3.png", "Player2") 
    card3 = Card("g-7", "small_cards/green_7.png", "Player3")
    card4 = Card("y-1", "small_cards/yellow_1.png", "Player4") 
    card5 = Card("w-d", "small_cards/wild_pick_four.png", "Player5")
    card_tree.update_card_tree(card1)
    card_tree.update_card_tree(card2)
    card_tree.update_card_tree(card3)
    card_tree.update_card_tree(card4)
    card_tree.update_card_tree(card5)
    output = travel_Card_Guess_Tree(card_tree.Guess_Tree, max_depth=5)
    assert output == [
        ('w','d','Player5'),
        ('y','1',None)
    ]
