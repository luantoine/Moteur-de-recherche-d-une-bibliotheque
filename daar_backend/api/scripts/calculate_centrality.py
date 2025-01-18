import os
import sys
import json
import psycopg2
import networkx as nx
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(project_root) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daar_backend.daar_backend.settings')
from daar_backend.daar_backend.settings import DATABASES


def fetch_books(cursor):
    cursor.execute("SELECT id, subjects FROM books;")
    books = cursor.fetchall()
    return [{"book_id": row[0], "subjects": row[1]} for row in books]

def update_book_data(cursor, book_id, centrality, neighbors):
    cursor.execute(
        """
        UPDATE books
        SET centrality = %s, neighbors = %s
        WHERE id = %s;
        """,
        (centrality, json.dumps(neighbors), book_id)
    )

def build_similarity_graph(cursor):
    G = nx.Graph()
    books = fetch_books(cursor)
    
    for book in books:
        G.add_node(book["book_id"], subjects=set(book.get("subjects", [])))
    
    similarity_threshold = 0.1
    for i in range(len(books)):
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
    return nx.pagerank(G, weight='weight')

def store_pagerank_and_neighbors(cursor, G, pagerank):
    for book_id in tqdm(G.nodes(), desc="Stocker les données dans PostgreSQL"):
        neighbors = list(G.neighbors(book_id))
        centrality = pagerank.get(book_id, 0)
        update_book_data(cursor, book_id, centrality, neighbors)

def main():
    db_config = DATABASES['default']
    # Connexion à PostgreSQL
    conn = psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT']
    )
    cursor = conn.cursor()
    
    try:
        print("Construction du graphe de similarité...")
        G = build_similarity_graph(cursor)
        
        print("Calcul de l'indice de centralité PageRank...")
        pagerank = calculate_pagerank(G)
        
        print("Stockage des indices de centralité et des voisins dans PostgreSQL...")
        store_pagerank_and_neighbors(cursor, G, pagerank)
        
        conn.commit()
        print("Calcul et stockage terminés.")
    except Exception as e:
        print(f"Erreur : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
