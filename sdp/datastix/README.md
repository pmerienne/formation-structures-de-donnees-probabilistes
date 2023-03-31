Datastix
==
DataStix est une entreprise éditrice de logiciels, basée à Paris. 
La société assure le développement et la distribution de FastDB, un système de gestion de base de données (SGBD) de type NoSQL conçu pour gérer des quantités massives de données.

# Challenge
DataStix cherche à améliorer les performances en lecture de sa base de données.
Ses ingénieurs ont notamment détecté une dégradation des performances lorsque l'index utilisé devenait trop gros.

Vous avez deux heures pour développer une amélioration à leur système.
Votre solution sera présenté devant le comité technique de DataStix qui validera la pertinence de vos développements.

La meilleure équipe gagnera un saucisson, une bonne bouteille de vin ainsi qu'un chèque de 1M€ !

# Moteur de stockage existant
FastDB est une base de données révolutionnaire ! 
Elle permet en effet d'enregistrer des clés/valeurs et de récupérer une valeur à partir d'une clé. Pour cela, elle organise ces données dans 2 fichiers : 
- `data.db` : Stockage de toutes les valeurs
- `index.db` : Index permettant de récupérer la position d'une valeur dans `data.db` à partir d'une clé 

## Écriture
1. Ajout valeur dans `data.db` + récupération position
2. Enregistrement de la position dans `index.db`

## Lecture
1. Recherche de la position de la valeur dans `index.db`
2. Lecture de la valeur dans `data.db`



