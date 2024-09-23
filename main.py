import requests
import json
import time

# Basis-URL der API
base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'


# Funktion zum Abrufen der Daten
def fetch_all_yugioh_cards():
    try:
        # Anfrage an die API senden
        response = requests.get(base_url)
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
        data = response.json()  # Daten im JSON-Format laden

        # Rückgabe der Karteninformationen
        return data['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return []


# Funktion zum Speichern der Daten als JSON-Datei
def save_to_json(card_data, file_name):
    # Speichern der Daten im JSON-Format
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(card_data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_name}")


# Hauptfunktion zum Ausführen des Skripts
def main():
    print("Fetching Yu-Gi-Oh! card data...")
    card_data = fetch_all_yugioh_cards()

    if card_data:
        print(f"Fetched {len(card_data)} cards.")

        # Speichern der Daten in einer JSON-Datei
        save_to_json(card_data, 'yugioh_cards.json')
    else:
        print("No card data fetched.")


if __name__ == "__main__":
    main()
