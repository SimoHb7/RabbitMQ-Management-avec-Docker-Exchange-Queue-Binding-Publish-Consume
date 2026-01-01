# Script pour créer automatiquement l'exchange, la queue et le binding
# TP 29 - Architecture Microservices

"""
Script de setup automatique pour RabbitMQ
Crée l'exchange 2iteExchange, la queue 2iteQueue et le binding
"""

import pika
import sys

# Configuration
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'

EXCHANGE_NAME = '2iteExchange'
EXCHANGE_TYPE = 'direct'
QUEUE_NAME = '2iteQueue'
ROUTING_KEY = ''  # Vide pour correspondre au TP


def setup_rabbitmq():
    """Créer l'exchange, la queue et le binding"""
    try:
        print("=" * 60)
        print("Setup RabbitMQ - TP29")
        print("=" * 60)
        
        # Connexion
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        
        print(f"\n[1/4] Connexion à RabbitMQ ({RABBITMQ_HOST}:{RABBITMQ_PORT})...")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        print("      ✓ Connexion établie")
        
        # Créer l'exchange
        print(f"\n[2/4] Création de l'exchange '{EXCHANGE_NAME}'...")
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type=EXCHANGE_TYPE,
            durable=True
        )
        print(f"      ✓ Exchange créé (type: {EXCHANGE_TYPE}, durable: true)")
        
        # Créer la queue
        print(f"\n[3/4] Création de la queue '{QUEUE_NAME}'...")
        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True
        )
        print("      ✓ Queue créée (durable: true)")
        
        # Créer le binding
        print(f"\n[4/4] Création du binding...")
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key=ROUTING_KEY
        )
        print(f"      ✓ Binding créé")
        print(f"        Exchange: {EXCHANGE_NAME}")
        print(f"        Queue: {QUEUE_NAME}")
        print(f"        Routing Key: '{ROUTING_KEY}' (vide)")
        
        # Fermer la connexion
        connection.close()
        
        print("\n" + "=" * 60)
        print("✓ Setup terminé avec succès!")
        print("=" * 60)
        print("\nAccédez à l'interface web: http://localhost:15672")
        print("Username: guest")
        print("Password: guest")
        print("\n")
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"\n✗ Erreur de connexion: {e}")
        print(f"  Vérifiez que RabbitMQ est démarré sur {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        sys.exit(1)


if __name__ == '__main__':
    setup_rabbitmq()
