import requests
from PIL import Image
from io import BytesIO


ppi = 300
mtg_card_size = (int(2.5 * ppi), int(3.5 * ppi))


def plot_deck(deck: dict, basic:bool, dimentions:tuple, deck_file:str, gap=1):
    
    # Repartir el mazo en el lienzo, si no se puede, crear otro
    # Dimensiones de las cartas y del lienzo final
    canvas_size = dimentions
    
    # Número máximo de cartas por hoja
    cards_per_row = (canvas_size[0] - 100) // (mtg_card_size[0] + 1)
    cards_per_col = (canvas_size[1] - 100) // (mtg_card_size[1] + 1)
    max_cards_per_page = cards_per_row * cards_per_col

    # Contadores para el número de cartas y la página actual
    card_count = 0
    page_count = 1

    # Crear el lienzo final
    width, height = canvas_size
    result = Image.new('RGBA', (width, height), (255, 255, 255, 255))

    # Agregar cada carta al lienzo final
    for card in deck.get('maindeck'):
        card_name = card.get("cardname")
        quantity = card.get("quantity")
        
        card_width, card_height = mtg_card_size
        
        r = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
        response = requests.get(r).json()
        
        # Filtrar por tipo de carta
        if not basic:   
            if 'Basic Land' in response.get('type_line'):
                continue
                
        print(card_name)
        print()
        card_faces = []
        # Verificar el número de objetos en la respuesta
        
        if 'image_uris' not in list(response):
            # Si la respuesta es una lista, agregar todos los objetos al lienzo
            for face in response.get('card_faces'):
                # Obtener la URL de la imagen
                large_url = face.get('image_uris').get('large')
                card_faces.append(large_url)
        else:
            large_url = response.get('image_uris').get('large')
            card_faces.append(large_url)
                
        for face in card_faces:
            # Obtener la imagen desde la API y guardarla temporalmente
            
            res = requests.get(face)
            img = Image.open(BytesIO(res.content))
            img = img.resize(mtg_card_size)
            
            for i in range(quantity):
                # Agregar la imagen de la carta al lienzo final
                x = 50 + (card_count // cards_per_row) * (card_width + gap)
                y = 50 + (card_count % cards_per_row) * (card_height + gap)
                
                result.paste(img, (x, y))
                card_count += 1
            
                # Si se llega al máximo de cartas por hoja, guardar la imagen actual y crear una nueva
                if card_count == max_cards_per_page:
                    # Guardar la imagen actual con un nombre de archivo basado en el nombre del mazo y el número de página
                    
                    result.save(f"{deck_file}_{str(page_count)}.png")
                    # Crear una nueva imagen para la siguiente página
                    page_count += 1
                    result = Image.new('RGBA', (width, height), (255, 255, 255, 255))
                    card_count = 0
    
    # Guardar la última página del mazo
    if card_count > 0:
        result.save(f"{deck_file}_{str(page_count)}.png")
                
    
    return "Deck" + deck_file + "Saved"
