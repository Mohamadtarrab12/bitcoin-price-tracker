import csv
import configparser
import requests
from datetime import datetime
import os

# Chemin vers le fichier de configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

def load_config(filename):
    """Charge les informations de configuration depuis un fichier INI."""
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        'output_file': config.get('files', 'output_file')
    }

def fetch_bitcoin_price(symbol):
    """Récupère le prix du Bitcoin depuis l'API CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Assure que la réponse est réussie
        data = response.json()
        return data['bitcoin'][symbol]
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None

def write_to_file(filename, price):
    """Écrit les données dans un fichier CSV."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [current_time, price]

    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["DateTime", "BitcoinPrice"])
        writer.writerow(row)
    print("Données écrites dans le fichier avec succès.")

def main():
    """Fonction principale qui coordonne la récupération et l'insertion des données."""
    config = load_config(config_path)
    bitcoin_price = fetch_bitcoin_price("eur")
    
    if bitcoin_price:
        write_to_file(config['output_file'], bitcoin_price)

if __name__ == "__main__":
    main()
