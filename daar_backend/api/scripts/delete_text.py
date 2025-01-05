# delete_text.py

import os
import sys
import django
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

def delete_text_from_books(book_ids):
    """
    Supprime le contenu du champ 'text' pour les livres spécifiés par leurs 'book_id'.
    
    Args:
        book_ids (list): Liste des 'book_id' des livres à modifier.
    """
    collection = mongo_client.get_collection("gutenberg_books")
    
    for book_id in tqdm(book_ids, desc="Suppression du champ 'text' des livres"):
        try:
            result = collection.update_one(
                {"book_id": book_id},
                {"$unset": {"text": ""}}  # Utiliser $unset pour supprimer le champ
            )
            if result.modified_count == 1:
                print(f"Le champ 'text' a été supprimé avec succès pour book_id={book_id}.")
            else:
                print(f"Aucun changement effectué pour book_id={book_id}. Le livre pourrait ne pas exister ou le champ 'text' est déjà absent.")
        except PyMongoError as e:
            print(f"[ERREUR] Échec de la suppression du champ 'text' pour book_id={book_id} : {e}")

def main():
    """
    Point d'entrée du script.
    """
    # Liste des 'book_id' des livres dont vous souhaitez supprimer le champ 'text'
    # Remplacez ces valeurs par les 'book_id' réels des livres que vous souhaitez modifier
    book_ids = ["2160", "2542"]  # Exemple : "1513" pour "Hamlet" et "1342" pour "Pride and Prejudice"
    
    print(f"Suppression du champ 'text' pour les livres avec les book_id suivants : {book_ids}")
    
    delete_text_from_books(book_ids)
    
    print("Suppression terminée.")

if __name__ == "__main__":
    main()
