import pytest
from deck_gen import *

def test_generate_cards():
    cards = generate_cards() 

    # 60 cartas en total
    assert len(cards) == 60, "Se esperaban 60 cartas, pero se generaron {}".format(len(cards))

    # Cartas de colores generadas correctamente
    expected_colors = ["b_", "r_", "g_", "y_"]
    expected_card_types = ["picker", "skip", "reverse", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for color in expected_colors:
        for ct in expected_card_types:
            card_name = f"{color}{ct}"
            assert any(card.name == card_name for card in cards), f"Se esperaba la carta {card_name} en la lista de cartas generadas"

    # Creacion de 4 cartas +4
    wild_pick_four_count = sum(1 for card in cards if "w_d" in card.name)
    assert wild_pick_four_count == 4, "Se esperaban 4 cartas +4, resultado -> {}".format(wild_pick_four_count)

    # Creacion de 4 cartas de cambio de color
    wild_color_count = sum(1 for card in cards if "w_c" in card.name)
    assert wild_color_count == 4, "Se esperaban 4 cartas de cambio de color, resultado -> {}".format(wild_color_count)

def test_card_shuffler():
    # Crea una lista más grande de cartas de prueba
    cartas = [game_classes.Card(f"b_{i}", f"small_cards/blue_{i}.png", None) for i in range(1, 10)] 
    nombres_cartas = [card.name for card in cartas]
    barajadas = card_shuffler(cartas)   
    nombres_cartas_barajadas = [card.name for card in barajadas]
    assert nombres_cartas_barajadas != nombres_cartas, "La lista de cartas no fue barajada correctamente."
    assert len(barajadas) == len(cartas), "La cantidad de cartas ha cambiado." 
    assert sorted(nombres_cartas_barajadas) == sorted(nombres_cartas), "Lo barajado no tiene las mismas cartas que la original."

def test_build_deck():
    cartas = [
        game_classes.Card("g_1", "small_cards/green_1.png", None),
        game_classes.Card("b_2", "small_cards/blue_2.png", None)
    ]   
    mazo_generado = build_deck("Test Deck", cartas)
    assert mazo_generado.name == "Test Deck", f"El nombre del mazo debería ser Test Deck, pero fue '{mazo_generado.name}'."    
    assert mazo_generado.deck == cartas, "Las cartas en el mazo no coincide con la lista proporcionada."

def test_gen_rand_deck():
    deck = gen_rand_deck("Test Deck", 2)
    assert deck.name == "Test Deck"
    assert len(deck.deck) == 2 * len(generate_cards())
    assert deck.deck != generate_cards() * 2