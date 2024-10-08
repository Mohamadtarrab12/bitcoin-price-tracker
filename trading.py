import configparser
import requests
import csv
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

def fetch_bitcoin_price():
    """Récupère le prix du Bitcoin depuis l'API CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['bitcoin']['eur']
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None

def write_to_csv(file_path, price):
    """Écrit les données dans un fichier CSV."""
    # Vérifie si le fichier existe
    if not os.path.isfile(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return

    # Ouvre le fichier en mode 'a' (append) pour ajouter des données
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Écrit l'en-tête uniquement si le fichier est nouveau
        if os.path.getsize(file_path) == 0:  # Vérifie si le fichier est vide
            writer.writerow(['DateTime', 'BitcoinPrice'])
        
        # Écrit les nouvelles données
        writer.writerow([datetime.now().isoformat(), price])

    print("Données écrites dans le fichier avec succès.")

def main():
    """Fonction principale qui coordonne la récupération et l'écriture des données."""
    config = load_config(config_path)
    bitcoin_price = fetch_bitcoin_price()
    write_to_csv(config['output_file'], bitcoin_price)

if __name__ == "__main__":
    main()
