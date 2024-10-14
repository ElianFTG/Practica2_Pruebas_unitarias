import pytest
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AI_classes import *

def test_leaf_initialization():
    leaf = Leaf(10)
    assert leaf.value == 10

def test_branch_initialization():
    leaf1 = Leaf(1)
    leaf2 = Leaf(2)
    branch = Branch(Branch_q="Is it a leaf?", child_1=leaf1, child_2=leaf2)
    
    assert branch.question == "Is it a leaf?"
    assert branch.child_1 == leaf1
    assert branch.child_2 == leaf2

def test_get_offshoots():
    leaf1 = Leaf(1)
    leaf2 = Leaf(2)
    branch = Branch(child_1=leaf1, child_2=leaf2)
    
    assert branch.get_offshoots() == (leaf1, leaf2)