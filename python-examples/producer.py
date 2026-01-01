"""
RabbitMQ Producer - Publier des messages vers 2iteExchange
TP 29 - Architecture Microservices
"""

import pika
import sys
import json
from datetime import datetime

# Configuration de la connexion RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Configuration de l'exchange
EXCHANGE_NAME = '2iteExchange'
EXCHANGE_TYPE = 'direct'
ROUTING_KEY = ''  # Vide pour correspondre au binding


def create_connection():
    """Créer une connexion à RabbitMQ"""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)


def publish_message(message):
    """Publier un message vers l'exchange"""
    try:
        # Établir la connexion
        connection = create_connection()
        channel = connection.channel()
        
        # Déclarer l'exchange (si il n'existe pas déjà)
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type=EXCHANGE_TYPE,
            durable=True
        )
        
        # Publier le message
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Rendre le message persistant
                content_type='text/plain',
                timestamp=int(datetime.now().timestamp())
            )
        )
        
        print(f"[✓] Message publié avec succès:")
        print(f"    Exchange: {EXCHANGE_NAME}")
        print(f"    Routing Key: '{ROUTING_KEY}'")
        print(f"    Message: {message}")
        
        # Fermer la connexion
        connection.close()
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[✗] Erreur de connexion à RabbitMQ: {e}")
        print(f"    Vérifiez que RabbitMQ est démarré sur {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    except Exception as e:
        print(f"[✗] Erreur lors de la publication: {e}")


def publish_json_message(data):
    """Publier un message JSON vers l'exchange"""
    try:
        connection = create_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type=EXCHANGE_TYPE,
            durable=True
        )
        
        # Convertir le dictionnaire en JSON
        message_json = json.dumps(data)
        
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=message_json,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json',
                timestamp=int(datetime.now().timestamp())
            )
        )
        
        print(f"[✓] Message JSON publié avec succès:")
        print(f"    Exchange: {EXCHANGE_NAME}")
        print(f"    Message: {message_json}")
        
        connection.close()
        
    except Exception as e:
        print(f"[✗] Erreur lors de la publication: {e}")


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("RabbitMQ Producer - TP29")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Message passé en argument
        message = ' '.join(sys.argv[1:])
        publish_message(message)
    else:
        # Mode interactif
        print("\nChoisissez une option:")
        print("1. Envoyer un message texte")
        print("2. Envoyer un message JSON")
        print("3. Envoyer plusieurs messages de test")
        
        choice = input("\nVotre choix (1-3): ").strip()
        
        if choice == '1':
            message = input("Entrez votre message: ")
            publish_message(message)
            
        elif choice == '2':
            name = input("Nom: ")
            message = input("Message: ")
            data = {
                'name': name,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            publish_json_message(data)
            
        elif choice == '3':
            print("\nEnvoi de 5 messages de test...")
            for i in range(1, 6):
                message = f"Message de test #{i} - {datetime.now().strftime('%H:%M:%S')}"
                publish_message(message)
                print()
        else:
            print("Choix invalide!")


if __name__ == '__main__':
    main()
