import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# Funktion um ein einzelnes Deck auszulesen
def scrape_deck(deck_url):
    deck_response = requests.get(deck_url)
    deck_soup = BeautifulSoup(deck_response.text, 'html.parser')

    # Deckkarten extrahieren
    main_deck = deck_soup.find('div', id='main_deck')
    side_deck = deck_soup.find('div', id='side_deck')
    extra_deck = deck_soup.find('div', id='extra_deck')

    def extract_cards(deck_div):
        if deck_div:
            return [card.text.strip() for card in deck_div.find_all('span', class_='card-name')]
        return []

    main_deck_cards = extract_cards(main_deck)
    side_deck_cards = extract_cards(side_deck)
    extra_deck_cards = extract_cards(extra_deck)

    return main_deck_cards, side_deck_cards, extra_deck_cards


# Funktion um alle Decks von einer Seite zu extrahieren
def scrape_decks_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Deck-Container identifizieren
    deck_articles = soup.find_all('div', class_='p-2 deck_article-card-container')

    all_decks = []

    # Für jeden Deck-Container die URL finden und Deck-Karten extrahieren
    for deck_article in deck_articles:
        deck_link = deck_article.find('a')['href']
        deck_url = f"https://ygoprodeck.com{deck_link}"

        deck_name = deck_article.find('h5').text.strip()
        views = deck_article.find('span', class_='views').text.strip()

        print(f"Scraping deck: {deck_name}, Views: {views}")

        main_deck, side_deck, extra_deck = scrape_deck(deck_url)

        all_decks.append({
            'deck_name': deck_name,
            'views': views,
            'main_deck': main_deck,
            'side_deck': side_deck,
            'extra_deck': extra_deck
        })

        time.sleep(1)  # Kurze Pause, um den Server nicht zu überlasten

    return all_decks


# Funktion um mehrere Seiten zu durchlaufen
def scrape_all_decks(base_url, num_pages):
    all_decks = []

    for page_num in range(num_pages):
        offset = page_num * 20  # 20 Decks pro Seite
        page_url = f"{base_url}&offset={offset}"

        print(f"Scraping page {page_num + 1}: {page_url}")
        page_decks = scrape_decks_from_page(page_url)
        all_decks.extend(page_decks)

        time.sleep(2)  # Pause zwischen den Seiten

    return all_decks


# Start des Scraping-Prozesses
base_url = "https://ygoprodeck.com/deck-search/?sort=Deck%20Views"
num_pages = 5  # Anzahl der Seiten, die gescraped werden sollen (anpassbar)

all_decks = scrape_all_decks(base_url, num_pages)

# Daten in ein Pandas DataFrame umwandeln
df = pd.DataFrame(all_decks)

# Daten in eine CSV-Datei exportieren
df.to_csv('ygopro_decks.csv', index=False)

print("Scraping abgeschlossen. Decks gespeichert in 'ygopro_decks.csv'.")
