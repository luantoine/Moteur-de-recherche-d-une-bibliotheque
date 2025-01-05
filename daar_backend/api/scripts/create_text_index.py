# scripts/create_text_index.py

import os
import sys
import django
from pymongo.errors import OperationFailure

# Définir le chemin du projet pour que Python puisse trouver 'daar_backend'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Cela devrait pointer vers 'api/'
grandparent_dir = os.path.dirname(parent_dir)  # Cela devrait pointer vers 'daar_backend/'

# Ajouter le répertoire 'daar_backend' au PYTHONPATH
sys.path.append(grandparent_dir)

# Définir le module de paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daar_backend.settings')
django.setup()

from api.services.mongo_client import mongo_client

def create_text_index():
    """
    Crée un index textuel sur les champs "title" et "authors.name" dans la collection "gutenberg_books".
    """
    try:
        collection = mongo_client.get_collection("gutenberg_books")
        
        # Définir les champs à indexer
        index_fields = [
            ("title", "text"),
            ("authors.name", "text")
        ]
        
        # Nom de l'index
        index_name = "title_authors_text_index"
        
        # Créer l'index textuel
        result = collection.create_index(
            index_fields,
            name=index_name,
            default_language="english",
            background=True  # Crée l'index en arrière-plan
        )
        
        print(f"Index textuel '{index_name}' créé avec succès : {result}")
    
    except OperationFailure as e:
        if "already exists" in str(e):
            print(f"L'index '{index_name}' existe déjà.")
        else:
            print(f"Erreur lors de la création de l'index : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

def main():
    create_text_index()

if __name__ == "__main__":
    main()
