import configparser
import requests
import psycopg2
import os

# Chemin vers le fichier de configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

def load_config(filename):
    """Charge les informations de configuration depuis un fichier INI."""
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        'dbname': config.get('database', 'dbname'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'host': config.get('database', 'host'),
        'port': config.get('database', 'port')
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

def connect_to_db(config):
    """Établit une connexion à la base de données PostgreSQL."""
    try:
        return psycopg2.connect(
            dbname=config['dbname'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
    except psycopg2.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

def insert_data(conn, price):
    """Insère les données dans la table PostgreSQL."""
    insert_query = """
    INSERT INTO dev.bitcoin(prix)
    VALUES (%s);
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_query, (price,))
            conn.commit()
            print("Données insérées avec succès.")
    except psycopg2.Error as e:
        print(f"Erreur lors de l'insertion des données : {e}")

def main():
    """Fonction principale qui coordonne la récupération et l'insertion des données."""
    config = load_config(config_path)
    bitcoin_price = fetch_bitcoin_price("eur")
    
    if bitcoin_price:
        conn = connect_to_db(config)
        
        if conn:
            insert_data(conn, bitcoin_price)
            conn.close()

if __name__ == "__main__":
    main()
