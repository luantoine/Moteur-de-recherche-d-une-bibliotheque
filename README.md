## Moteur de Recherche d'une Bibliothèque

### Équipe
- Arnaud UTHAYAKUMAR
- Andre VICENTE
- ANTOINE LUONG

### Objectif du Projet
L'objectif de ce projet est de développer une application web/mobile permettant d'effectuer des recherches dans une bibliothèque de documents textuels. Cette bibliothèque contiendra au minimum **1664 livres**, chaque livre ayant une taille minimale de **10 000 mots**.

L'application devra inclure un moteur de recherche efficace et performant, intégrant des fonctionnalités de recherche avancée, de classement et de suggestion de documents pertinents.

## Fonctionnalités Principales

### 1. Recherche Simple
- Recherche de livre par mot-clé.
- Récupération de tous les documents textuels contenant la chaîne de caractères recherchée.

### 2. Recherche Avancée
- Recherche par **expression régulière (RegEx)**.
- Deux modes :
  - Recherche dans la table d'indexage.
  - Recherche dans le contenu des documents (risque de dégradation des performances).

### 3. Classement des Résultats
- Tri des documents retournés selon un critère de pertinence.
- Utilisation d'au moins un des trois indices de centralité suivants :
  - **Closeness**
  - **Betweenness**
  - **PageRank**
- Définition et justification de l'indice choisi.

### 4. Suggestion de Documents
- Proposition de documents similaires aux résultats les plus pertinents.
- Approches possibles :
  - Documents voisins dans le **graphe de Jaccard**.
  - Documents les plus choisis par d'autres utilisateurs.
  - Autre stratégie à définir et expliquer dans le rapport.

## Architecture de l'Application
### 1. Couche Data
- Stockage des documents textuels et des index.
- Construction et exploitation du **graphe de Jaccard**.

### 2. Couche Serveur
- Implémentation des algorithmes de recherche et de classement.
- Utilisation d'algorithmes d'indexation et de recherche efficace (éventuellement **KMP, Jaccard, PageRank**).

### 3. Couche Client
- Interface utilisateur avec recherche simple et avancée.
- Affichage des résultats triés.
- Affichage des suggestions de lecture.

## Tests et Évaluation
- **Tests de performance** :
  - Courbes de temps d'exécution pour différents volumes de données.
  - Comparaison des performances selon l'indice de classement choisi.
- **Tests utilisateur** :
  - Evaluation de la pertinence des résultats retournés.
  - Recueil de feedbacks sur l'ergonomie et la qualité des suggestions.
