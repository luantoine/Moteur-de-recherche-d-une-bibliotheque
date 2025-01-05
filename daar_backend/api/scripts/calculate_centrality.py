# calculate_centrality.py

import os
import sys
import django
import networkx as nx
from pymongo.errors import PyMongoError
from tqdm import tqdm

# Déterminer le chemin absolu du répertoire parent
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Remonte de deux niveaux pour atteindre le répertoire parent de 'daar_backend'

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(parent_dir)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daar_backend.settings')  # Assurez-vous que le chemin est correct
django.setup()

from api.services.mongo_client import mongo_client

def build_similarity_graph(collection):
    """
    Construire un graphe de similarité basé sur l'indice de Jaccard entre les livres.
    Les sommets sont les livres, et une arête est créée si la similarité dépasse un seuil.
    """
    G = nx.Graph()
    books = list(collection.find({}, {"book_id": 1, "subjects": 1}))
    
    # Ajouter les sommets
    for book in books:
        G.add_node(book["book_id"], subjects=set(book.get("subjects", [])))
    
    # Définir un seuil de similarité Jaccard pour créer une arête
    similarity_threshold = 0.1  # Ajustez ce seuil selon vos besoins
    
    # Ajouter les arêtes basées sur la similarité Jaccard
    print("Construction des arêtes du graphe de similarité...")
    for i in tqdm(range(len(books)), desc="Construire les arêtes du graphe"):
        for j in range(i + 1, len(books)):
            book1 = books[i]
            book2 = books[j]
            subjects1 = book1.get("subjects", [])
            subjects2 = book2.get("subjects", [])
            
            if not subjects1 or not subjects2:
                continue
            
            set1 = set(subjects1)
            set2 = set(subjects2)
            
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            
            if union:
                jaccard_similarity = len(intersection) / len(union)
                if jaccard_similarity >= similarity_threshold:
                    G.add_edge(book1["book_id"], book2["book_id"], weight=jaccard_similarity)
    
    return G

def calculate_pagerank(G):
    """
    Calculer l'indice de centralité PageRank pour chaque nœud du graphe.
    """
    print("Calcul de l'indice de centralité PageRank...")
    pagerank = nx.pagerank(G, weight='weight')
    return pagerank

def store_pagerank_and_neighbors(collection, G, pagerank):
    """
    Stocker l'indice de centralité PageRank et les voisins dans chaque document.
    """
    print("Stockage des indices de centralité et des voisins dans MongoDB...")
    for book_id in tqdm(G.nodes(), desc="Stocker les données dans MongoDB"):
        try:
            # Récupérer les voisins du livre
            neighbors = list(G.neighbors(book_id))
            
            # Récupérer l'indice de centralité
            centrality = pagerank.get(book_id, 0)
            
            # Mettre à jour le document dans MongoDB
            collection.update_one(
                {"book_id": str(book_id)},  # S'assurer que book_id est une chaîne de caractères
                {"$set": {
                    "centrality": centrality,
                    "neighbors": neighbors
                }}
            )
        except PyMongoError as e:
            print(f"[ERREUR] Échec de la mise à jour pour book_id={book_id} : {e}")

def main():
    """
    Point d'entrée du script.
    """
    collection = mongo_client.get_collection("gutenberg_books")
    
    print("Construction du graphe de similarité...")
    G = build_similarity_graph(collection)
    
    print("Calcul de l'indice de centralité PageRank...")
    pagerank = calculate_pagerank(G)
    
    print("Stockage des indices de centralité et des voisins dans MongoDB...")
    store_pagerank_and_neighbors(collection, G, pagerank)
    
    print("Calcul et stockage de l'indice de centralité et des voisins terminés.")

if __name__ == "__main__":
    main()
