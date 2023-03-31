Structure de données probabiliste : Filtre de bloom
== 
Il y a quelques années, je m’intéressais aux bases de données NoSQL et particulièrement à Cassandra. J’étais très impressionné par les capacités de montée en charge et la performance de ce genre de base de données. Au-delà des changements conceptuels apportés par cette nouvelle génération de base de données, je me demandais comment les développeurs de Cassandra avaient pu obtenir d’aussi bonnes performances ? J’avais donc entreprit de comprendre le fonctionnement interne de Cassandra et j’ai ainsi découvert l'existence des structures de données probabilistes.

Quand on cherche à stocker des données en maximisant les performances, les accès (lecture/écriture) ont habituellement recours à des structures de données conventionnelles. Les structures de données permettent d’organiser, de traiter, d’extraire et de stocker des données pour répondre à un besoin précis, afin de pouvoir y accéder de manière performante. Les bases de données relationnelles utilisent par exemple des arbres binaires pour accélérer les requêtes de plage (range queries). Il existe beaucoup de structures de données qui répondent chacune à un besoin précis. Devant ce panel de possibilités, on peut donc se demander ce que peuvent apporter en plus les structures de données probabilistes  ?

Nous allons essayer d’éviter de parler de probabilité ! Donc n’ai pas peur si tu n’es pas un crack en mathématiques !

