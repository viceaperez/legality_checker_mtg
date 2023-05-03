import requests


def deck_check(deck: dict, deck_format: str) -> bool:
    reasons = ""

    if format == "commander":
        if deck.get("maincount") != 99:
            reasons += f"Deck contains {deck.get('maincount')} card instead of 99.\n"

        if deck.get("sidecount") != 1:
            reasons += f"Deck contains more than 1 commander.\n"

    else:
        if deck.get("maincount") < 60:
            reasons += f"Deck contains too few cards (minimum quantity is 60).\n"

        if deck.get("sidecount") > 15:
            reasons += f"Sideboard contains too many cards (maximun quantity is 15).\n"

    for card in deck.get("maindeck"):
        reasons += card_legality_check(deck_format, *card.values())

    for card in deck.get("sidedeck"):
        reasons += card_legality_check(deck_format, *card.values())

    if not reasons:
        reasons += f"The deck is legal in {deck_format}"
    return reasons


def card_legality_check(format: str, card_name: str, quantity: int) -> str:
    reasons = ""

    r = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    response = requests.get(r).json()
    try:
        response.get('legalities').get(format)
    except AttributeError:
        # 9
        # print(response)
        reasons += f"{card_name} not found."
        return reasons
    if response.get('legalities').get(format) != "legal":
        reasons += f"{card_name} is {response.get('legalities').get(format).replace('_', ' ')} in {format}.\n"

    if (response.get("name") not in
            ["Persistent Petitioners", "Rat Colony", "Relentless Rats", "Shadowborn Apostle", "Dragon's Approach"]):

        if not response.get("type_line").startswith("Basic") and quantity > 4:
            reasons += f"Too many copies of {card_name}\na deck can have up to 4 copies of it.\n"

    if response.get("name") == "Seven Dwarves" and quantity > 7:
        reasons += f"Too many copies of {card_name}\na deck can have up to 7 copies of it.\n"

    return reasons


# TODO: use regex to check deck_text
def text_check(deck_text: str) -> str:
    reason = ""

    return reason
