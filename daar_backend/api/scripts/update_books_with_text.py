# update_books_with_text.py

import os
import sys
import django
import requests
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from tqdm import tqdm
from time import sleep

# Déterminer le chemin absolu du répertoire parent
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Remonte de deux niveaux pour atteindre le répertoire parent de 'daar_backend'

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(parent_dir)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daar_backend.settings')  # Assurez-vous que le chemin est correct
django.setup()

from api.services.mongo_client import mongo_client

def download_text(url):
    """
    Télécharge le contenu textuel depuis l'URL donnée.
    Retourne le texte en clair ou None en cas d'échec.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERREUR] Échec du téléchargement depuis {url} : {e}")
        return None

def update_books_with_text(limit=1664, batch_size=100):
    """
    Itère sur les documents de la collection 'gutenberg_books' qui ont un 'text_url' mais pas encore de 'text'.
    Télécharge le contenu depuis 'text_url' et ajoute-le dans le champ 'text'.
    """
    collection = mongo_client.get_collection("gutenberg_books")
    
    # Requête pour trouver les documents avec 'text_url' mais sans 'text'
    query = {
        "$and": [
            { "text_url": { "$exists": True, "$ne": "" } },
            { "$or": [
                { "text": { "$exists": False } },
                { "text": "" }
            ]}
        ]
    }
    
    total_documents = collection.count_documents(query)
    if total_documents == 0:
        print("Aucun document à mettre à jour.")
        return
    
    print(f"Nombre total de documents à mettre à jour : {total_documents}")
    
    # Itérer avec une barre de progression
    for doc in tqdm(collection.find(query).batch_size(batch_size), total=total_documents, desc="Mise à jour des documents"):
        if limit and limit <= 0:
            break
        
        book_id = doc.get("book_id", "N/A")
        title = doc.get("title", "N/A")
        text_url = doc.get("text_url")
        
        if not text_url:
            print(f"[AVERTISSEMENT] Document avec book_id={book_id} n'a pas de 'text_url'. Skipping.")
            continue
        
        # Télécharger le contenu textuel
        content = download_text(text_url)
        
        if content:
            try:
                # Mettre à jour le document avec le contenu téléchargé
                result = collection.update_one(
                    { "_id": doc["_id"] },
                    { "$set": { "text": content } }
                )
                if result.modified_count == 1:
                    tqdm.write(f"Document book_id={book_id} mis à jour avec succès.")
                    limit -= 1
                else:
                    tqdm.write(f"[AVERTISSEMENT] Document book_id={book_id} n'a pas été mis à jour.")
            except PyMongoError as e:
                tqdm.write(f"[ERREUR] Échec de la mise à jour du document book_id={book_id} : {e}")
        else:
            tqdm.write(f"[ERREUR] Contenu non téléchargé pour book_id={book_id}.")
        
        # Respecter les bonnes pratiques et ne pas surcharger les serveurs
        sleep(0.1)  # Ajustez ce délai selon vos besoins et les conditions d'utilisation de Project Gutenberg

def main():
    """
    Point d'entrée du script.
    """
    # Vous pouvez ajuster la limite si nécessaire
    update_books_with_text(limit=1664, batch_size=100)
    print("Mise à jour terminée.")

if __name__ == "__main__":
    main()
