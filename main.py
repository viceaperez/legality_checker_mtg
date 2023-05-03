from Checker import deck_check
from Plotter import plot_deck
from prettytable import PrettyTable

import argparse
parser = argparse.ArgumentParser(description='Check the legality of a Magic: The Gathering deck using the Scryfall API')

parser.add_argument('-l', '--list', type=str, required=True, help='The filename of the decklist to check')
parser.add_argument('-f', '--format', type=str, default="modern", help='The format to check the deck against (e.g. standard, modern, pioneer)')
parser.add_argument('-p', '--print', action='store_true', default=False, help='Print the decklist in a formatted way')
parser.add_argument('-b', '--basic', action='store_true', default=False, help='Print the decklist with the basic lands')
args = parser.parse_args()

# Access the arguments using args.format, args.list, and args.print
deck_file = args.list
deck_format = args.format
print_decklist = args.print
basic_print = args.basic


def run():
    deck = read_deckfile(deck_file)
    deck_show(deck)
    msg = deck_check(deck, deck_format)
    print()
    print(msg)
    
    if not print_decklist:
        return

    dimentions = ask_dimensions()
    print("These are the dimentions (%s x %s)" % dimentions)
    
    result = plot_deck(deck, basic_print, dimentions, deck_file)
    print(result)

def deck_show(deck):

    # Creamos la tabla miandeck
    main = PrettyTable()
    main.field_names = ["Card", "Quantity"]
    
    # Creamos la tabla sidedeck
    side = PrettyTable()
    side.field_names = ["Card", "Quantity"]

    
    print("|\t\tMAIN DECK\t\t|")
    for card in deck.get("maindeck"):
        card_name, quantity = card.get("cardname"), card.get("quantity")
        main.add_row([card_name, quantity])
    # Mostramos la tabla
    print(main)
    print("|\t\SIDE DECK\t\t|")
    for card in deck.get("sidedeck"):
        card_name, quantity = card.get("cardname"), card.get("quantity")
        side.add_row([card_name, quantity])
    # Mostramos la tabla
    print(side)


def ask_dimensions():
    types = {
        "A4": (21.0, 29.7),
        "Letter": (21.6, 27.9),
        "Custom": (0, 0)
    }
    print("Choose a paper size:", str(list(types.keys())))
    op = input()
    if op == "Custom":
        types["Custom"] = (float(input("Enter value for Custom Width (cm): ")), float(input("Enter value for Custom Height (cm): ")))
    
    width_cm, height_cm = types[op.capitalize()]
    ppi = 300
    width_px = int(width_cm * ppi / 2.54)
    height_px = int(height_cm * ppi / 2.54)
    
    return (width_px, height_px)


def read_deckfile(filename: str) -> dict:
    maindeck = []
    maincount = 0
    sideboard = False
    sidedeck = []
    sidecount = 0

    for line in open(filename, "r", encoding="utf-8").readlines():
        line = line.strip()
        if not line:
            sideboard = True
            continue

        reg = line.split(" ")
        card = " ".join(reg[1:])
        quantity = int(reg[0])
        if sideboard:
            sidedeck.append({"cardname": card, "quantity": quantity})
            sidecount += quantity
        else:
            maindeck.append({"cardname": card, "quantity": quantity})
            maincount += quantity

    return {"maindeck": maindeck,
            "maincount": maincount,
            "sidedeck": sidedeck,
            "sidecount": sidecount,
            }


if __name__ == "__main__":
    run()