# Cassandra, euh je suis pas trop calé en mythologie !
![cassandra](https://user-images.githubusercontent.com/739495/229084486-5e31f22a-a6e4-4f7d-a4a2-5179c50944d3.jpg)

Les données de Cassandra sont stockées sous forme de lignes. Chaque ligne est identifiée par une clé de partition (une sorte de clé primaire) qui servira à accéder à la ligne de manière performante.
[Grossièrement](https://cassandra.apache.org/doc/latest/cassandra/architecture/storage_engine.html), le stockage de ces lignes se fait dans des SSTables. 
Ces SSTables sont constituées de plusieurs fichiers permettant d’assurer leur fonctionnement. On peut notamment citer : 
- Data.db : Stockage des lignes
- Index.db : Index des clé de partitions et des positions des lignes dans Data.db

De cette manière, pour accéder à une ligne à partir d’une clé de partition, Cassandra va utiliser l’index pour identifier la position de la ligne puis la lire dans le stockage. Jusqu’à maintenant, rien de nouveau ! Utiliser un index est plutôt commun pour accéder rapidement à un enregistrement. 
Mais en réalité, Cassandra améliore les performances en utilisant un filtre de bloom avant la lecture index. Ce filtre permet très rapidement (plus rapidement qu’un index !!) de savoir si une clé de partition existe dans une SSTable. De cette manière, elle évite le parcours de l’index.

# Plus rapide qu’un index ?
Les index sont des structures de données permettant de rechercher des informations très rapidement. Comment peut-on être plus rapide ? En réalité, un index peut être lent à parcourir, surtout s’il est trop gros pour être chargé en mémoire. Dans ce cas là, des accès en lecture sur le disque sont nécessaires et là ça fait mal !!!

Un filtre de bloom est une structure de données de type ensemble (imagine toi une set en python) qui permet de vérifier la présence d’un élément dans un ensemble. Mais c’est surtout une structure de données probabiliste, elle utilise en effet les probabilités pour stocker de manière efficace les données et se permet d’avoir des faux positifs lors du test de présence.

Des faux positifs !!! Oui tu as bien lu, les filtres de bloom peuvent se tromper !! En tant que développeur, tu dois te dire que la personne qui a inventé ce filtre de Bloom n’a rien compris à la beauté du déterminisme en informatique !

![i've no idea](https://user-images.githubusercontent.com/739495/229086614-478c58f7-18f9-4883-9dbb-78a8202f352a.gif)

En vrai, Burton Howard Bloom est un génie ! Il a compris que l’acceptation de faux-positifs permettait de créer une superbe structure de données !

Prenons notre exemple de cassandra, le filtre de bloom est utilisé pour savoir si une ligne est présente dans une SSTable pour éviter un scan d’index.
Dans ce cas, le filtre peut nous dire avec certitude l'absence d'un élément (il ne peut pas y avoir de faux négatif) et avec une certaine probabilité la présence d'un élément (il peut y avoir des faux positifs). 
Si le filtre se trompe, l’index sera parcouru mais ce n’est pas si grave que ça si le taux de faux positif est garanti bas. 
Par exemple avec un taux de faux positif de 10% : 
- 90% du temps, le filtre permet d’éviter le parcours de l’index
- 10% du temps, le filtre ne permet pas d’éviter ce parcours

C’est magique et bien pensé, non ? Et est-ce que je vous ai dit que l’espace mémoire nécessaire pour stocker tous les éléments est extrêmement réduit. 
Magique je vous dit !!

![magic](https://user-images.githubusercontent.com/739495/229087094-7768bd9e-2d70-447f-8057-e81aa1fce9d5.gif)

# La magie j’y crois pas !
Rentrons maintenant dans le vif du sujet, un filtre de Bloom est constitué d'un tableau de bits ainsi que plusieurs fonctions de hachage. Les fonctions de hachage associent chaque élément à une case du tableau. Pour ajouter un élément, il suffit de “mettre des 1” dans les cases d'indice données par les fonctions de hachage. 

![ajout](https://user-images.githubusercontent.com/739495/229087732-82f07dd4-5be1-41f2-a296-3ff9cd208b12.jpg)

Pour tester si un élément est présent, on vérifie que les cases d'indice (données par les fonctions de hachage) contiennent toutes un 1.
![verification](https://user-images.githubusercontent.com/739495/229087794-42151c16-d437-40cd-a2c9-70523dd5bbc3.jpg)

Dans ce cas, avec 3 fonctions de hachages et un tableau de 10 bits, il y a de grandes chances d’avoir des faux positifs.

![collision](https://user-images.githubusercontent.com/739495/229088013-6c2e0723-b961-417e-9b27-75e4cc47abab.jpg)

# La clé de la réussite : le taux de faux positif
Il est facile de s’imaginer que le taux de faux-positif va dépendre de la taille du tableau de bits et du nombre de fonctions de hachage. On peut aisément (pas moi !) déduire ce taux comme étant :

![formule](https://user-images.githubusercontent.com/739495/229088335-133ed251-408b-4486-8e62-4c08a709f0a0.png)

Avec : 
- f : Taux de faux-positif
- m : Taille du tableau de bits
- k : Nombre de fonction de hachage
- n : Nombre d’éléments insérés

On peut ainsi faire varier l’utilisation de l’espace mémoire et le taux de faux positifs. Pratique non ?

Quelques exemples :
| Nombre d’éléments | Taux de faux positif | Fonctions de hachage | Taille du tableau (bit) |
|-------------------|----------------------|----------------------|-------------------------|
| 100               | 1%                   | 6                    | 958                     |
| 100               | 5%                   | 4                    | 623                     |
| 100               | 10%                  | 3                    | 479                     |
| 1000              | 1%                   | 6                    | 9585                    |
| 1000              | 5%                   | 4                    | 6235                    |
| 1000              | 10%                  | 3                    | 4792                    |
| 10000             | 1%                   | 6                    | 95850                   |
| 10000             | 5%                   | 4                    | 62352                   |
| 10000             | 10%                  | 3                    | 47925                   |

# Et voilà !
J'espère que tu as bien compris l'intérêt des filtres de bloom. Cette structure de données est vraiment super pratique et elle est utilisé dans de nombreux systèmes.

Par exemple, Google Chrome protège les utilisateurs en utilisant une énorme blacklist (>1M d'urls). 
Ces URL, représentées de manière classique occuperaient plusieurs dizaines de MB ! 
Chrome a donc choisi de représenter cette liste sous la forme d’un filtre de Bloom, ce qui a permis de réduire la consommation mémoire à deux mégas, et de garantir une validation en temps constant.

# Tu veux aller plus loin ?
- Essaies d'exprimer mathématiquement des valeurs optimales de m et k en fonction de f et n !
- [Une autre structure de données probabiliste : HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog)
- [Moteur de stockage Cassandra](https://cassandra.apache.org/doc/latest/cassandra/architecture/storage_engine.html)

