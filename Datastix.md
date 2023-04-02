Datastix
==
DataStix est une entreprise éditrice de logiciels, basée à Paris. 
La société assure le développement et la distribution de FastDB, un système de gestion de base de données (SGBD) de type NoSQL conçu pour gérer des quantités massives de données.

# Challenge
DataStix cherche à améliorer les performances en lecture de sa base de données.
En effet, ses ingénieurs pensent qu'il est possible d'être encore plus rapide, mais ils ne savent pas ce qu'ils peuvent faire !

C'est pourquoi DataStix a fait appel à votre équipe et vous a mis à disposition un de leur ingénieur afin que vous développiez une amélioration à leur système.

Vous n'êtes pas la seule équipe ! Votre solution sera présentée devant le comité technique de DataStix qui validera la pertinence de vos développements.
La meilleure équipe gagnera un saucisson, une bonne bouteille de vin ainsi qu'un chèque de 1M€ !

# Moteur de stockage existant
FastDB est une base de données révolutionnaire ! 
Elle permet en effet d'enregistrer des clés/valeurs et de récupérer une valeur à partir d'une clé. Pour cela, elle organise ces données dans 2 fichiers : 
- `data.db` : Stockage de toutes les valeurs
- `index.db` : Index permettant de récupérer la position d'une valeur dans `data.db` à partir d'une clé 

Le code de FastDB est situé dans le module [`sdp.fast_db`](./sdp/fast_db) :
- [`sdp.fast_db.db`](./sdp/fast_db/db.py) : API d'utilisation de FastDB
- [`sdp.fast_db.storage`](./sdp/fast_db/storage.py) : Moteur de stockage des valeurs
- [`sdp.fast_db.index`](./sdp/fast_db/index.py) : Index

Des exemples d'utilisation sont présents dans les tests : [`tests.fast_db.test_fast_db`](./tests/fast_db/test_fast_db.py).

### Fonctionnement interne
Bien que révolutionnaire, le fonctionnement de FastDB est assez simple à comprendre.
Il y a 2 opérations principales :

**Écriture** : `FastDB#set(key, value)`
1. Ajout valeur dans `data.db` + récupération position
2. Enregistrement de la position dans `index.db`

**Lecture** : `FastDB#get(key)`
1. Recherche de la position de la valeur dans `index.db`
2. Lecture de la valeur dans `data.db`



