# TP 29 : RabbitMQ avec Docker

> Architecture Microservices : Conception, Déploiement et Orchestration

## 📋 Objectif

Mettre en place RabbitMQ via Docker, manipuler l'interface web pour créer un exchange, une queue, effectuer un binding, puis publier et consommer des messages via l'interface web et des scripts Python.

## 📁 Structure du projet

```
tp29/
├── docker/
│   └── docker-compose.yml          # Configuration Docker Compose
├── python-examples/
│   ├── setup.py                    # Script de setup automatique
│   ├── producer.py                 # Producteur de messages
│   └── consumer.py                 # Consommateur de messages
├── screenshots/                     # Captures d'écran du TP
├── requirements.txt                 # Dépendances Python
├── TP29_RabbitMQ_Docker.md         # Documentation complète du TP
└── Readme.md                        # Ce fichier
```

## 🚀 Démarrage rapide

### Option 1 : Avec Docker Compose (Recommandé)

```bash
# Démarrer RabbitMQ
cd docker
docker-compose up -d

# Vérifier que le conteneur tourne
docker-compose ps

# Voir les logs
docker-compose logs -f

# Arrêter RabbitMQ
docker-compose down
```

### Option 2 : Avec Docker run

```bash
docker run -d --hostname rabbit --name rabbit-server \
  -p 15672:15672 -p 5672:5672 \
  rabbitmq:3.12.9-management
```

## 🌐 Accès à l'interface web

- URL: http://localhost:15672
- Username: `guest`
- Password: `guest`

## 🐍 Utilisation des scripts Python

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Setup automatique (Exchange + Queue + Binding)

```bash
cd python-examples
python setup.py
```

Ce script crée automatiquement:
- Exchange: `2iteExchange` (type: direct, durable)
- Queue: `2iteQueue` (durable)
- Binding: `2iteExchange` → `2iteQueue` (routing key vide)

### 3. Publier des messages (Producer)

```bash
# Mode interactif
python producer.py

# Message en ligne de commande
python producer.py "Mon message de test"
```

Options du mode interactif:
1. Envoyer un message texte
2. Envoyer un message JSON
3. Envoyer plusieurs messages de test

### 4. Consommer des messages (Consumer)

```bash
# Mode continu (écoute permanente)
python consumer.py

# Récupérer un seul message
python consumer.py --one

# Afficher les infos de la queue
python consumer.py --info
```

## 📝 Étapes du TP

Consultez le fichier [TP29_RabbitMQ_Docker.md](TP29_RabbitMQ_Docker.md) pour le guide complet avec 13 étapes détaillées.

---

## Prérequis

