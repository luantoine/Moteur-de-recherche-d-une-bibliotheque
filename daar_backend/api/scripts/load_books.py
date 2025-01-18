# load_books.py

import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from time import sleep

from pymongo.errors import PyMongoError, DuplicateKeyError
from tqdm import tqdm

# Déterminer le chemin absolu du répertoire actuel (scripts/)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Remonter jusqu'au répertoire racine du projet (DAAR---Moteur-de-recherche-d-une-bibliotheque/)
# Étant donné la structure, nous remontons de deux niveaux : scripts/ -> api/ -> daar_backend/
project_root = os.path.abspath(os.path.join(current_dir, '../../'))

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(project_root)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daar_backend.daar_backend.settings')  # Chemin correct vers settings.py
django.setup()

from api.services.mongo_client import mongo_client

def fetch_gutenberg_books(limit=1664):
    """
    Récupère jusqu'à limit livres depuis l'API Gutendex en stockant dans MongoDB :
      - L'id
      - Le titre
      - La liste d'auteurs, de sujets, de langues, etc.
      - Le lien vers le texte brut (text_url) s'il existe
      - Le lien vers l'image de couverture (cover_url) s'il existe
      - Les autres informations qui pourront être utiles
    """

    base_url = "https://gutendex.com/books/"
    page_url = base_url
    fetched_count = 0

    collection = mongo_client.get_collection("gutenberg_books")

    while page_url and fetched_count < limit:
        print(f"[*] Récupération de la page : {page_url}")
        resp = requests.get(page_url)
        if resp.status_code != 200:
            print(f"    > Impossible de charger la page {page_url}, arrêt")
            break

        data = resp.json()
        results = data.get("results", [])
        next_url = data.get("next")

        for book in results:
            if fetched_count >= limit:
                break

            book_id = book["id"]
            title = book["title"]
            authors = book.get("authors", [])
            subjects = book.get("subjects", [])
            bookshelves = book.get("bookshelves", [])
            languages = book.get("languages", [])
            copyright_ = book.get("copyright", False)
            media_type = book.get("media_type", "Text")
            download_count = book.get("download_count", 0)
            formats = book.get("formats", {})

            # URL texte
            text_url = None
            for fkey, fval in formats.items():
                if fkey.startswith("text/plain"):
                    text_url = fval
                    break

            # URL image
            cover_url = formats.get("image/jpeg", None)

            book_data = {
                "book_id": str(book_id),
                "title": title,
                "authors": authors,
                "subjects": subjects,
                "bookshelves": bookshelves,
                "languages": languages,
                "copyright": copyright_,
                "media_type": media_type,
                "download_count": download_count,
                "text_url": text_url,
                "cover_url": cover_url,
            }

            try:
                # Utiliser upsert=True pour insérer ou mettre à jour le document
                result = collection.update_one(
                    {"book_id": str(book_id)},
                    {"$set": book_data},
                    upsert=True  # Insère le document si aucun n'est trouvé
                )
                if result.upserted_id:
                    fetched_count += 1
                    print(f"    > Livre '{title}' (ID={book_id}) inséré. (Total={fetched_count})")
                else:
                    print(f"    > Livre ID={book_id} mis à jour.")
            except DuplicateKeyError:
                print(f"    > Livre ID={book_id} existe déjà (violated unique index). Mise à jour en cours...")
                try:
                    collection.update_one({"book_id": str(book_id)}, {"$set": book_data})
                except PyMongoError as e:
                    print(f"[ERREUR] Échec de la mise à jour du livre ID={book_id} : {e}")
            except PyMongoError as e:
                print(f"[ERREUR] Échec de la mise à jour/insertion du livre ID={book_id} : {e}")

            sleep(0.01)

        page_url = next_url

    print(f"=== Fin {fetched_count} livres stockés ou mis à jour ===")

def main():
    fetch_gutenberg_books(limit=1664)

if __name__ == "__main__":
    main()
