"""
RabbitMQ Consumer - Consommer des messages depuis 2iteQueue
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

# Configuration de la queue
QUEUE_NAME = '2iteQueue'


def create_connection():
    """Créer une connexion à RabbitMQ"""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)


def callback(ch, method, properties, body):
    """Fonction appelée lors de la réception d'un message"""
    print("\n" + "=" * 60)
    print(f"[✓] Message reçu à {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Afficher les propriétés
    print(f"Exchange: {method.exchange}")
    print(f"Routing Key: {method.routing_key}")
    print(f"Delivery Tag: {method.delivery_tag}")
    
    if properties.content_type:
        print(f"Content Type: {properties.content_type}")
    if properties.timestamp:
        timestamp = datetime.fromtimestamp(properties.timestamp)
        print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Décoder et afficher le message
    try:
        message = body.decode('utf-8')
        print(f"\nMessage (text):")
        print(f"  {message}")
        
        # Tenter de parser comme JSON si applicable
        if properties.content_type == 'application/json':
            try:
                data = json.loads(message)
                print(f"\nMessage (JSON):")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                pass
                
    except UnicodeDecodeError:
        print(f"\nMessage (raw bytes):")
        print(f"  {body}")
    
    # Acquitter le message
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("\n[✓] Message acquitté (ack)")
    print("-" * 60)


def consume_messages():
    """Consommer les messages de la queue en continu"""
    try:
        print("=" * 60)
        print("RabbitMQ Consumer - TP29")
        print("=" * 60)
        print(f"Connexion à RabbitMQ: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        
        # Établir la connexion
        connection = create_connection()
        channel = connection.channel()
        
        # Déclarer la queue (si elle n'existe pas déjà)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        
        # Configuration du consommateur
        channel.basic_qos(prefetch_count=1)  # Un message à la fois
        
        print(f"Queue: {QUEUE_NAME}")
        print(f"\n[*] En attente de messages... (CTRL+C pour arrêter)\n")
        
        # Commencer à consommer
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback,
            auto_ack=False  # Acquittement manuel
        )
        
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print("\n\n[!] Arrêt du consommateur...")
        try:
            channel.stop_consuming()
            connection.close()
        except:
            pass
        print("[✓] Consommateur arrêté proprement")
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"\n[✗] Erreur de connexion à RabbitMQ: {e}")
        print(f"    Vérifiez que RabbitMQ est démarré sur {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        
    except Exception as e:
        print(f"\n[✗] Erreur: {e}")


def get_one_message():
    """Récupérer un seul message de la queue"""
    try:
        connection = create_connection()
        channel = connection.channel()
        
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        
        print(f"Récupération d'un message depuis {QUEUE_NAME}...")
        
        # Récupérer un message
        method_frame, properties, body = channel.basic_get(queue=QUEUE_NAME)
        
        if method_frame:
            callback(channel, method_frame, properties, body)
        else:
            print("[!] Aucun message disponible dans la queue")
        
        connection.close()
        
    except Exception as e:
        print(f"[✗] Erreur: {e}")


def get_queue_info():
    """Afficher les informations sur la queue"""
    try:
        connection = create_connection()
        channel = connection.channel()
        
        # Déclarer passivement la queue pour obtenir ses infos
        result = channel.queue_declare(queue=QUEUE_NAME, durable=True, passive=True)
        
        print("\n" + "=" * 60)
        print(f"Informations sur la queue: {QUEUE_NAME}")
        print("=" * 60)
        print(f"Messages en attente: {result.method.message_count}")
        print(f"Consommateurs actifs: {result.method.consumer_count}")
        print("=" * 60 + "\n")
        
        connection.close()
        
    except Exception as e:
        print(f"[✗] Erreur: {e}")


def main():
    """Point d'entrée principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--one':
        # Mode: récupérer un seul message
        get_one_message()
    elif len(sys.argv) > 1 and sys.argv[1] == '--info':
        # Mode: afficher les infos de la queue
        get_queue_info()
    else:
        # Mode par défaut: consommation continue
        consume_messages()


if __name__ == '__main__':
    main()