- Docker installé (Docker Desktop sous Windows, ou Docker Engine sous Linux)
- Python 3.7+ (pour les scripts Python)
- Accès à Internet (pour télécharger l'image)
- Navigateur web

---

## Étape 1 — Identifier la bonne image Docker

1. Ouvrir la page Docker Hub de RabbitMQ : [https://hub.docker.com/_/rabbitmq](https://hub.docker.com/_/rabbitmq)
   - **Objectif :** repérer les tags disponibles
2. Repérer le tag `3.12.9-management` (version stable utilisée)
   - Le tag `-management` inclut l'interface web de gestion

---

## Étape 2 — Télécharger l'image (docker pull)

Exécuter la commande suivante dans un terminal :

```bash
docker pull rabbitmq:3.12.9-management
```

**Remarque :** le téléchargement peut prendre un peu de temps selon la connexion Internet.

---

## Étape 3 — Lancer le conteneur (docker run)

Exécuter la commande suivante :

```bash
docker run -d --hostname rabbit --name rabbit-server -p 15672:15672 -p 5672:5672 rabbitmq:3.12.9-management
```

### Explication des paramètres :

| Paramètre | Description |
|-----------|-------------|
| `-d` | Exécution en arrière-plan (mode détaché) |
| `--hostname rabbit` | Nom d'hôte interne du serveur RabbitMQ |
| `--name rabbit-server` | Nom du conteneur (visible dans Docker Desktop) |
| `-p 15672:15672` | Port UI (machine hôte → conteneur) pour l'interface web |
| `-p 5672:5672` | Port broker AMQP (applications clientes → RabbitMQ) |

---

## Étape 4 — Vérifier que le conteneur tourne

### Option 1 : Via Docker Desktop
1. Ouvrir **Docker Desktop**
2. Vérifier que `rabbit-server` est en état **Running**
3. Vérifier les ports exposés (15672 et 5672)

### Option 2 : Via ligne de commande

```bash
docker ps
```

Vous devriez voir une ligne contenant `rabbit-server` avec les ports 15672 et 5672.

---

## Étape 5 — Accéder à l'interface web

1. Ouvrir le navigateur web
2. Accéder à l'URL : **http://localhost:15672**
3. S'authentifier avec les identifiants par défaut :
   - **Username :** `guest`
   - **Password :** `guest`

**⚠️ Remarque importante :** L'utilisateur `guest` est généralement autorisé uniquement depuis `localhost`. Pour un accès distant, il faut créer un utilisateur dédié via l'onglet **Admin → Users**.

---

## Étape 6 — Comprendre la page d'accueil (Overview)

Après connexion, la page **Overview** affiche :

- Les compteurs en temps réel :
  - **Connections** : nombre de connexions actives
  - **Channels** : canaux de communication ouverts
  - **Exchanges** : points de routage des messages
  - **Queues** : files d'attente de messages
  - **Consumers** : consommateurs actifs
- L'état du nœud RabbitMQ :
  - Mémoire utilisée
  - Uptime (temps de fonctionnement)
  - Statistiques du broker

---

## Étape 7 — Créer un Exchange : `2iteExchange`

1. Aller dans l'onglet **Exchanges**
2. Descendre vers la section **Add a new exchange**
3. Renseigner les paramètres suivants :
   - **Name :** `2iteExchange`
   - **Type :** `direct`
   - **Durability :** `Durable`
   - **Auto delete :** `No`
   - **Internal :** `No`
   - Laisser les autres paramètres par défaut
4. Cliquer sur **Add exchange**

### 📝 Note sur les types d'exchanges :
- **direct** : routage basé sur une clé de routage exacte
- **fanout** : diffusion à toutes les queues liées
- **topic** : routage basé sur des patterns de clés
- **headers** : routage basé sur les en-têtes des messages

---

## Étape 8 — Ouvrir la page de l'exchange `2iteExchange`

1. Dans la liste des exchanges, cliquer sur **2iteExchange**
2. Observer les informations :
   - **Type** = `direct`
   - **Durable** = `true`
   - Sections disponibles :
     - **Bindings** : liens vers les queues
     - **Publish message** : publier des messages de test
     - **Delete** : supprimer l'exchange

---

## Étape 9 — Créer une Queue : `2iteQueue`

1. Aller dans l'onglet **Queues and Streams**
2. Descendre vers **Add a new queue**
3. Renseigner les paramètres :
   - **Type :** `Classic`
   - **Name :** `2iteQueue`
   - **Durability :** `Durable`
   - **Auto delete :** `No`
   - Laisser les autres paramètres par défaut
4. Cliquer sur **Add queue**

### 📝 Note sur la durabilité :
- **Durable** : la queue survit au redémarrage du broker
- **Transient** : la queue est supprimée au redémarrage

---

## Étape 10 — Faire le binding (lier l'exchange à la queue)

**Objectif :** faire en sorte que l'exchange `2iteExchange` envoie des messages vers la queue `2iteQueue`.

1. Retourner dans **Exchanges** → cliquer sur **2iteExchange**
2. Aller à la section **Bindings**
3. Dans **Add binding from this exchange** :
   - **To queue :** sélectionner/saisir `2iteQueue`
   - **Routing key :** laisser vide (ou définir une clé, ex: `rk.2ite`)
   - **Arguments :** laisser vide
4. Cliquer sur **Bind**

### ⚠️ Remarque IMPORTANTE pour un exchange `direct` :

- Si **Routing key** est vide lors du binding, alors la publication doit se faire avec une routing key **vide** aussi
- Si une clé est définie (ex : `rk.2ite`), la **même clé** doit être utilisée lors de **Publish message**

---

## Étape 11 — Publier un message dans l'exchange

1. Toujours dans la page **Exchange: 2iteExchange**
2. Ouvrir la section **Publish message**
3. Renseigner les paramètres :
   - **Routing key :** laisser vide (si binding vide) ou utiliser la clé choisie lors du binding
   - **Delivery mode :** `2 - Persistent` (recommandé pour la durabilité)
   - **Headers :** laisser vide
   - **Properties :** laisser vide
   - **Payload :** saisir le message, exemple :
     ```
     Hi I'm Oussama from RabbitMQ WebUI
     ```
4. Cliquer sur **Publish message**

### 📝 Confirmation :
Après publication, un message de confirmation apparaît : **"Message published"**

---

## Étape 12 — Vérifier l'arrivée des messages dans la queue

1. Aller dans l'onglet **Queues and Streams**
2. Cliquer sur **2iteQueue**
3. Vérifier les indicateurs :
   - **Ready** > 0 : messages en attente de consommation
   - **Total** : nombre total de messages
   - Les graphiques affichent :
     - **Queued messages** : évolution du nombre de messages
     - **Message rates** : taux d'entrée/sortie des messages

### 📊 Interprétation :
- **Ready** : messages disponibles pour consommation
- **Unacked** : messages en cours de traitement (acquittement non reçu)
- **Total** : Ready + Unacked

---

## Étape 13 — Lire un message (Get messages)

1. Dans la page de **2iteQueue**, descendre à la section **Get messages**
2. Configurer les paramètres :
   - **Ack Mode :** 
     - **Ack message requeue false** : consomme et supprime définitivement le message
     - **Nack message requeue true** : remet le message dans la queue (pratique pour tester sans vider)
     - **Reject requeue false** : rejette et supprime le message
   - **Encoding :** `Auto string / base64`
   - **Messages :** `1` (nombre de messages à récupérer)
3. Cliquer sur **Get Message(s)**
4. Observer le **Payload** affiché dans les résultats

### ⚠️ Remarque importante :

L'interface indique que **"getting messages from a queue is a destructive action"**.

- Pour **tester sans vider** la queue : utiliser **Nack message requeue true**
- Pour **consommer réellement** : utiliser **Ack message requeue false**

### 📋 Informations affichées :

- **Exchange** : l'exchange d'origine
- **Routing Key** : la clé de routage utilisée
- **Redelivered** : indique si le message a déjà été délivré
- **Properties** : propriétés du message (content_type, delivery_mode, etc.)
- **Payload** : le contenu du message

---

## Résumé des concepts clés

### 🔄 Flux de message dans RabbitMQ :

```
Publisher → Exchange → [Binding + Routing Key] → Queue → Consumer
```

### 📚 Composants principaux :

| Composant | Rôle |
|-----------|------|
| **Exchange** | Point d'entrée des messages, les route vers les queues |
| **Queue** | Stocke les messages en attente de consommation |
| **Binding** | Lien entre un exchange et une queue (avec routing key) |
| **Routing Key** | Clé utilisée pour le routage des messages |
| **Consumer** | Application qui lit et traite les messages |

### 🎯 Types d'exchanges :

- **Direct** : routage exact par routing key
- **Fanout** : broadcast à toutes les queues liées
- **Topic** : routage par pattern (ex: `logs.*.error`)
- **Headers** : routage par en-têtes HTTP

---

## Commandes Docker utiles

### Voir les logs du conteneur :
```bash
docker logs rabbit-server
```

## 🎯 Concepts clés

### Flux de message RabbitMQ
```
Publisher → Exchange → [Binding + Routing Key] → Queue → Consumer
```

### Composants

| Composant | Rôle |
|-----------|------|
| **Exchange** | Point d'entrée des messages, les route vers les queues |
| **Queue** | Stocke les messages en attente de consommation |
| **Binding** | Lien entre un exchange et une queue |
| **Routing Key** | Clé utilisée pour le routage |

### Types d'Exchange

- **Direct**: routage exact par routing key
- **Fanout**: broadcast à toutes les queues
- **Topic**: routage par pattern (ex: `logs.*.error`)
- **Headers**: routage par en-têtes

## 🔧 Commandes utiles

### Docker

```bash
# Voir les logs
docker logs rabbit-server

# Voir les logs en temps réel
docker logs -f rabbit-server

# Arrêter le conteneur
docker stop rabbit-server

# Démarrer le conteneur
docker start rabbit-server

# Redémarrer le conteneur
docker restart rabbit-server

### Supprimer le conteneur :
```bash
docker rm -f rabbit-server
```

### Entrer dans le conteneur (shell) :
# Supprimer le conteneur
docker rm -f rabbit-server

# Entrer dans le conteneur
docker exec -it rabbit-server bash
```

### RabbitMQ CLI (dans le conteneur)

```bash
# Lister les queues
docker exec rabbit-server rabbitmqctl list_queues

# Lister les exchanges
docker exec rabbit-server rabbitmqctl list_exchanges

# Lister les bindings
docker exec rabbit-server rabbitmqctl list_bindings
```

---

## 🧪 Exercices

### Exercice 1: Multiple bindings
1. Créer une 2ème queue: `2iteQueue2`
2. Binder avec routing key `rk.test`
3. Tester le routage avec différentes routing keys

### Exercice 2: Fanout Exchange
1. Créer un exchange `fanoutExchange` (type: fanout)
2. Créer 2 queues et les binder
3. Publier un message → il arrive dans les 2 queues

### Exercice 3: Persistence
1. Publier plusieurs messages
2. Arrêter le conteneur
3. Redémarrer et vérifier la persistence

## 🐛 Dépannage

### Impossible d'accéder à http://localhost:15672

- Vérifier: `docker ps`
- Attendre 10-20s (initialisation)
- Logs: `docker logs rabbit-server`

### Message n'arrive pas dans la queue

- Vérifier le binding
- Vérifier que la routing key correspond
- Pour exchange `direct`: correspondance exacte requise

### Port déjà utilisé

```bash
# Utiliser d'autres ports
docker run -d --name rabbit-server \
  -p 15673:15672 -p 5673:5672 \
  rabbitmq:3.12.9-management
```

## 📚 Ressources

- [Documentation RabbitMQ](https://www.rabbitmq.com/documentation.html)
- [Tutoriels RabbitMQ](https://www.rabbitmq.com/getstarted.html)
- [Docker Hub RabbitMQ](https://hub.docker.com/_/rabbitmq)
- [Pika Documentation](https://pika.readthedocs.io/)

## 🎓 Pour aller plus loin

- Développer une application complète Producer/Consumer
- Implémenter les patterns: Work Queues, Pub/Sub, Routing, Topics, RPC
- Configurer un cluster RabbitMQ
- Mettre en place SSL/TLS et la gestion des utilisateurs

---

**Auteur**: TP Architecture Microservices  
**Date**: Janvier 2026  
**Version**: 1.0
