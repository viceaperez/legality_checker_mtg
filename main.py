import requests

def run():
    deck = read_deckfile('torbran.txt')
    # print(deck)
    msg = validate("commander", deck)
    print(msg)

def read_deckfile(filename: str) -> dict:
    
    maindeck = []
    maincount = 0
    sideboard = False    
    sidedeck = []
    sidecount = 0
    
    for line in open(filename, "r").readlines():
        line = line.strip()
        if not line: continue
        
        if line.startswith("#"):
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


def validate(format: str, deck: dict) -> bool:

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
        reasons += check_legality(*card.values(), format=format)
    
    for card in deck.get("sidedeck"):
        reasons += check_legality(*card.values(), format=format)
    
    if not reasons:
        reasons += f"The deck is legal in {format}"
    return reasons

def check_legality(cardname: str, quantity: int, format: str) -> str:
    reasons = ""
    
    r =  f"https://api.scryfall.com/cards/named?exact={cardname}"
    response = requests.get(r).json()
    
    if response.get('legalities').get(format) != "legal":
        reasons += f"{cardname} is {response.get('legalities').get(format).replace('_',' ')} in {format}.\n"

    if (response.get("name") not in 
        ["Persistent Petitioners", "Rat Colony","Relentless Rats","Shadowborn Apostle","Dragon's Approach"]):
        
        if not response.get("type_line").startswith("Basic") and quantity > 4:
            reasons += f"Too many copies of {cardname}\na deck can have up to 4 copies of it.\n"
    
    if response.get("name") == "Seven Dwarves" and quantity > 7:
        reasons += f"Too many copies of {cardname}\na deck can have up to 7 copies of it.\n"

    return reasons

if __name__ == "__main__":
    run()
